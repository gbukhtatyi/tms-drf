from django.contrib import admin
from .models import Event
from django.core.cache import cache

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["name", "short_description", "meeting_time"]
    search_fields = ["name", "description"]
    date_hierarchy = "meeting_time"

    @admin.display(description="Описание")
    def short_description(self, obj: Event) -> str:
        return obj.description[:50] + "..." if len(obj.description) > 50 else obj.description

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        cache.clear()

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        cache.clear()