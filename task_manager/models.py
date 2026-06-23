from django.contrib.auth.models import AbstractUser
from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = None

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
        return f"{self.username} ({self.position if self.position else 'No position'})"


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

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
    # Connection for workers who execising task
    assignees = models.ManyToManyField(Worker, related_name="tasks")
    # Connection for tags (option)
    tags = models.ManyToManyField(Tag, related_name="tasks", blank=True)

    def __str__(self) -> str:
        return f"{self.name} (Completed: {self.is_completed})"