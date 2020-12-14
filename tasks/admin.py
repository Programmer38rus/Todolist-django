from django.contrib import admin

from tasks.models import (
    TodoItem,
    Category,
    Priority,
)


@admin.register(TodoItem)
class TodoItemAdmin(admin.ModelAdmin):
    list_display = ('description', 'is_completed', 'created')

    # Сохраняет пользователя автоматически
    # exclude = ('owner',)
    # def save_model(self, request, obj, form, change):
    #     if not obj.pk:
    #         print(obj)
    #         obj.owner = request.user
    #
    #     super().save_model(request, obj, form, change)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name')


@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    pass
