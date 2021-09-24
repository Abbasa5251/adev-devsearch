from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from .utils import searchProjects, paginateProjects


def projects(request):
    projects, search = searchProjects(request)
    custom_range, projects = paginateProjects(request, projects, 6)
    context = {
        "projects": projects,
        "search": search,
        "custom_range": custom_range,
    }
    return render(request, "projects/projects.html", context)


def project(request, id):
    project = Project.objects.get(id=id)
    form = ReviewForm()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = project
        review.owner = request.user.profile
        review.save()
        project.get_vote_count
        messages.success(request, "Your review was successfully submitted")
        return redirect("projects:project", id=project.id)
    context = {"project": project, "form": form}
    return render(request, "projects/single-project.html", context)


@login_required(login_url="users:login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm
    if request.method == "POST":
        newtags = request.POST.get("newtags").split()
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            for tag in newtags:
                tag, _ = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect("users:account")

    context = {"form": form}
    return render(request, "projects/project_form.html", context)


@login_required(login_url="users:login")
def updateProject(request, id):
    profile = request.user.profile
    project = profile.project_set.get(id=id)
    form = ProjectForm(instance=project)
    if request.method == "POST":
        newtags = request.POST.get("newtags").split()
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for tag in newtags:
                tag, _ = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect("users:account")

    context = {"form": form, "project": project}
    return render(request, "projects/project_form.html", context)


@login_required(login_url="users:login")
def deleteProject(request, id):
    profile = request.user.profile
    project = profile.project_set.get(id=id)

    if request.method == "POST":
        project.delete()
        return redirect("projects:projects")

    context = {"object": project}
    return render(request, "delete_template.html", context)
