from django.shortcuts import render
from django.http import HttpResponse
from .models import Hydroxide, Acid, Container
import datetime, math
import matplotlib.pyplot as plt
import seaborn as sns


def sub_added(container, substance):
    H = container.V * container.CmH
    container.V += substance.V
    if type(substance) == Hydroxide:
        container.CmH = (H - substance.mol_OH) / container.V
    elif type(substance) == Acid:
        container.CmH = (H + substance.mol_H) / container.V
    container.pH = -math.log10(container.CmH)


#def reaction(container):
#   n1 = container.V * container.CmH
#    n2 = container.V * (10 ** (-container.aim_pH))
#    x = abs(n1 - n2)
#    if container.pH > container.aim_pH:

# else:


# take care of 404 later on
def main_view(request):
    container = Container.objects.all()[0]
    last_acid = Acid.objects.order_by('when_added')[0]
    last_hydroxide = Hydroxide.objects.order_by('when_added')[0]
    if (last_acid.when_added - last_hydroxide.when_added) > datetime.timedelta(days=0, hours=0, minutes=0, seconds=0,
                                                                               microseconds=0, milliseconds=0):
        substance = last_acid
    else:
        substance = last_hydroxide
    context = {'container': container, 'substance': substance}
    return render(request, 'chemistry/main.html', context)



def add_substance(request):
    return HttpResponse("Add a new substance")
# Create your views here.

sns.set()
sns.set_style("ticks")


# Create your views here.
def plot_ph(x, y):
    plt.xlabel("Time")
    plt.ylabel("pH")
    plt.minorticks_on()
    plt.grid(which="major", linestyle='-', linewidth='0.7')
    plt.grid(which="minor", linestyle=':', linewidth='0.5')
    plt.ylim(0,14)
    plt.plot(y,x)
    plt.savefig("static/chemistry/images/pic1.png")

def plot_volume(x, y):
    plt.xlabel("Time")
    plt.ylabel("Volume")
    plt.minorticks_on()
    plt.grid(which="major", linestyle='-', linewidth='0.7')
    plt.grid(which="minor", linestyle=':', linewidth='0.5')
    plt.plot(y,x)
    plt.savefig("static/chemistry/images/pic1.png")