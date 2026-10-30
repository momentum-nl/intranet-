"""Leeslogica. Geeft geëvalueerde data terug voor templates."""

from dataclasses import dataclass
from datetime import date, timedelta
from itertools import groupby

from django.db.models import Avg, Count
from django.utils import timezone

from apps.intranet.models import (
    ChoreAssignment,
    Link,
    Notification,
    PicnicPreference,
    RedMerge,
)
from apps.users.models import User


def links_grouped() -> list[tuple[str, list[Link]]]:
    links = list(Link.objects.all())
    return [
        (cat, list(items))
        for cat, items in groupby(links, key=lambda link: link.category)
    ]


def active_notifications() -> list[Notification]:
    now = timezone.now()
    qs = Notification.objects.filter(published_at__lte=now).exclude(expires_at__lte=now)
    return list(qs)


@dataclass
class ShameEntry:
    user: User
    count: int


def shame_leaderboard(month: date | None = None, limit: int = 5) -> list[ShameEntry]:
    """Rode merges per persoon in de maand, meeste eerst. [0] draagt de pin."""
    month = month or timezone.localdate()
    rows = (
        RedMerge.objects.filter(
            merged_on__year=month.year, merged_on__month=month.month
        )
        .values("user")
        .annotate(count=Count("id"))
        .order_by("-count", "user__username")[:limit]
    )
    users = User.objects.in_bulk([r["user"] for r in rows])
    return [ShameEntry(user=users[r["user"]], count=r["count"]) for r in rows]


def week_start(day: date | None = None) -> date:
    day = day or timezone.localdate()
    return day - timedelta(days=day.weekday())


def corvee_schedule(weeks: int = 4) -> list[ChoreAssignment]:
    """Deze week plus de komende weken, met gemiddelde rating geannoteerd."""
    start = week_start()
    end = start + timedelta(weeks=weeks)
    qs = (
        ChoreAssignment.objects.filter(week_start__gte=start, week_start__lt=end)
        .select_related("chore", "user")
        .annotate(avg_score=Avg("ratings__score"), n_ratings=Count("ratings"))
    )
    return list(qs)


def corvee_history(weeks: int = 4) -> list[ChoreAssignment]:
    """Afgelopen weken: dit is wat je beoordeelt."""
    start = week_start()
    qs = (
        ChoreAssignment.objects.filter(
            week_start__lt=start, week_start__gte=start - timedelta(weeks=weeks)
        )
        .select_related("chore", "user")
        .annotate(avg_score=Avg("ratings__score"), n_ratings=Count("ratings"))
        .order_by("-week_start", "chore__order")
    )
    return list(qs)


def corvee_ranking() -> list[dict]:
    """Gemiddelde rating per persoon over alle corvee ooit."""
    rows = (
        ChoreAssignment.objects.filter(ratings__isnull=False)
        .values("user__id", "user__username", "user__first_name", "user__last_name")
        .annotate(avg_score=Avg("ratings__score"), n_ratings=Count("ratings"))
        .order_by("-avg_score")
    )
    return list(rows)


def picnic_summary() -> list[dict]:
    rows = (
        PicnicPreference.objects.values("diet")
        .annotate(count=Count("id"))
        .order_by("-count")
    )
    labels = dict(PicnicPreference.Diet.choices)
    return [{"label": labels[r["diet"]], "count": r["count"]} for r in rows]


def picnic_preferences() -> list[PicnicPreference]:
    return list(
        PicnicPreference.objects.select_related("user").order_by("user__username")
    )
