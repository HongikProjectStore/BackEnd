from base64 import urlsafe_b64encode
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, DjangoUnicodeDecodeError

from .models import User, GENDER

class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        help_text="닉네임(Unique)",
        required = True,
        validators =[UniqueValidator(queryset=User.objects.all())],
    )
    email = serializers.EmailField(
        help_text="이메일(Unique)",
        required = True,
        validators =[UniqueValidator(queryset=User.objects.all())],
    )
    password = serializers.CharField(
        help_text="비밀번호",
        write_only=True,
        required = True,
        validators=[validate_password],
    )
    password2 = serializers.CharField(
        help_text="비밀번호 재입력",
        write_only = True, 
        required=True
    )

    birth = serializers.DateField(
        help_text="생년월일",
        required =True
    )

    gender = serializers.ChoiceField(
        help_text="성별",
        choices=GENDER,
        required =True,
    )


    class Meta:
        model = User
        fields = ('username','email','password','password2','birth','gender')

    def validate(self, data):
        username = data['username']
        if not username.isalnum():
            raise serializers.ValidationError(
                {"username" : "Username should only contain alphanumeric characters."}
            )
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password" : "Password fields didn't match."}
            )
        return data


    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            email=validated_data['email'],
            password = validated_data['password'],
            birth=validated_data['birth'],
            gender = validated_data['gender']
        )
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user:
            token = TokenObtainPairSerializer.get_token(user)
            return token
        raise serializers.ValidationError(
            {"error" : "Unable to log in with provided credentials."}
        )

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(help_text="access token")

    class Meta:
        model = User
        fields = ['token']

# class RequestPasswordResetEmailSerializer(serializers.Serializer):
#     email = serializers.EmailField()

#     class Meta:
#         fields = ['email']

#     def validate(self, data):
#         email = data['email']
#         if User.objects.filter(email=email).exists():
#             user = User.objects.get(email=email)
#             uidb64 = urlsafe_b64encode(user.id)
#             token = PasswordResetTokenGenerator().make_token(user)


#         return data

class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(
        help_text="기존 비밀번호",
        write_only = True, 
        required=True
    )
    password = serializers.CharField(
        help_text="새로운 비밀번호",
        write_only=True,
        required = True,
        validators=[validate_password],
    )
    password2 = serializers.CharField(
        help_text="새로운 비밀번호 재입력",
        write_only = True, 
        required=True
    )
    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password" : "Password fields didn't match."}
            )
        return data


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token' : ('Token is expired or invalid.')
    }

    def validate(self, data):
        self.token = data['refresh']
        return data

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')
    

class ProfileSerializer(serializers.ModelSerializer):
    gender = serializers.SerializerMethodField()    # 조심할 것

    class Meta:
        model = User
        fields = ("pk", "username","email","created_at","gender","birth","image") 

    def get_gender(self,obj):
        return obj.get_gender_display()


class ProfileUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(help_text="닉네임(Unique)", 
        validators =[UniqueValidator(queryset=User.objects.all())], required=False)
    gender = serializers.CharField(help_text="성별", required = False)
    birth = serializers.DateField(help_text="생년월일", required = False)
    image = serializers.ImageField(help_text="image 파일", required = False)

    class Meta:
        model = User
        fields = ("username", "birth", "gender", "image")
