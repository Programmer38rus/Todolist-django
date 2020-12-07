from django.db.models.signals import m2m_changed, pre_delete, post_save
from django.dispatch import receiver
from tasks.models import TodoItem, Category
from collections import Counter


@receiver(m2m_changed, sender=TodoItem.category.through)
def task_cats_added(sender, instance, action, model, **kwargs):
    print(action)
    if action != 'post_add':

        return

    for cat in instance.category.all():
        slug = cat.slug
        new_count = 0
        print(cat.todos_count)
        for task in TodoItem.objects.all():
            new_count += task.category.filter(slug=slug).count()

        Category.objects.filter(slug=slug).update(todos_count=new_count)

@receiver(m2m_changed, sender=TodoItem.category.through)
def task_cats_removed(sender, instance, action, model, **kwargs):
    if action != "post_remove":
        return

    # cat_counter = Counter()
    # for t in TodoItem.objects.all():
    #     for cat in t.category.all():
    #         cat_counter[cat.slug] += 1
    #         print(cat.slug)
    #         for category in Category.objects.all():
    #             if category.slug not in cat_counter:
    #                 cat_counter[category.slug] = 0
    # for slug, new_count in cat_counter.items():
    #     Category.objects.filter(slug=slug).update(todos_count=new_count)
    for t in TodoItem.objects.all():
        for cat in t.category.all():
            print(cat)
@receiver(pre_delete, sender=TodoItem)
def task_delete(sender, instance, **kwargs):

    print(f"{sender} - {instance} -  - {kwargs}")

@receiver(post_save, sender=TodoItem)
def task_save(sender, instance, **kwargs):

    sender.priority_counter()
