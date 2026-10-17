from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class ServiceRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        RESOLVED = "RESOLVED", "Resolved"

    citizen = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="requests",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="requests",
    )
    location = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="request_images/", blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"#{self.pk} {self.category} - {self.location}"

    @property
    def status_badge_class(self):
        """Bootstrap colour classes for showing the status as a badge."""
        return {
            self.Status.PENDING: "bg-warning text-dark",
            self.Status.IN_PROGRESS: "bg-primary",
            self.Status.RESOLVED: "bg-success",
        }.get(self.status, "bg-secondary")