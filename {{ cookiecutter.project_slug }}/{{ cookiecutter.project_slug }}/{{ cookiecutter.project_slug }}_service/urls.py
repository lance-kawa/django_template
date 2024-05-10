"""
URL configuration for {{ cookiecutter.project_slug }}_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from {{ cookiecutter.project_slug }}_service.logger import trigger_logger


def trigger_logs_view(request):
    trigger_logger()
    return HttpResponse('Test logs !')


def healthcheck(request):
    return HttpResponse(
        'I am {{ cookiecutter.project_slug }} and I am alive!', status=200, content_type='text/plain'
    )


urlpatterns = [
    path('admin/', admin.site.urls),
    path('trigger-logs/', trigger_logs_view, name='trigger-logs'),
    path('health/', healthcheck, name='healthcheck'),
    path(
        'docs/',
        TemplateView.as_view(
            template_name='swagger-ui.html',
            extra_context={'schema_url': 'openapi-schema'},
        ),
        name='docs',
    ),
    path(
        'openapi/',
        get_schema_view(
            title='{{ cookiecutter.project_slug }} schema',
            description='API for {{ cookiecutter.project_slug }} service',
            version='1.0.0',
        ),
        name='openapi-schema',
    ),
]
