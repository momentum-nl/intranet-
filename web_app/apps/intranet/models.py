from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Link(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField()
    category = models.CharField(max_length=50, default="Algemeen")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["category", "order", "title"]

    def __str__(self) -> str:
        return self.title


class Notification(models.Model):
    class Level(models.TextChoices):
        INFO = "info", "Info"
        WARNING = "warning", "Let op"
        DANGER = "danger", "Urgent"

    title = models.CharField(max_length=120)
    body = models.TextField(blank=True)
    level = models.CharField(max_length=10, choices=Level.choices, default=Level.INFO)
    published_at = models.DateTimeField()
    expires_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )

    class Meta:
        ordering = ["-published_at"]

    def __str__(self) -> str:
        return self.title


class RedMerge(models.Model):
    """Eén rode merge (CI rood na merge). Telling per maand = pin of shame."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    merged_on = models.DateField()
    repo = models.CharField(max_length=100)
    pr_url = models.URLField(blank=True)
    note = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["-merged_on"]

    def __str__(self) -> str:
        return f"{self.user} · {self.repo} · {self.merged_on}"


class Chore(models.Model):
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=200, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self) -> str:
        return self.name


class ChoreAssignment(models.Model):
    chore = models.ForeignKey(Chore, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    week_start = models.DateField(help_text="Maandag van de week")

    class Meta:
        ordering = ["week_start", "chore__order"]
        unique_together = [("chore", "week_start")]

    def __str__(self) -> str:
        return f"{self.chore} · {self.user} · week van {self.week_start}"


class ChoreRating(models.Model):
    assignment = models.ForeignKey(
        ChoreAssignment, on_delete=models.CASCADE, related_name="ratings"
    )
    rater = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = [("assignment", "rater")]

    def __str__(self) -> str:
        return f"{self.assignment} · {self.score}/5"


class PicnicPreference(models.Model):
    class Diet(models.TextChoices):
        ALLES = "alles", "Alles"
        VEGETARISCH = "vegetarisch", "Vegetarisch"
        VEGAN = "vegan", "Vegan"
        HALAL = "halal", "Halal"
        GLUTENVRIJ = "glutenvrij", "Glutenvrij"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="picnic"
    )
    diet = models.CharField(max_length=20, choices=Diet.choices, default=Diet.ALLES)
    allergies = models.CharField(max_length=200, blank=True)
    favourite = models.CharField("Favoriet", max_length=200, blank=True)
    drink = models.CharField("Drankje", max_length=100, blank=True)

    def __str__(self) -> str:
        return f"{self.user} · {self.get_diet_display()}"
