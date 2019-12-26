from django.shortcuts import render
import matplotlib.pyplot as plt
import seaborn as sns

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