from django.http import request
from rest_framework import response, serializers, settings, status
from rest_framework.utils import field_mapping
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from .models import User
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.middleware import csrf


class Client_AdminList(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['firstname', 'username', 'firstname', 'email', 'avatar', 'Joined_date',
                  'is_active', 'is_staff', 'is_superuser', 'Mail_opt_in', 'type', 'last_login']

class Profile_AdminList(serializers.ModelSerializer):
    user = Client_AdminList()
    class Meta:
        model = User
        fields = ['avatar',]



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attr):
        data = super().validate(attr)
        # token = self.get_token(self.user)
        # serializer = UserSerializer
        data['email'] = self.user.email
        data['firstname'] = str(self.user.firstname)
        data['username'] = str(self.user.username)
        data['type'] = str(self.user.type)
        data['is_active'] = str(self.user.is_active)
        data['Joined_date'] = str(self.user.Joined_date)
        data['is_superuser'] = str(self.user.is_superuser)
        return data


class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    firstname = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'firstname', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}, 'joined_date' : {'read_only': True}}

    def validate(self, args):
        email = args.get('email', None)
        username = args.get('username', None)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'email': ('Email address already in use!')})
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {'username': ('Username already in use!')})

        return super().validate(args)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        # as long as the fields are the same, we can just use this
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, )
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct"})
        return value


    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError(
                {"authorize": "You dont have permission for this user."})

        instance.set_password(validated_data['password'])
        instance.save()

        return instance



class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']