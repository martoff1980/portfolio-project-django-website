from django.urls import path

from task_manager.views import (
    IndexView,
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    WorkerCreateView,
    MyTaskListView,
    ProjectListView,
    ProjectDetailView
)

app_name = "task_manager"

urlpatterns = [
    # Main page
    path("", IndexView.as_view(), name="index"),

    # Tasks (CRUD)
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path(
        "tasks/<int:pk>/update/",
        TaskUpdateView.as_view(),
        name="task-update"
        ),
    path(
        "tasks/<int:pk>/delete/",
        TaskDeleteView.as_view(),
        name="task-delete"
        ),
    path("workers/create/", WorkerCreateView.as_view(), name="worker-create"),
    path("my-tasks/", MyTaskListView.as_view(), name="my-tasks"),
    path("projects/", ProjectListView.as_view(), name="project-list"),
    path(
        "projects/<int:pk>/",
        ProjectDetailView.as_view(),
        name="project-detail"
        ),
]
