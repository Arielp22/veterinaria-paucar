# veterinaria/serializers/auth.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class CustomTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email']    = user.email
        token['role']     = user.role  # Rol específico veterinaria
        token['is_staff'] = user.is_staff or (user.role == 'VET')
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_id']  = self.user.id
        data['username'] = self.user.username
        data['email']    = self.user.email
        data['role']     = self.user.role
        data['is_staff'] = self.user.is_staff or (self.user.role == 'VET')
        return data

class CustomTokenView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer