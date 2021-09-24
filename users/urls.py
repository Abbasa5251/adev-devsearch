from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.loginUser, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("register/", views.registerUser, name="register"),
    path("", views.profiles, name="profiles"),
    path("profile/<str:id>/", views.userProfile, name="user-profile"),
    path("account/", views.userAccount, name="account"),
    path("edit-account/", views.editAccount, name="edit-account"),
    path("create-skill/", views.createSkill, name="create-skill"),
    path("update-skill/<str:id>/", views.updateSkill, name="update-skill"),
    path("delete-skill/<str:id>/", views.deleteSkill, name="delete-skill"),
    path("inbox/", views.inbox, name="inbox"),
    path("inbox/<str:id>/", views.viewMessage, name="message"),
    path("create-message/<str:id>/", views.createMessage, name="create-message"),
]
