# used to generate globally unique IDs instead of auto‑increment integers.
from uuid import uuid4
# Django ORM field and model classes.
from django.db import models
# runtime validation helpers for numbers/URLs.
from django.core.validators import MinValueValidator, URLValidator
# returns your active User model (works with custom auth later).
from django.contrib.auth import get_user_model


User = get_user_model()


# Choices for job location types, job statuses, and sources.
# These are used to ensure consistency in the values stored in the database.
class LocationType(models.TextChoices):
    # Represents different types of job locations.
    REMOTE = "remote", "Remote"
    HYBRID = "hybrid", "Hybrid"
    ONSITE = "onsite", "On‑site"


class JobStatus(models.TextChoices):
    WISHLIST = "wishlist", "Wishlist"
    APPLIED = "applied", "Applied"
    INTERVIEW = "interview", "Interview"
    OFFER = "offer", "Offer"
    REJECTED = "rejected", "Rejected"


class Source(models.TextChoices):
    LINKEDIN = "LinkedIn", "LinkedIn"
    INDEED = "Indeed", "Indeed"
    OTHER = "Other", "Other"


# Model representing a tag that can be associated with jobs.
# Tags can be used to categorize or label jobs for easier filtering
# and searching.
class Tag(models.Model):
    # Each tag has a unique identifier and a name.
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# Job model (the core entity)
class Job(models.Model):
    # Each job has a unique identifier, an owner (the user who created it),
    # a title, company, location type, and other relevant fields.
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    # The owner of the job, which is a foreign key to the User model.
    # This allows for associating jobs with specific users.
    owner = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,  # delete all related jobs if the user
        # is deleted.
        related_name="jobs"  # gives you user.jobs.all()
    )

    title = models.CharField(max_length=200)
    company = models.CharField(max_length=150)

    # Location type is a choice field that can be remote, hybrid, or on-site.
    location_type = models.CharField(
        max_length=10,
        choices=LocationType.choices,
        default=LocationType.REMOTE
    )
    # Location is a free-text field for the job's location.
    location = models.CharField(max_length=150, blank=True)
    # Salary fields are optional and can be used to store minimum and maximum
    # salary values for the job. They are positive integers with a minimum
    # value of 0
    salary_min = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0)
        ]
    )
    salary_max = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    # stores ISO 4217 codes like “EUR”, “USD”
    currency = models.CharField(max_length=3, default="EUR")  # ISO 4217 code
    # Where you found it (LinkedIn/Indeed/Other)
    source = models.CharField(
        max_length=20,
        choices=Source.choices,
        default=Source.OTHER
    )
    # URL to the job posting, which can be blank if not applicable.
    # It uses a URL validator to ensure the format is correct.
    url = models.URLField(
        max_length=500,
        blank=True,
        validators=[URLValidator()]
    )

    status = models.CharField(
        max_length=12,
        choices=JobStatus.choices,
        default=JobStatus.WISHLIST
    )
    # Pipeline tracking. applied_at is when you applied
    applied_at = models.DateField(null=True, blank=True)
    # your follow‑up/reminder date
    next_action_at = models.DateField(null=True, blank=True)
    # Automatic timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Many-to-many relationship with tags.
    # This allows a job to have multiple tags and a tag to be associated with
    tags = models.ManyToManyField(Tag, blank=True, related_name="jobs")

    # Meta options
    class Meta:
        # Default ordering is by creation date, newest first.
        ordering = ["-created_at"]
        # Indexes for faster querying.
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["company"]),
            models.Index(fields=["location_type"]),
        ]

    # Cross‑field validation
    # Ensure logical salary ranges
    def clean(self):
        super().clean()
        if self.salary_min is not None and self.salary_max is not None:
            if self.salary_min > self.salary_max:
                from django.core.exceptions import ValidationError
                raise ValidationError({
                    "salary_min": (
                        "salary_min cannot be greater than salary_max."
                    )
                })

    def __str__(self):
        return f"{self.title} at {self.company}"


# Note model
class Note(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    job = models.ForeignKey(
        Job,  # Each note belongs to one job
        on_delete=models.CASCADE,  # delete notes if the job is deleted
        related_name="notes"
    )
    author = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,  # set to null if the user is deleted
        related_name="notes"
    )
    body = models.TextField()  # The content of the note
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Note for {self.job}…"
