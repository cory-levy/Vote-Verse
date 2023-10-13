from django.urls import path

from .views import (
    RegisterView,
    ChangePasswordView,
    RetrieveProfileView,
    ListVoteView,
    RetrieveVoteView,
    ListChoiceView,
    RetrieveChoiceView,
    ListQuestionView,
    RetrieveQuestionView,
    CreateQuesitonView,
    CreateChoiceView,
    CreateVoteView,
    CreateSchoolView,
    ListSchoolView,
    RetrieveSchoolView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="auth_register"),
    path("password/change/", ChangePasswordView.as_view(), name="change-password"),
    path("profile/<int:pk>/", RetrieveProfileView.as_view(), name="get-profile"),
    path("vote/", ListVoteView.as_view(), name="list-vote"),
    path("vote/<int:pk>/", RetrieveVoteView.as_view(), name="get-vote"),
    path("vote/create/", CreateVoteView.as_view(), name="create-vote"),
    path("choice/", ListChoiceView.as_view(), name="list-choice"),
    path("choice/<int:pk>/", RetrieveChoiceView.as_view(), name="get-choice"),
    path("choice/crteate/", CreateChoiceView.as_view(), name="create-choice"),
    path("question/", ListQuestionView.as_view(), name="list-question"),
    path("question/<int:pk>/", RetrieveQuestionView.as_view(), name="get-question"),
    path("question/create/", CreateQuesitonView.as_view(), name="create-question"),
    path("school/", ListSchoolView.as_view(), name="list-school"),
    path("school/<int:pk>/", RetrieveSchoolView.as_view(), name="get-school"),
    path("school/create/", CreateSchoolView.as_view(), name="create-school"),
]
