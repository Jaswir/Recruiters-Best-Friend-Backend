"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.contrib import admin
from django.urls import path, include
from api import views

schema_view = get_schema_view(
    openapi.Info(
        title="Recruiters Best Friend API",
        default_version="v1",
        description="Recruiters Best Friend API",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("admin/", admin.site.urls),
    path("query/", views.query),
    path("upload/", views.uploadFile),
<<<<<<< HEAD
    path("slackQuery/", views.slackQuery),
    path('analyze/', views.analyzeInput),
    path('hello/', views.hello_there),
=======
    path("list/", views.list_doc),
    path("del_doc/", views.del_doc)
>>>>>>> 1d959ca (added endpoint to delet docs in corpus)
]
