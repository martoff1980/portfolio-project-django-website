from django.contrib.auth.models import AbstractUser
from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
        related_name="workers"
    )

    def __str__(self) -> str:
        return (
            f"{self.username} "
            f"({self.position if self.position else 'No position'})"
        )


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    # Members of the team (Many-to-Many with Worker)
    members = models.ManyToManyField(Worker, related_name="teams")

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    # За каждым проектом закреплена одна команда (или наоборот)
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="projects"
    )

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("urgent", "Urgent"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="medium"
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks",
        # null=True,temporary,
        # to avoid errors with old tasks in the database
        null=True,
        blank=False
    )

    # Connection for workers who execising task
    assignees = models.ManyToManyField(Worker, related_name="tasks")
    # Connection for tags (option)
    tags = models.ManyToManyField(Tag, related_name="tasks", blank=True)

    class Meta:
        ordering = ["deadline"]

    def __str__(self) -> str:
        return f"{self.name} (Completed: {self.is_completed})"
