from django import forms


class AcidForm(forms.Form):
    name = forms.CharField(label="Podaj nazwę silnego kwasu do dodania", max_length=8, required=True)
    V = forms.FloatField(label="Podaj objętość substancji w litrach", required=True)
    Cm = forms.IntegerField(label="Podaj stężenie molowe substancji", required=True)



class HydroForm(forms.Form):
    name = forms.CharField(label="Podaj nazwę silnej zasady do dodania", max_length=8, required=True)
    V = forms.FloatField(label="Podaj objętość substancji w litrach", required=True)
    Cm = forms.IntegerField(label="Podaj stężenie molowe substancji", required=True)


class pHForm(forms.Form):
    Oczekiwane_pH = forms.IntegerField(label="Oczekiwane pH w zbiorniku", required=True)
