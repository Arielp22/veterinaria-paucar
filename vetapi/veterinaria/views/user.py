# veterinaria/views/user.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from veterinaria.serializers.user import (
    UserSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer,
)
from veterinaria.pagination import StandardPagination

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset           = User.objects.all().order_by('id')
    serializer_class   = UserSerializer
    pagination_class   = StandardPagination
    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields   = ['role', 'is_active']
    search_fields      = ['username', 'email', 'first_name', 'last_name']
    ordering_fields    = ['id', 'username', 'date_joined']
    ordering           = ['id']

    def get_permissions(self):
        """Solo veterinarios o administradores listan o mutan usuarios globales."""
        if self.action in ['profile', 'change_password']:
            return [IsAuthenticated()]
        return [IsAuthenticated()] # Nota: Puedes validar roles customizados aquí

    def check_permissions(self, request):
        super().check_permissions(request)
        if self.action not in ['profile', 'change_password']:
            if not (request.user.is_superuser or request.user.role == 'VET'):
                self.permission_denied(request, message="No tienes permisos médicos o de administración.")

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated],
        url_path='profile',
    )
    def profile(self, request):
        if request.method == 'GET':
            return Response(
                UserProfileSerializer(request.user, context={'request': request}).data
            )
        serializer = UserProfileSerializer(
            request.user,
            data=request.data,
            partial=True,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(
        detail=False,
        methods=['post'],
        permission_classes=[IsAuthenticated],
        url_path='change-password',
    )
    def change_password(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response({'message': 'Contraseña actualizada. Por favor, inicia sesión nuevamente.'})

    @action(
        detail=True,
        methods=['post'],
        url_path='toggle-active',
    )
    def toggle_active(self, request, pk=None):
        user = self.get_object()
        user.is_active = not user.is_active
        user.save(update_fields=['is_active'])
        state = 'activado' if user.is_active else 'desactivado'
        return Response({'message': f'Usuario {state}.', 'is_active': user.is_active})

    @action(
        detail=False,
        methods=['get'],
        url_path='stats',
    )
    def stats(self, request):
        qs = User.objects.all()
        return Response({
            'total':    qs.count(),
            'active':   qs.filter(is_active=True).count(),
            'inactive': qs.filter(is_active=False).count(),
            'admins': qs.filter(role='ADMIN').count(),
            'vets': qs.filter(role='VET').count(),
            'staff': qs.filter(role='STAFF').count(),
        })