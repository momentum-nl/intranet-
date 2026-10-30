from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.intranet import selectors, services
from apps.intranet.forms import ChoreRatingForm, PicnicPreferenceForm
from apps.intranet.models import ChoreAssignment, PicnicPreference


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
            "picnic": selectors.picnic_summary(),
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
def picnic(request):
    pref = PicnicPreference.objects.filter(user=request.user).first()
    form = PicnicPreferenceForm(request.POST or None, instance=pref)
    if request.method == "POST" and form.is_valid():
        form.instance.user = request.user
        form.save()
        messages.success(request, "Voorkeuren opgeslagen.")
        return redirect("intranet:picnic")
    return render(
        request,
        "intranet/picnic.html",
        {
            "form": form,
            "summary": selectors.picnic_summary(),
            "everyone": selectors.picnic_preferences(),
        },
    )
