from django.contrib import admin
from .models import Project, Review, Tag


class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "owner")
    list_filter = ("owner",)
    search_fields = ("title",)
    # prepopulated_fields = {"slug": ("title",)}

    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs
    #     return qs.filter(owner__user=request.user)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("owner", "project", "value")
    list_filter = ("project",)
    search_fields = (
        "project",
        "owner",
    )


class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)


admin.site.register(Project, ProjectAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Tag, TagAdmin)
