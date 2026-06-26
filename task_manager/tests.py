from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from task_manager.models import Position, Project, Task, Team


class ModelTests(TestCase):
    # Testing the correctness of model creation and
    # their string representation.
    def test_position_str(self) -> None:
        position = Position.objects.create(name="Python Developer")
        self.assertEqual(str(position), "Python Developer")

    def test_worker_str(self) -> None:
        position = Position.objects.create(name="QA Engineer")
        worker = get_user_model().objects.create_user(
            username="test_user",
            password="password123",
            position=position
        )
        self.assertEqual(str(worker), "test_user (QA Engineer)")


class ViewTests(TestCase):
    # Testing the views, authentication, and business logic.
    def setUp(self) -> None:
        # Create a position,
        # a worker, a team,
        # a project,
        # a task for testing.
        self.position = Position.objects.create(name="Manager")
        self.worker = get_user_model().objects.create_user(
            username="manager_jack",
            password="securepassword",
            position=self.position
        )
        self.team = Team.objects.create(name="Alpha Team")
        self.team.members.add(self.worker)

        self.project = Project.objects.create(
            name="E-Commerce",
            team=self.team
        )

        self.task = Task.objects.create(
            name="Write Documentation",
            description="Fix README and draw diagrams",
            deadline=timezone.now() + timezone.timedelta(days=2),
            priority="medium",
            project=self.project
        )
        self.task.assignees.add(self.worker)

    def test_dashboard_requires_login(self) -> None:
        # Check that the main page requires login and redirects
        # to the login page for unauthenticated users.
        response = self.client.get(reverse("task_manager:index"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_dashboard_accessible_with_login(self) -> None:
        # Check that the main page is accessible after logging in and
        # that the correct template is used.
        self.client.login(username="manager_jack", password="securepassword")
        response = self.client.get(reverse("task_manager:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "task_manager/index.html")
        # Check that the statistics in the context are calculated correctly
        self.assertEqual(response.context["num_tasks"], 1)
        self.assertEqual(response.context["num_workers"], 1)

    def test_task_list_isolation(self) -> None:
        # Create another team,
        # project,
        # task that our user has no relation to
        other_team = Team.objects.create(name="Beta Team")
        other_project = Project.objects.create(
            name="Mobile App",
            team=other_team
        )
        Task.objects.create(
            name="Secret QA Task",
            description="For Beta Team only",
            deadline=timezone.now() + timezone.timedelta(days=1),
            project=other_project
        )

        self.client.login(username="manager_jack", password="securepassword")
        response = self.client.get(reverse("task_manager:task-list"))

        self.assertEqual(response.status_code, 200)
        # Our task should be in the list
        self.assertContains(response, "Write Documentation")
        # The foreign task should NOT be in the list
        self.assertNotContains(response, "Secret QA Task")

    def test_toggle_task_status(self) -> None:
        # Testing the toggle functionality of a task's status
        # from "In Progress" to "Completed" and back.
        self.client.login(username="manager_jack", password="securepassword")

        # Default status should be False (In Progress)
        self.assertFalse(self.task.is_completed)

        # Send a POST request to toggle the task status
        detail_url = reverse(
            "task_manager:task-detail",
            kwargs={"pk": self.task.id}
        )
        toggle_url = reverse(
            "task_manager:toggle-task-status",
            kwargs={"pk": self.task.id}
        )
        # Send a POST request to toggle the task status,
        # explicitly passing the HTTP_REFERER header
        response = self.client.post(toggle_url, HTTP_REFERER=detail_url)

        # Check that the response is a redirect to the task detail page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, detail_url)

        # Check that the response is a redirect after toggling the status
        self.assertEqual(response.status_code, 302)

        # Refresh the task object from the database to get the updated status
        self.task.refresh_from_db()

        # Now the status should be True (Completed)
        self.assertTrue(self.task.is_completed)

        # Send another POST request to toggle the status back (False)
        response = self.client.post(toggle_url, HTTP_REFERER=detail_url)
        self.assertRedirects(response, detail_url)

        self.task.refresh_from_db()
        self.assertFalse(self.task.is_completed)
