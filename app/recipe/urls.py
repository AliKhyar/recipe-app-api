from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app.recipe import views

router = DefaultRouter()
router.register('tags', views.TagViewSet)

app_name = 'recispe'

urlpatterns = [
    path('', include(router.urls))
]
