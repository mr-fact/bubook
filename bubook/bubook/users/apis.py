from django.core.validators import MinLengthValidator
from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from bubook.api.mixins import ApiAuthMixin
from bubook.users.models import BaseUser
from bubook.users.services import register, create_new_otp, validate_otp
from .validators import number_validator, special_char_validator, letter_validator, phone_validator, otp_code_validator


class UserApi(ApiAuthMixin, APIView):
    class OutPutUserSerializer(serializers.ModelSerializer):
        class Meta:
            model = BaseUser
            fields = ('phone', 'email',)

    @extend_schema(responses=OutPutUserSerializer, tags=['user', ])
    def get(self, request):
        return Response(self.OutPutUserSerializer(request.user, context={"request": request}).data)


class RegisterApi(APIView):
    class InputRegisterSerializer(serializers.Serializer):
        phone = serializers.CharField(max_length=15, validators=[phone_validator])
        email = serializers.EmailField(max_length=255, required=False)
        password = serializers.CharField(
            validators=[
                number_validator,
                letter_validator,
                special_char_validator,
                MinLengthValidator(limit_value=10)
            ]
        )
        confirm_password = serializers.CharField(max_length=255)

        def validate_email(self, email):
            if BaseUser.objects.filter(email=email).exists():
                raise serializers.ValidationError("email Already Taken")
            return email

        def validate(self, data):
            if not data.get("password") or not data.get("confirm_password"):
                raise serializers.ValidationError("Please fill password and confirm password")

            if data.get("password") != data.get("confirm_password"):
                raise serializers.ValidationError("confirm password is not equal to password")
            return data

    class OutPutRegisterSerializer(serializers.ModelSerializer):
        token = serializers.SerializerMethodField("get_token")

        class Meta:
            model = BaseUser
            fields = ("phone", "email", "token", "created_at", "updated_at")

        def get_token(self, user):
            data = dict()
            token_class = RefreshToken

            refresh = token_class.for_user(user)

            data["refresh"] = str(refresh)
            data["access"] = str(refresh.access_token)

            return data

    @extend_schema(request=InputRegisterSerializer, responses=OutPutRegisterSerializer, tags=['user', ])
    def post(self, request):
        serializer = self.InputRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = register(
                phone=serializer.validated_data.get("phone"),
                email=serializer.validated_data.get("email"),
                password=serializer.validated_data.get("password"),
            )
        except Exception as ex:
            return Response(
                f"Database Error {ex}",
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(self.OutPutRegisterSerializer(user, context={"request": request}).data)


class SendOtpApi(APIView):
    class InputPhoneSerializer(serializers.Serializer):
        phone = serializers.CharField(max_length=15, validators=[phone_validator])

        def validate(self, attrs):
            if not BaseUser.objects.filter(phone=attrs["phone"]).exists():
                raise serializers.ValidationError("phone not found")
            return attrs

        def create(self, validated_data):
            create_new_otp(phone=validated_data.get("phone"))
            return validated_data

    @extend_schema(summary='send otp code', tags=['user'], request=InputPhoneSerializer())
    def post(self, request):
        serializer = self.InputPhoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except Exception as ex:
            return Response({'detail': str(ex)}, status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_200_OK)


class PasswordRecoveryApi(APIView):
    class InputOtpSerializer(serializers.Serializer):
        phone = serializers.CharField(max_length=15, validators=[phone_validator])
        otp_code = serializers.CharField(max_length=15, validators=[otp_code_validator])
        new_password = serializers.CharField(
            validators=[number_validator, letter_validator, special_char_validator, MinLengthValidator(limit_value=10)]
        )
        confirm_password = serializers.CharField(max_length=128)

        def validate(self, attrs):
            if attrs.get('new_password') != attrs.get('confirm_password'):
                raise serializers.ValidationError(
                    {'confirm_password': 'new_password and confirm_password do not match'})
            if not BaseUser.objects.filter(phone=attrs["phone"]).exists():
                raise serializers.ValidationError({'phone': 'this phone not found'})
            result, message = validate_otp(phone=attrs.get('phone'), code=attrs.get('otp_code'))
            if not result:
                raise serializers.ValidationError({'otp_code': message})
            return attrs

        def create(self, validated_data):
            user = BaseUser.objects.get(phone=validated_data.get('phone'))
            user.set_password(validated_data.get('new_password'))
            user.save()
            return user

    @extend_schema(summary='validate otp code and recovery password', tags=['user'], request=InputOtpSerializer())
    def post(self, request):
        serializer = self.InputOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)
