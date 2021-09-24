from .models import Project, Tag
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginateProjects(request, projects, results):
    page = request.GET.get("page", 1)
    paginator = Paginator(projects, results)
    try:

        projects = paginator.page(page)

    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)

    left_index = int(page) - 4
    if left_index < 1:
        left_index = 1

    right_index = int(page) + 5
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    custom_range = range(left_index, right_index)
    return custom_range, projects


def searchProjects(request):
    search = request.GET.get("search", "")
    # if request.GET.get('search'):
    #     search = request.GET.get('search')
    tags = Tag.objects.filter(name__icontains=search)
    projects = Project.objects.distinct().filter(
        Q(title__icontains=search)
        | Q(description__icontains=search)
        | Q(owner__name__icontains=search)
        | Q(tags__in=tags)
    )
    return projects, search
