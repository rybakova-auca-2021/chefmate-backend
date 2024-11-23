from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from authentication.serializers import (
    RegisterUserSerializer,
    RegisterWithEmailSerializer,
    SendCodeSerializer,
    UserProfileSerializer,
    LogoutSerializer,
    LoginSerializer,
    PasswordResetSerializer,
    PasswordSetSerializer
)
from authentication.models import User
from config import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

import random
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404



class TokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        tags=['Authentication'],
        operation_description="Этот эндпоинт предоставляет "
                              "возможность пользователю "
                              "обновить токен доступа (Access Token) "
                              "с помощью токена обновления (Refresh Token). "
                              "Токен обновления позволяет пользователям "
                              "продлить срок действия своего Access Token без "
                              "необходимости повторной аутентификации.",
    )
    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)


class BaseRegisterView(generics.GenericAPIView):
    serializer_class = None  # Сериализатор будет определен в наследниках

    @swagger_auto_schema(
        tags=['Authentication'],
        operation_description="Этот эндпоинт предоставляет "
                              "возможность пользователям зарегистрироваться "
                              "в системе, предоставив имя пользователя и номер телефона. "
                              "После успешной регистрации, система создает "
                              "новую запись пользователя и возвращает информацию о нем.",
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()

            user_data = serializer.data

            user = User.objects.filter(email=user_data["email"]).first()

            if user is None:
                return Response({"error": "User not found!"}, status.HTTP_404_NOT_FOUND)

            return Response({
                "message": "The user has been successfully created!",
                "user": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class RegisterWithEmailView(BaseRegisterView):
    serializer_class = RegisterWithEmailSerializer

    @swagger_auto_schema(
        tags=['Authentication'],
        operation_description="Этот эндпоинт предоставляет "
                              "возможность пользователям зарегистрироваться "
                              "в системе, предоставив номер телефона. Этот "
                              "эндпоинт предназначен для незарегистрированных "
                              "пользователей, которые пытаются сделать заказ, но "
                              "требуется регистрация для выполнения этой операции. "
                              "После успешной регистрации, система создает новую "
                              "запись пользователя и возвращает информацию о нем, "
                              "включая токены и айди.",
    )
    def post(self, request):
        response = super().post(request)

        if response.status_code == status.HTTP_201_CREATED:
            user_data = response.data.get('user', {})
            user = User.objects.filter(email=user_data.get('email')).first()

            if user:
                default_username = f"username{random.randint(1000, 9999)}"
                user.username = default_username
                user.profile_photo = 'https://i.ibb.co/m8CpW33/profile-pic.jpg'
                user.save()

                refresh = RefreshToken.for_user(user)

                response.data['user_id'] = user.id
                response.data['username'] = user.username
                response.data['profile_photo'] = user.profile_photo
                response.data['access_token'] = str(refresh.access_token)
                response.data['refresh_token'] = str(refresh)

        return response

class RegisterView(BaseRegisterView):
    serializer_class = RegisterUserSerializer

User = get_user_model()

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    @swagger_auto_schema(
        tags=['Authentication'],
        operation_description="Этот эндпоинт предоставляет "
                              "возможность пользователям войти в систему, "
                              "предоставив почту. После успешного ввода "
                              "почты система якобы "
                              "отправит SMS с 4-значным кодом, "
                              "но на самом деле код будет храниться на "
                              "сервере для последующей проверки. После успешной "
                              "отправки почты "
                              "система возвращает айди пользователя. \nКод подтверждения: 1441.",
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.data

            user = User.objects.filter(email=user_data["email"]).first()
            if not user:
                return Response({"error": "User not found!"}, status=status.HTTP_404_NOT_FOUND)

            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "The SMS sent successfully!",
                "user_id": user.id,
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            })

        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    @swagger_auto_schema(
        tags=['Authentication'],
        operation_description="Этот эндпоинт предоставляет возможность пользователям сбросить пароль, "
                              "предоставив почту. После успешного ввода почты система отправляет "
                              "код сброса на почту (или на сервере хранится заранее определенный "
                              "код для последующей проверки). После успешной отправки почты "
                              "система возвращает айди пользователя. \nКод сброса: 1441."
    )
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.data

            user = User.objects.filter(email=user_data["email"]).first()
            if not user:
                return Response({"error": "User not found!"}, status=status.HTTP_404_NOT_FOUND)

            reset_code = "1441"  

            return Response({
                "message": "The reset code has been sent successfully!",
                "user_id": user.id,
                "reset_code": reset_code, 
            })

        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class PasswordSetView(generics.GenericAPIView):
    serializer_class = PasswordSetSerializer

    @swagger_auto_schema(
        tags=['Authentication'],
        operation_description="Этот эндпоинт позволяет пользователям установить новый пароль, "
                              "используя айди пользователя и код сброса (например, 9876). "
                              "После ввода нового пароля и его подтверждения система сохраняет "
                              "новый пароль."
    )
    def post(self, request):
        serializer = PasswordSetSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data

            user = User.objects.filter(id=user_data['user_id']).first()
            if not user:
                return Response({"error": "User not found!"}, status=status.HTTP_404_NOT_FOUND)


            user.password = make_password(user_data['new_password'])
            user.save()

            return Response({
                "message": "Password has been reset successfully!"
            })

        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
class SendCodeView(generics.GenericAPIView):
    serializer_class = SendCodeSerializer

    @swagger_auto_schema(
        tags=['Authentication'],
        operation_description="На этом эндпоинте вы "
                              "должны ввести код, который "
                              "вам якобы приходит на номер телефона. "
                              "Однако, на самом деле, код подтверждения "
                              "будет заранее храниться на сервере (код=1441). "
                              "После успешного ввода 4-значного кода "
                              "система генерирует Access Token и Refresh "
                              "Token для пользователя, которые можно использовать "
                              "для доступа к защищенным ресурсам. \nСрок действия 'access' токена - "
                              "60 минут, а refresh токена - 30 дней.",
    )
    def post(self, request, user_id):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data.get('code')

        user = User.objects.filter(pk=user_id).first()

        if user is None:
            return Response({"error": "User not found!"}, status=status.HTTP_404_NOT_FOUND)

        refresh = RefreshToken.for_user(user)

        if code == settings.CONFIRMATION_CODE:
            return Response({
                "message": "Success!",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=200)

        return Response({"error": "Invalid or already confirmed code."}, status=400)


class UserMeView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer

    @swagger_auto_schema(
        tags=['Authentication'],
        operation_description="Этот эндпоинт предоставляет возможность получить информацию о пользователе по его ID.",
    )
    def get(self, request, user_id, *args, **kwargs):
        user = get_object_or_404(User, id=user_id)
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class UserProfileUpdateView(generics.GenericAPIView):
    serializer_class = UserProfileSerializer

    @swagger_auto_schema(
        tags=['Authentication'],
        operation_description="Этот эндпоинт позволяет пользователям "
                              "обновить свой профиль по ID пользователя. "
                              "Пользователь должен быть аутентифицирован для доступа к этому "
                              "эндпоинту. Если данные пользователя проходят "
                              "валидацию, профиль будет обновлен."
    )
    def put(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        
        serializer = UserProfileSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User updated successfully!'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Authentication'],
        operation_description="Этот эндпоинт предоставляет "
                              "возможность пользователю выйти "
                              "из системы. Пользователь должен быть "
                              "аутентифицирован для доступа к этому "
                              "эндпоинту. При отправке запроса на выход "
                              "из системы, система аннулирует текущий Refresh "
                              "Token пользователя, что означает, что пользователь "
                              "больше не сможет использовать его для получения новых "
                              "Access Token. Пользователь будет вынужден повторно "
                              "войти в систему.",
    )
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data["refresh_token"]

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "You have successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Unable to log out."}, status=status.HTTP_400_BAD_REQUEST)

