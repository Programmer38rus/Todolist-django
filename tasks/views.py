from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from tasks.models import TodoItem, Category, Priority
# from django.views.decorators.cache import cache_page
from django.core.cache import cache
from collections import Counter
from django.db.models import Count
import datetime


def index(request):
    if not cache.get('date_open'):
        cache.set('date_open', datetime.datetime.now().ctime(), 10)

    # 1st version
    # counts = {t.name: random.randint(1, 100) for t in Tag.objects.all()}

    # 2nd version
    # counts = {t.name: t.taggit_taggeditem_items.count()
    # for t in Tag.objects.all()}

    # 3rd version
    # from django.db.models import Count
    #
    # counts = Category.objects.annotate(total_tasks=Count(
    #     'todoitem')).order_by("-total_tasks")
    # counts = {c.name: c.total_tasks for c in counts}
    #
    # return render(request, "tasks/index.html", {"counts": counts, 'cache': cache.get('date_open')})

    # 4rd version
    # category = Category.objects.all().select_related()
    # priority = Priority.objects.all().select_related()

    list_todo = []
    list_priority = []
    dict_cat = {}
    dict_priority = {}

    try:
        todoitems = TodoItem.objects.filter(owner=request.user).select_related()
        category = Category.objects.all().select_related()
        priority = Priority.objects.all().select_related()

        for item in todoitems:
            list_todo.append(TodoItem.category.through.objects.filter(todoitem_id=item.id).prefetch_related()[0])
            list_priority.append(item)

        for cat in category:
            dict_cat[cat] = 0
            for i in list_todo:
                if cat.id == i.category_id:
                    dict_cat[cat] += 1
        for pri in priority:
            dict_priority[pri] = 0
            for task in list_priority:
                if pri.id == task.priority.id:
                    dict_priority[pri] += 1
    except:
        pass

    # for dic, value in dict.items():
    #     print(dic.name, value)
    # for i in todo_category:
    #     print(i.category.id)
    return render(request, "tasks/index.html", {"category": dict_cat, "priority": dict_priority, "cache": cache.get('date_open')})
    # return render(request, "tasks/index.html" )


def filter_tasks(tags_by_task):
    return set(sum(tags_by_task, []))


def tasks_by_cat(request, cat_slug=None):
    u = request.user
    tasks = TodoItem.objects.filter(owner=u).all()

    cat = None
    if cat_slug:
        cat = get_object_or_404(Category, slug=cat_slug)
        tasks = tasks.filter(category__in=[cat])

    categories = []
    for t in tasks:
        for cat in t.category.all():
            if cat not in categories:
                categories.append(cat)
    return render(
        request,
        "tasks/list_by_cat.html",
        {"category": cat, "tasks": tasks, "categories": categories},
    )


class TaskListView(ListView):
    if not cache.get('date_open'):
        cache.set('date_open', datetime.datetime.now().ctime(), 10)

    model = TodoItem
    context_object_name = "tasks"
    template_name = "tasks/list.html"

    def get_queryset(self):
        u = self.request.user
        qs = super().get_queryset()
        return qs.filter(owner=u)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_tasks = self.get_queryset()

        categories = Category.objects.all()

        query_list = []
        for task in user_tasks:
            for cat in task.category.through.objects.all().order_by('id'):
                query_list.append(cat)
            break

        context['trough'] = query_list
        context['cache'] = cache.get('date_open')
        context['categories'] = categories

        return context


class TaskDetailsView(DetailView):
    model = TodoItem
    template_name = "tasks/details.html"
