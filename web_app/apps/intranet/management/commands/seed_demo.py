"""Demodata voor lokaal ontwikkelen. Idempotent."""

from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.intranet.models import Chore, ChoreAssignment, Notification, RedMerge
from apps.intranet.selectors import week_start
from apps.users.models import User


class Command(BaseCommand):
    help = "Vult demo-notificaties, corvee en rode merges"

    def handle(self, *args, **options):
        users = [
            User.objects.get_or_create(username=n, defaults={"first_name": n.title()})[
                0
            ]
            for n in ("max", "jasper", "kilian", "mara")
        ]
        Notification.objects.get_or_create(
            title="Welkom op het intranet",
            defaults={
                "body": "Links, notificaties, pin of shame, corvee en picnic op één plek.",
                "published_at": timezone.now(),
            },
        )
        today = timezone.localdate()
        for i, (u, repo) in enumerate(
            [
                (users[1], "igepa-order-agent"),
                (users[1], "scalar-cpq"),
                (users[2], "website"),
            ]
        ):
            RedMerge.objects.get_or_create(
                user=u, repo=repo, merged_on=today - timedelta(days=i * 3)
            )
        chores = [
            Chore.objects.get_or_create(name=n, defaults={"order": i})[0]
            for i, n in enumerate(
                ["Vaatwasser", "Koffiemachine", "Planten", "Prullenbakken"]
            )
        ]
        start = week_start()
        for w in range(-2, 3):
            for i, chore in enumerate(chores):
                ChoreAssignment.objects.get_or_create(
                    chore=chore,
                    week_start=start + timedelta(weeks=w),
                    defaults={"user": users[(i + w) % len(users)]},
                )
        self.stdout.write(self.style.SUCCESS("Demodata staat klaar."))
