from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import get_user_model
        
from task_manager.models import Task
from task_manager.forms import TaskForm, WorkerCreationForm

class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "task_manager/task_list.html"
    context_object_name = "task_list"
    paginate_by = 10

    def get_queryset(self):
        #  We can implement filtering or searching by task name
        queryset = Task.objects.select_related().prefetch_related("assignees", "tags")
        query = self.request.GET.get("name")
        if query:
            return queryset.filter(name__icontains=query)
        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    template_name = "task_manager/task_detail.html"


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task_manager:task-list")
    template_name = "task_manager/task_confirm_delete.html"
    

class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = "task_manager/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # We collect basic analytics for display on the main page
        # Number of tasks and number of active tasks
        context["num_tasks"] = Task.objects.count()
        context["num_active_tasks"] = Task.objects.filter(is_completed=False).count()
        # We extract the number of employees from the custom Worker
        Worker = get_user_model()
        context["num_workers"] = Worker.objects.count()
        return context

class WorkerCreateView(generic.CreateView):
    # Presentation for registration of new employees on the website
    form_class = WorkerCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")