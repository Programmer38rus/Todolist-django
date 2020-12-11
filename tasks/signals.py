from django.db.models.signals import m2m_changed, post_delete, post_save, pre_delete
from django.dispatch import receiver
from tasks.models import TodoItem, Category
from collections import Counter


@receiver(m2m_changed, sender=TodoItem.category.through)
def task_cats_added(sender, instance, action, model, **kwargs):
    print(action)
    if action != 'post_add':
        return

    todo_by_cat = instance.category.through.objects.filter(todoitem_id=instance.id).prefetch_related()
    category = Category.objects.all().select_related()

    for cat_id in todo_by_cat:
        for cat in category:
            if cat.id == cat_id.category_id:
                cat.todos_count += 1

            cat.save()

    #
    # for cat in instance.category.all():
    #     slug = cat.slug
    #     new_count = 0
    #     for task in TodoItem.objects.all():
    #         new_count += task.category.filter(slug=slug).count()
    #
    #     Category.objects.filter(slug=slug).update(todos_count=new_count)
    TodoItem.priority_counter()


@receiver(m2m_changed, sender=TodoItem.category.through)
def task_cats_removed(sender, instance, action, model, **kwargs):
    if action != "post_remove":
        return

    cat_counter = Counter()
    for t in TodoItem.objects.all():
        for cat in t.category.all():
            cat_counter[cat.slug] += 1
            for category in Category.objects.all():
                if category.slug not in cat_counter:
                    cat_counter[category.slug] = 0
    for slug, new_count in cat_counter.items():
        Category.objects.filter(slug=slug).update(todos_count=new_count)

    TodoItem.priority_counter()


@receiver(pre_delete, sender=TodoItem)
def task_delete(sender, instance, **kwargs):
    print(instance.id)

    todo_by_cat = TodoItem.category.through.objects.filter(todoitem_id=instance.id).prefetch_related()
    print(todo_by_cat)
    category = Category.objects.all().select_related()

    for cat_id in todo_by_cat:
        for cat in category:
            if cat.id == cat_id.category_id:
                cat.todos_count -= 1

            cat.save()


@receiver(post_delete, sender=TodoItem)
def post_task_delete(sender, instance, **kwargs):
    sender.priority_counter()


@receiver(post_save, sender=TodoItem)
def task_save(sender, instance, **kwargs):
    sender.priority_counter()
