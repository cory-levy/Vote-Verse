from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from friendship.models import FriendshipRequest

from .models import VoteUser, School, Question, Vote, Choice, Profile


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ["id", "name"]


class VoteUserSerializer(serializers.ModelSerializer):
    school = SchoolSerializer()

    class Meta:
        model = VoteUser
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "date_of_birth",
            "school",
        ]


class ProfileSerializer(serializers.ModelSerializer):
    user = VoteUserSerializer()

    class Meta:
        model = Profile
        fields = ["id", "user", "show_name"]


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ["id", "name"]


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = ["id", "name", "description", "choices", "created"]


class VoteSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()
    choice = ChoiceSerializer()
    user = VoteUserSerializer()

    class Meta:
        model = Vote
        fields = ["id", "question", "choice", "user", "created"]


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        write_only=True,
        required=True,
        validators=[UniqueValidator(queryset=VoteUser.objects.all())],
    )
    email = serializers.EmailField(
        write_only=True,
        required=True,
        validators=[UniqueValidator(queryset=VoteUser.objects.all())],
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    date_of_birth = serializers.DateField(write_only=True, required=True)
    school = serializers.PrimaryKeyRelatedField(
        write_only=True, required=True, queryset=School.objects.all()
    )

    class Meta:
        model = VoteUser
        fields = [
            "username",
            "email",
            "password",
            "password2",
            "first_name",
            "last_name",
            "date_of_birth",
            "school",
        ]
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data):
        user = VoteUser(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            date_of_birth=validated_data["date_of_birth"],
            school=validated_data["school"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user

    def to_representation(self, instance):
        return VoteUserSerializer(instance=instance).data


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = VoteUser
        fields = ("old_password", "password", "password2")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct"}
            )

        return value

    def update(self, instance, validated_data):
        user = self.context["request"].user

        if user.pk != instance.pk:
            raise serializers.ValidationError(
                {"authorize": "You dont have permission for this user."}
            )

        instance.set_password(validated_data["password"])
        instance.save()

        return instance


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username", "email"]


class FriendshipRequestSerializer(serializers.ModelSerializer):
    to_user = serializers.CharField()
    from_user = serializers.StringRelatedField()

    class Meta:
        model = FriendshipRequest
        fields = (
            "id",
            "from_user",
            "to_user",
            "message",
            "created",
            "rejected",
            "viewed",
        )
        extra_kwargs = {
            "from_user": {"read_only": True},
            "created": {"read_only": True},
            "rejected": {"read_only": True},
            "viewed": {"read_only": True},
        }


class FriendshipRequestResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendshipRequest
        fields = [
            "id",
        ]
