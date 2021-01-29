from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .models import Schema, Column, Dataset
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .csv_generator import get_csv_config
from .tasks import write_csv
from django.http import JsonResponse
from django.template.loader import render_to_string
from .forms import Login, SchemaForm, ColumnFormSet, RowForm


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = Login()
        return render(request, "login.html", context={
            'form': form
        })

    def post(self, request):
        form = Login(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("generator:schemas_list")

        return render(request, "login.html", context={
            'form': form,
            'invalid': True,
        })


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('generator:start_page')


@login_required
def view_schemas(request):
    user = request.user
    schemas = user.schemas.all()
    return render(request, "schemas.html", context={
        'schemas': schemas
    })


@login_required
def view_delete_schema(request, schema_id):
    user = request.user
    schema = get_object_or_404(Schema, id=schema_id, user=user)
    schema.delete()
    return redirect("generator:schemas_list")


@login_required
def view_schema_edit(request, schema_id=None):
    schema = Schema(user=request.user)
    if schema_id:
        schema = get_object_or_404(Schema, user=request.user, pk=schema_id)

    if request.method == 'POST':
        form = SchemaForm(request.POST, instance=schema)

        if form.is_valid():
            schema = form.save(commit=False)
            schema.modified = timezone.now()
            schema.save()

        formset = ColumnFormSet(request.POST, instance=schema)

        if formset.is_valid():
            formset.save()

        if not 'add' in request.POST:
            return redirect('generator:schemas_list')

        return redirect('generator:edit_schema', schema.id)

    formset = ColumnFormSet(instance=schema)
    form = SchemaForm(instance=schema)
    return render(request, "schema_edit.html", context={
        'form': form,
        'schema': schema,
        'formset': formset
    })


@login_required
def view_datasets(request, schema_id=None):
    user = request.user
    schema = get_object_or_404(Schema, id=schema_id, user=user)
    datasets = schema.datasets.all()
    form = RowForm()

    if request.method == 'POST':
        form = RowForm(request.POST)
        if form.is_valid():
            rows = form.cleaned_data['rows']
            dataset = Dataset.objects.create(
                created=timezone.now(),
                status=0,
                schema_id=schema_id)
            config = get_csv_config(Schema, schema_id)
            write_csv.delay(config, rows, dataset.id)
        return redirect('generator:schema_datasets', schema.id)

    return render(request, "datasets.html", context={
        'datasets': datasets, 'form': form
    })


@login_required
def view_datasets(request, schema_id=None):
    user = request.user
    schema = get_object_or_404(Schema, id=schema_id, user=user)
    datasets = schema.datasets.all()
    form = RowForm()

    if request.is_ajax() and request.method == 'GET':
        context = {'datasets': datasets}
        rendered_table = render_to_string('status_table.html', context=context)
        data = {'rendered_table': rendered_table}
        return JsonResponse(data)

    if request.method == 'POST':
        form = RowForm(request.POST)
        if form.is_valid():
            rows = form.cleaned_data['rows']
            dataset = Dataset.objects.create(
                created=timezone.now(),
                status=0,
                schema_id=schema_id)
            config = get_csv_config(Schema, schema_id)
            write_csv.delay(config, rows, dataset.id)
        return redirect('generator:schema_datasets', schema.id)

    return render(request, "datasets.html", context={
        'datasets': datasets, 'form': form
    })
