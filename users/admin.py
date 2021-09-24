from django.contrib import admin
from .models import Profile, Skill, Message


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("username", "name", "email", "location")
    ordering = ("-created",)


class SkillAdmin(admin.ModelAdmin):
    list_display = ("name",)
    ordering = ("-created",)


class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "name", "subject")
    ordering = ("-created",)


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(Message, MessageAdmin)
