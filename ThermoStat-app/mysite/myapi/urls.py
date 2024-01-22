from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'mode',views.ModeViewSet)
router.register(r'state',views.StateViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('control/', views.control, name='control'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]