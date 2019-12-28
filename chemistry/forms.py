from django import forms


class AcidForm(forms.Form):
    name = forms.CharField(max_length=8, required=True)
    V = forms.FloatField(required=True)
    Cm = forms.IntegerField(required=True)


class HydroForm(forms.Form):
    name = forms.CharField(max_length=8, required=True)
    V = forms.FloatField(required=True)
    Cm = forms.IntegerField(required=True)
