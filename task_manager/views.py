from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import get_user_model
        
from task_manager.models import Project,Task
from task_manager.forms import TaskForm, WorkerCreationForm

class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "task_manager/task_list.html"
    context_object_name = "task_list"
    paginate_by = 10

    def get_queryset(self):
        #  We can implement filtering or searching by task name
        # queryset = Task.objects.select_related().prefetch_related("assignees", "tags")
        queryset = Task.objects.filter(
            project__team__members=self.request.user
        ).select_related("project").prefetch_related("assignees", "tags")
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
    
class MyTaskListView(LoginRequiredMixin, generic.ListView):
    # Page "My cabinet" with worker's personal tasks 
    model = Task
    template_name = "task_manager/my_task_list.html"
    context_object_name = "my_tasks"

    def get_queryset(self):
        # Only select tasks where the current user is in the list of assignees
        return (
            Task.objects.filter(assignees=self.request.user)
            .prefetch_related("tags")
            .order_by("is_completed", "deadline")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        
        # We separate tasks into two categories 
        # for convenient display in different tables
        context["active_tasks"] = queryset.filter(is_completed=False)
        context["completed_tasks"] = queryset.filter(is_completed=True)
        return context

class ProjectListView(LoginRequiredMixin, generic.ListView):
    # Current user get projects
    model = Project
    template_name = "task_manager/project_list.html"
    context_object_name = "project_list"

    def get_queryset(self):
        # We show only those projects in the teams of which the current user is a member
        return Project.objects.filter(team__members=self.request.user).select_related("team")


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    # A detailed project page with a list of its tasks
    model = Project
    template_name = "task_manager/project_detail.html"

    def get_queryset(self):
        # Protect: you can only access the project page if you are a member of its team
        return Project.objects.filter(team__members=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # We pass to the template all tasks of this project
        context["project_tasks"] = self.object.tasks.prefetch_related("assignees", "tags")
        return context
