import uuid
from django.db import models


class Job(models.Model):
    class Status(models.TextChoices):
        WISHLIST = "wishlist", "Wishlist"
        APPLIED = "applied", "Applied"
        INTERVIEW = "interview", "Interview"
        OFFER = "offer", "Offer"
        REJECTED = "rejected", "Rejected"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location_type = models.CharField(
        max_length=10,
        choices=[
            ("remote", "remote"),
            ("hybrid", "hybrid"),
            ("onsite", "onsite"),
        ],
        blank=True
    )
    location = models.CharField(max_length=200, blank=True)
    salary_min = models.IntegerField(null=True, blank=True)
    salary_max = models.IntegerField(null=True, blank=True)
    currency = models.CharField(max_length=8, blank=True)
    source = models.CharField(max_length=50, blank=True)
    url = models.URLField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.WISHLIST
    )
    applied_at = models.DateField(null=True, blank=True)
    next_action_at = models.DateField(null=True, blank=True)
    tags_csv = models.TextField(blank=True, help_text="Comma-separated tags")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def tags(self):
        return [t.strip() for t in self.tags_csv.split(",") if t.strip()]


class Note(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job = models.ForeignKey(
        Job,
        related_name="notes",
        on_delete=models.CASCADE
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
