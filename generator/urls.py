from django.urls import path
from . import views


app_name = 'generator'

urlpatterns = [
path('', views.LoginView.as_view(), name="start_page"),
path('logout/', views.LogoutView.as_view(), name="LogoutView"),
path('schema/create/', views.view_schema_edit, name='new_schema'),
path('schema/edit/<int:schema_id>/', views.view_schema_edit, name='edit_schema'),
path('schemas/', views.view_schemas, name="schemas_list"),
path('delete/<schema_id>/', views.view_delete_schema, name='delete_schema'),
path('dataset/<int:schema_id>/', views.view_datasets, name='schema_datasets'),
     ]
