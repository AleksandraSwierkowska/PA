import datetime
import math
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from .models import Hydroxide, Acid, Container

register_matplotlib_converters()


def sub_added(container, substance):
    H = container.V * container.CmH
    container.V += substance.V
    if type(substance) == Hydroxide:
        container.CmH = (H - substance.mol_OH) / container.V
    elif type(substance) == Acid:
        container.CmH = (H + substance.mol_H) / container.V
    container.pH = -math.log10(container.CmH)


def reaction(container):
    V_to_add = (container.V * abs(10 ** (-container.pH) - 10 ** (-container.aim_pH))) / (
            10 ** (-container.aim_pH) + 1)  # 1 as Cm of either NaOH or HCl
    container.V += V_to_add
    container.pH = container.aim_pH
    container.CmH = 10 ** (-container.pH)
    return V_to_add


# take care of 404 later on
def main_view(request):
    container = Container.objects.all()[0]
    last_acid = Acid.objects.order_by('when_added')[0]
    last_hydroxide = Hydroxide.objects.order_by('when_added')[0]
    sns.set()
    sns.set_style("ticks")
    if len(container.Vs) > 1:
        Vs = [int(i) for i in container.Vs.split(" ")]
    elif len(container.Vs) == 1:
        Vs = [int(container.Vs)]
    else:
        Vs = []
    if len(container.pHs) > 1:
        pHs = [int(i) for i in container.pHs.split(" ")]
    elif len(container.pHs) == 1:
        pHs = [int(container.pHs)]
    else:
        pHs = []

    plot_ph(Vs, pHs)

    if (last_acid.when_added - last_hydroxide.when_added) > datetime.timedelta(days=0, hours=0, minutes=0, seconds=0,
                                                                               microseconds=0, milliseconds=0):
        substance = last_acid
    else:
        substance = last_hydroxide

    context = {'container': container, 'substance': substance, }
    return render(request, 'chemistry/main.html', context)


def add_substance(request):
    return render(request, 'chemistry/add.html', {'container': Container.objects.all()[0]})


def delete(request):
    container = Container.objects.all()[0]
    container.CmH = 0.0000001
    container.pH = 7
    container.aim_pH = 7
    container.V = 0.0
    container.pHs = ''
    container.Vs = ''
    plot_ph([], [])
    container.save(update_fields=['Vs', 'pHs', 'V', 'aim_pH', 'pH', 'CmH', ])
    return redirect('/')


def plot_ph(x, y):
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
