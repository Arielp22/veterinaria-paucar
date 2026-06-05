# veterinaria/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from veterinaria.views.health   import health_check
from veterinaria.views.auth     import RegisterView, LogoutView
from veterinaria.views.user     import UserViewSet
from veterinaria.views.servicio import ServicioViewSet
from veterinaria.views.item     import ItemClinicoViewSet
from veterinaria.views.ticket   import TicketAtencionViewSet
from veterinaria.views.mascota  import MascotaViewSet
from veterinaria.views.vacuna   import VacunaViewSet
from veterinaria.serializers.auth import CustomTokenView

router = DefaultRouter()
router.register('users',            UserViewSet,            basename='user')
router.register('servicios',        ServicioViewSet,        basename='servicio')
router.register('items-clinicos',   ItemClinicoViewSet,     basename='item-clinico')
router.register('tickets-atencion', TicketAtencionViewSet,  basename='ticket-atencion')
router.register('mascotas',         MascotaViewSet,         basename='mascota')
router.register('vacunas',          VacunaViewSet,          basename='vacuna')

urlpatterns = [
    path('health/',             health_check),
    path('auth/register/',      RegisterView.as_view()),
    path('auth/login/',         CustomTokenView.as_view()),
    path('auth/token/refresh/', TokenRefreshView.as_view()),
    path('auth/token/verify/',  TokenVerifyView.as_view()),
    path('auth/logout/',        LogoutView.as_view()),
    path('', include(router.urls)),
]