from django import forms
from .models import Schema, Column


class Login(forms.Form):
    username = forms.CharField(
        label='', max_length=75, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control-name',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        label='', max_length=75, required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control-password',
            'placeholder': 'Password'
        })
    )


class SchemaForm(forms.ModelForm):
    class Meta:
        model = Schema
        fields = [
            'name',
            'column_separator',
            'string_character'
        ]

    def __init__(self, *args, **kwargs):
        super(SchemaForm, self).__init__(*args, **kwargs)
        for _, f in self.fields.items():
            f.widget.attrs['class'] = 'form-control form-control-schema'


ColumnFormSet = forms.inlineformset_factory(Schema, Column, fields=(
    'name',
    'type',
    'range_from',
    'range_to',
    'order',), extra=1, can_delete=True)


class RowForm(forms.Form):
    rows = forms.IntegerField()