from django.contrib import admin

from apps.intranet.models import (
    Chore,
    ChoreAssignment,
    ChoreRating,
    Link,
    Notification,
    RedMerge,
    ShoppingItem,
)


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "url", "order")
    list_editable = ("category", "order")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "level", "published_at", "expires_at")
    list_filter = ("level",)

    def save_model(self, request, obj, form, change):
        if not obj.created_by_id:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(RedMerge)
class RedMergeAdmin(admin.ModelAdmin):
    list_display = ("user", "repo", "merged_on", "note")
    list_filter = ("user", "repo")
    date_hierarchy = "merged_on"


@admin.register(Chore)
class ChoreAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "order")
    list_editable = ("order",)


@admin.register(ChoreAssignment)
class ChoreAssignmentAdmin(admin.ModelAdmin):
    list_display = ("week_start", "chore", "user")
    list_filter = ("chore", "user")


admin.site.register(ChoreRating)
admin.site.register(ShoppingItem)
