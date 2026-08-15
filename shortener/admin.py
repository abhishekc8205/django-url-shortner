from django.contrib import admin

from .models import ClickEvent, ShortURL


@admin.register(ShortURL)
class ShortURLAdmin(admin.ModelAdmin):
    list_display = ("code", "original_url", "created_at")
    search_fields = ("code", "original_url")


@admin.register(ClickEvent)
class ClickEventAdmin(admin.ModelAdmin):
    list_display = ("short_url", "clicked_at", "referrer")
    list_select_related = ("short_url",)
    readonly_fields = ("short_url", "clicked_at", "referrer", "user_agent")
