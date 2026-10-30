from django import forms

from apps.intranet.models import PicnicPreference


class PicnicPreferenceForm(forms.ModelForm):
    class Meta:
        model = PicnicPreference
        fields = ["diet", "allergies", "favourite", "drink"]
        labels = {
            "diet": "Dieet",
            "allergies": "Allergieën",
            "favourite": "Wat moet er zeker bij?",
            "drink": "Drankje",
        }


class ChoreRatingForm(forms.Form):
    assignment = forms.IntegerField(widget=forms.HiddenInput)
    score = forms.IntegerField(min_value=1, max_value=5)
    comment = forms.CharField(max_length=200, required=False)
