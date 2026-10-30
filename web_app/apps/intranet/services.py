"""Schrijflogica."""

from apps.intranet.models import ChoreAssignment, ChoreRating
from apps.users.models import User


def rate_chore(
    *, assignment: ChoreAssignment, rater: User, score: int, comment: str = ""
) -> ChoreRating:
    if rater.pk == assignment.user_id:
        raise ValueError("Je kunt je eigen corvee niet beoordelen.")
    rating, _ = ChoreRating.objects.update_or_create(
        assignment=assignment,
        rater=rater,
        defaults={"score": score, "comment": comment},
    )
    return rating
