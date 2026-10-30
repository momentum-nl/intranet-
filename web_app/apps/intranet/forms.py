from django import forms

from apps.intranet.models import ShoppingItem


class ShoppingItemForm(forms.ModelForm):
    class Meta:
        model = ShoppingItem
        fields = ["article", "quantity", "note"]


class ChoreRatingForm(forms.Form):
    assignment = forms.IntegerField(widget=forms.HiddenInput)
    score = forms.IntegerField(min_value=1, max_value=5)
    comment = forms.CharField(max_length=200, required=False)
