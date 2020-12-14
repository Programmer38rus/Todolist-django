from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Category(models.Model):
    slug = models.CharField(max_length=128)
    name = models.CharField(max_length=256)
    todos_count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name} ({self.slug})'

    def get_absolute_url(self):
        return reverse("tasks:list_by_cat", args=[self.slug])


class Priority(models.Model):
    name = models.CharField(max_length=256)
    priority_count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Приоритет'
        verbose_name_plural = 'Приоритеты'

    def __str__(self):
        return self.name


class TodoItem(models.Model):
    # PRIORITY_HIGH = 1
    # PRIORITY_MEDIUM = 2
    # PRIORITY_LOW = 3
    #
    # PRIORITY_CHOICES = [
    #     (PRIORITY_HIGH, "Высокий приоритет"),
    #     (PRIORITY_MEDIUM, "Средний приоритет"),
    #     (PRIORITY_LOW, "Низкий приоритет"),
    # ]
    description = models.TextField("описание")
    is_completed = models.BooleanField("выполнено", default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    # priority = models.IntegerField(
    #     "Приоритет", choices=PRIORITY_CHOICES, default=PRIORITY_MEDIUM
    # )
    priority = models.ForeignKey(Priority,
                                 on_delete=models.DO_NOTHING, related_name="priority",
                                 default=Priority.objects.filter(name="Средний приоритет").first()
                                 )

    category = models.ManyToManyField(Category, blank=True)

    class Meta:
        verbose_name_plural = "Задачи"

    def priority_counter():
        for i in Priority.objects.all():
            i.priority_count = TodoItem.objects.filter(priority=i.id).count()
            i.save()

    def __str__(self):
        return self.description.lower()

    def get_absolute_url(self):
        return reverse("tasks:details", args=[self.pk])
