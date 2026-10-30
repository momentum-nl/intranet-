from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.intranet import selectors, services
from apps.intranet.forms import ChoreRatingForm, ShoppingItemForm
from apps.intranet.models import ChoreAssignment, ShoppingItem


@login_required
def dashboard(request):
    shame = selectors.shame_leaderboard()
    return render(
        request,
        "intranet/dashboard.html",
        {
            "notifications": selectors.active_notifications(),
            "link_groups": selectors.links_grouped(),
            "shame": shame[0] if shame else None,
            "shame_rest": shame[1:],
            "corvee": selectors.corvee_schedule(weeks=1),
            "shopping": selectors.shopping_items(),
        },
    )


@login_required
def corvee(request):
    if request.method == "POST":
        form = ChoreRatingForm(request.POST)
        if form.is_valid():
            assignment = get_object_or_404(
                ChoreAssignment, pk=form.cleaned_data["assignment"]
            )
            try:
                services.rate_chore(
                    assignment=assignment,
                    rater=request.user,
                    score=form.cleaned_data["score"],
                    comment=form.cleaned_data["comment"],
                )
                messages.success(request, "Beoordeling opgeslagen.")
            except ValueError as e:
                messages.error(request, str(e))
        return redirect("intranet:corvee")
    return render(
        request,
        "intranet/corvee.html",
        {
            "upcoming": selectors.corvee_schedule(),
            "history": selectors.corvee_history(),
            "ranking": selectors.corvee_ranking(),
            "this_week": selectors.week_start(),
        },
    )


@login_required
def shopping(request):
    form = ShoppingItemForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("intranet:shopping")
    return render(
        request,
        "intranet/shopping.html",
        {"form": form, "items": selectors.shopping_items()},
    )


@login_required
@require_POST
def shopping_delete(request, pk: int):
    get_object_or_404(ShoppingItem, pk=pk).delete()
    return redirect("intranet:shopping")
