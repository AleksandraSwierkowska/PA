import datetime
import math
import io
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from pandas.plotting import register_matplotlib_converters
from django.http import HttpResponse
from django.shortcuts import render
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
    pic = plot_ph(container.V, container.pH)
    pic.seek(0)  # rewind to beginning of file
    pic = base64.b64encode(pic.getvalue())  # load the bytes in the context as base64
    pic = pic.decode('utf8')

    if (last_acid.when_added - last_hydroxide.when_added) > datetime.timedelta(days=0, hours=0, minutes=0, seconds=0,
                                                                               microseconds=0, milliseconds=0):
        substance = last_acid
    else:
        substance = last_hydroxide
    context = {'container': container, 'substance': substance, 'pic': pic}
    return render(request, 'chemistry/main.html', context)


def add_substance(request):
    return HttpResponse("Add a new substance")



def plot_ph(x, y):
    fig = Figure()
    plt.xlabel("Volume")
    plt.ylabel("pH")
    plt.minorticks_on()
    plt.grid(which="major", linestyle='-', linewidth='0.7')
    plt.grid(which="minor", linestyle=':', linewidth='0.5')
    plt.ylim(0, 14)
    plt.plot(y, x)
    FigureCanvas(fig)
    buf = io.BytesIO()
    plt.savefig(buf, format='png', transparent=True, dpi=130)
    plt.close(fig)
    return buf


def plot_volume(x, y):
    plt.xlabel("Time")
    plt.ylabel("Volume")
    plt.minorticks_on()
    plt.grid(which="major", linestyle='-', linewidth='0.7')
    plt.grid(which="minor", linestyle=':', linewidth='0.5')
    plt.plot(y, x)
    plt.savefig("static/chemistry/images/pic2")
