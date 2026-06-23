from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from task_manager.models import Position, Worker, Tag, Task


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    # Add field position in users list
    list_display = UserAdmin.list_display + ("position",)
    
    # Add filter by position in the right panel
    list_filter = ["position"]
    
    # Set the fieldsets to include the position field in the user edit form
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info"), {"fields": ("position",)}),
    )

    # Set the add_fieldsets to include the position field 
    # in the user creation form
    add_fieldsets = UserAdmin.add_fieldsets + (
        (("Additional info"), {"fields": ("first_name", "last_name", "email", "position")}),
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    # Fields that will be visible in the list of all tasks
    list_display = ["name", "deadline", "priority", "is_completed"]
    
    # Filter by completion status, priority, deadline, and tags
    list_filter = ["is_completed", "priority", "deadline", "tags"]
    
    # Search by task name and description
    search_fields = ["name", "description"]
    
    # This allows for a better user experience
    # when selecting multiple assignees or tags for a task.
    filter_horizontal = ["assignees", "tags"]