import datetime
import math

import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
from django.shortcuts import render, redirect
from .forms import AcidForm, HydroForm, pHForm
from .models import Hydroxide, Acid, Container

register_matplotlib_converters()


def acid_added(container, substance):
    H = container.CmH * container.V
    container.V += substance.V
    container.save(update_fields=['V'])
    container.CmH = (H + substance.mol_H) / container.V
    container.save(update_fields=['CmH'])
    container.pH = round(-math.log10(container.CmH))
    container.save(update_fields=['pH'])
    if len(container.pHs) > 0:
        container.pHs = container.pHs + " " + str(container.pH)
    else:
        container.pHs = str(container.pH)
    container.save(update_fields=["pHs"])
    if len(container.Vs) > 0:
        container.Vs = container.Vs + " " + str(container.V)
    else:
        container.Vs = str(container.V)
    container.save(update_fields=["Vs"])


def hydro_added(container, substance):
    OH = container.CmOH * container.V
    container.V += substance.V
    container.save(update_fields=['V'])
    container.CmOH = (OH + substance.mol_OH) / container.V
    container.save(update_fields=['CmOH'])
    container.pH = round(14 + math.log10(container.CmOH))
    container.save(update_fields=['pH'])
    if len(container.pHs) > 0:
        container.pHs = container.pHs + " " + str(container.pH)
    else:
        container.pHs = str(container.pH)
    container.save(update_fields=["pHs"])
    if len(container.Vs) > 0:
        container.Vs = container.Vs + " " + str(container.V)
    else:
        container.Vs = str(container.V)
    container.save(update_fields=["Vs"])


def reaction(container):
    #tutaj liczymy ile V NaOH lub HCl dodac
    V_to_add = round((container.V * abs(10 ** (-container.pH) - 10 ** (-container.aim_pH))) / (
            10 ** (-container.aim_pH) + 1))  # 1 as Cm of either NaOH or HCl
    if container.pH < container.aim_pH:
        container.last_sub = "NaOH"
    elif container.pH > container.aim_pH:
        container.last_sub = "HCl"
    container.pHs = container.pHs + " " + str(container.aim_pH)
    container.Vs = container.Vs + " " + str(container.V + V_to_add)
    container.V += V_to_add
    container.pH = container.aim_pH
    container.CmH = 10 ** (-container.pH)
    container.CmOH = 10 ** (-(14 - container.pH))
    container.last_sub_V = V_to_add
    container.save(update_fields=['pHs', 'Vs', 'V', 'pH', 'CmH', 'CmOH', 'last_sub', 'last_sub_V'])
    pass


# take care of 404 later on
def main_view(request):
    container = Container.objects.all()[0]
    form = pHForm(request.POST)
    if form.is_valid():
        container.aim_pH = form.cleaned_data['Oczekiwane_pH']
        container.save(update_fields=['aim_pH'])
    form = pHForm()
    """
    last_acid = Acid.objects.order_by('when_added')[0]
    last_hydroxide = Hydroxide.objects.order_by('when_added')[0]
    """
    sns.set()
    sns.set_style("ticks")
    if len(container.Vs) > 1:
        Vs = [float(i) for i in container.Vs.split(" ")]
    elif len(container.Vs) == 1:
        Vs = [float(container.Vs)]
    else:
        Vs = []
    if len(container.pHs) > 1:
        pHs = [float(i) for i in container.pHs.split(" ")]
    elif len(container.pHs) == 1:
        pHs = [float(container.pHs)]
    else:
        pHs = []

    plot_ph(Vs, pHs)
    """
    if (last_acid.when_added - last_hydroxide.when_added) > datetime.timedelta(days=0, hours=0, minutes=0, seconds=0,
                                                                               microseconds=0, milliseconds=0):
        substance = last_acid
    else:
        substance = last_hydroxide
    """
    context = {'container': container, 'last_sub': container.last_sub, 'last_sub_V': container.last_sub_V, 'form': form}
    return render(request, 'chemistry/main.html', context)


def add_hydro(request):
    container = Container.objects.all()[0]
    form = HydroForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']
        V = form.cleaned_data['V']
        Cm = form.cleaned_data['Cm']
        if name[-1].isalpha():
            mol_OH = V * Cm
        else:
            mol_OH = int(name[-1]) * V * Cm
        sub = Hydroxide.objects.create(name=name, V=V, Cm=Cm, mol_OH=mol_OH)
        hydro_added(container, sub)
        reaction(container)
    form = HydroForm()
    return render(request, 'chemistry/add_hydro.html', {'form': form})


def add_acid(request):
    container = Container.objects.all()[0]
    form = AcidForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']
        V = form.cleaned_data['V']
        Cm = form.cleaned_data['Cm']
        if name[1].isalpha():
            mol_H = V * Cm
        else:
            mol_H = int(name[1]) * V * Cm
        sub = Acid.objects.create(name=name, V=V, Cm=Cm, mol_H=mol_H)
        acid_added(container, sub)
        reaction(container)
    form = AcidForm()
    return render(request, 'chemistry/add_acid.html', {'form': form})


def delete(request):
    container = Container.objects.all()[0]
    container.CmH = 0.0000001
    container.CmOH = 0.0000001
    container.pH = 7
    container.aim_pH = 7
    container.V = 1.0
    container.pHs = '7'
    container.Vs = '1'
    container.Plot = "media/pic1.png"
    container.save(update_fields=['Vs', 'pHs', 'V', 'aim_pH', 'pH', 'CmH', 'CmOH', 'Plot'])
    return redirect('/')


def plot_ph(y, x):
    plt.xlabel("Volume")
    plt.ylabel("pH")
    plt.minorticks_on()
    plt.grid(which="major", linestyle='-', linewidth='0.7')
    plt.grid(which="minor", linestyle=':', linewidth='0.5')
    plt.ylim(0, 14)
    plt.plot(y, x)
    plt.savefig("media/media/pic.png")
    c = Container.objects.all()[0]
    c.Plot = "media/pic.png"
    c.save(update_fields=['Plot'])
    pass
