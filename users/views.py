from django.http import request
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from django.contrib.auth.models import User
from .models import Profile, Message
from .utils import searchProfiles, paginateProfiles


def loginUser(request):
    page = "login"
    context = {"page": page}
    if request.user.is_authenticated:
        return redirect("users:profiles")
    if request.method == "POST":
        username = request.POST["username"].lower()
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # return redirect(
            #     request.GET["next"] if "next" in request.GET else "users:account"
            # )
            return redirect(request.GET.get("next", "users:account"))
        else:
            messages.error(request, "Username or password is incorrect")

    return render(request, "users/login_register.html", context)


def logoutUser(request):
    logout(request)
    messages.info(request, "User was logged out")
    return redirect("users:login")


def registerUser(request):
    page = "register"
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, "User account was created")
            login(request, user)
            return redirect("users:edit-account")
        else:
            messages.error(request, "An error has occured during registration")

    context = {"page": page, "form": form}
    return render(request, "users/login_register.html", context)


def profiles(request):
    profiles, search = searchProfiles(request)
    custom_range, profiles = paginateProfiles(request, profiles, 3)
    context = {"profiles": profiles, "search": search, "custom_range": custom_range}
    return render(request, "users/profiles.html", context)


def userProfile(request, id):
    profile = Profile.objects.get(id=id)
    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")
    context = {"profile": profile, "topSkills": topSkills, "otherSkills": otherSkills}
    return render(request, "users/user-profile.html", context)


@login_required(login_url="users:login")
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    context = {"profile": profile, "skills": skills, "projects": projects}
    return render(request, "users/account.html", context)


@login_required(login_url="users:login")
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("users:account")

    context = {"form": form}
    return render(request, "users/profile_form.html", context)


@login_required(login_url="users:login")
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, "Skill added successfully")
            return redirect("users:account")

    context = {"form": form}
    return render(request, "users/skill_form.html", context)


@login_required(login_url="users:login")
def updateSkill(request, id):
    profile = request.user.profile
    skill = profile.skill_set.get(id=id)
    form = SkillForm(instance=skill)
    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill updated successfully")
            return redirect("users:account")

    context = {"form": form}
    return render(request, "users/skill_form.html", context)


@login_required(login_url="users:login")
def deleteSkill(request, id):
    profile = request.user.profile
    skill = profile.skill_set.get(id=id)
    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill deleted successfully")
        return redirect("users:account")
    context = {"object": skill}
    return render(request, "delete_template.html", context)


@login_required(login_url="users:login")
def inbox(request):
    profile = request.user.profile
    message_request = profile.messages.all()
    unread_count = message_request.filter(is_read=False).count()
    context = {"message_request": message_request, "unread_count": unread_count}
    return render(request, "users/inbox.html", context)


@login_required(login_url="users:login")
def viewMessage(request, id):
    profile = request.user.profile
    message = profile.messages.get(id=id)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {"message": message}
    return render(request, "users/message.html", context)


# @login_required(login_url="users:login")
def createMessage(request, id):
    recipient = Profile.objects.get(id=id)
    form = MessageForm()
    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()
            messages.success(request, "Your message was successfully sent!")
            return redirect("users:user-profile", recipient.id)

    context = {"recipient": recipient, "form": form}
    return render(request, "users/message_form.html", context)
