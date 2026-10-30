from datetime import date, timedelta

import pytest

from apps.intranet import selectors, services
from apps.intranet.models import Chore, ChoreAssignment, RedMerge
from apps.users.models import User


@pytest.mark.django_db
def test_shame_leaderboard_counts_only_this_month():
    a, b = (User.objects.create(username=n) for n in ("a", "b"))
    month = date(2026, 10, 1)
    for _ in range(2):
        RedMerge.objects.create(user=a, repo="x", merged_on=month)
    RedMerge.objects.create(user=b, repo="x", merged_on=month)
    RedMerge.objects.create(user=b, repo="x", merged_on=month - timedelta(days=1))
    RedMerge.objects.create(user=b, repo="x", merged_on=month - timedelta(days=2))

    board = selectors.shame_leaderboard(month)

    assert [(e.user.username, e.count) for e in board] == [("a", 2), ("b", 1)]


@pytest.mark.django_db
def test_rate_chore_rejects_self_and_upserts():
    doer, rater = (User.objects.create(username=n) for n in ("doer", "rater"))
    assignment = ChoreAssignment.objects.create(
        chore=Chore.objects.create(name="Vaat"),
        user=doer,
        week_start=date(2026, 10, 19),
    )
    with pytest.raises(ValueError):
        services.rate_chore(assignment=assignment, rater=doer, score=5)
    services.rate_chore(assignment=assignment, rater=rater, score=2)
    services.rate_chore(assignment=assignment, rater=rater, score=4)

    assert list(assignment.ratings.values_list("score", flat=True)) == [4]
