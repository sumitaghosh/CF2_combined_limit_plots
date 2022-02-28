import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from glob import glob
from os.path import join

h_eVs = 4.135667696E-15  # eV * s
h_ueV = h_eVs * 1e6  # ueV * s
upper_limit = 10  # highest limit for data
put_legend = True
save_plots = True
fill_excls = False


def end_plot(fig, ueV_ax, plot_name, last_z, tlim=1e-3, llim=1e-7, rlim=1e-1):
    plot_path_name = 'plots/img' + str(last_z) + plot_name
    GHz_ax = ueV_ax.secondary_xaxis('top', functions=(ueV_to_GHz, GHz_to_ueV))
    GHz_ax.set_xlabel('Frequency (GHz)')
    plt.xlim((llim, rlim))
    plt.ylim(top=tlim)
    if put_legend:
        legend = plt.legend()  # bbox_to_anchor=(1.05, 1))
        legend.set_zorder(last_z)  # put the legend on top
    if save_plots:
        if put_legend:
            plt.savefig(plot_path_name + '_legend.png')
        else:
            plt.savefig(plot_path_name + '.png')
            plt.savefig(plot_path_name + '.svg', format='svg', dpi=1200)
    fig.tight_layout()
    plt.show()


def ueV_to_GHz(ueV):
    return np.divide(ueV, h_ueV) * 1e-9


def GHz_to_ueV(GHz):
    return np.multiply(GHz, h_ueV) * 1e9


def start_plot():
    fig, ueV_ax = plt.subplots()
    ueV_ax.set_xlabel('Mass ($\\mu$eV)')
    ueV_ax.set_ylabel('$1 / \\Lambda$')
    ueV_ax.set_xscale('log')
    ueV_ax.set_yscale('log')
    return fig, ueV_ax


def plot_exclusions(ueV_ax, masses_list, limits_list, label_list, color_list, last_z):
    """
    All arrays are in order of back to front
    :param color_list: list of colors for the exclusion regions
    :param ueV_ax: name of axis (for plotting)
    :param masses_list: list of masses of previous searches
    :param limits_list: list of limits of previous searches
    :param label_list: labels for the previous searches
    :param last_z: number of plots already made (so these can go on top)
    :return: nothing - this function just calls fill
    """
    n = 2 * last_z + 2 + 1
    for i, (masses, limits, label, color) in enumerate(zip(masses_list, limits_list, label_list, color_list)):
        if fill_excls:
            ueV_ax.fill(masses, limits, color, label=label, zorder=n + i)
        else:
            ueV_ax.loglog(masses, limits, color=color, label=label, zorder=n + i)


def add_upper_limits(mass_ueV, exc_array, order=True):
    if order:
        mass_ueV, exc_array = zip(*sorted(zip(mass_ueV, exc_array)))
    mass_ueV2 = np.append(mass_ueV[0], mass_ueV)
    mass_ueV2 = np.append(mass_ueV2, mass_ueV2[-1])
    exc_array2 = np.append(upper_limit, exc_array)
    exc_array2 = np.append(exc_array2, upper_limit)
    return mass_ueV2, exc_array2


def get_order_of_curves():
    names = glob(join('data/', '*.csv'))
    print(names)

    colors = ['lightgray', 'darkviolet', 'yellow', 'lightskyblue', 'lightgreen', 'violet', 'brown', 'darksalmon',
              'pink', 'olive', 'goldenrod', 'midnightblue', 'teal', 'tab:grey', 'blue', 'darkslategrey', 'fuchsia']
    return names, colors


def load_exclusion_data():
    # load previous searches
    mass_array = []
    excl_array = []
    name_array = []
    file_list, color_array = get_order_of_curves()
    for f in file_list:
        name = f[f.rfind('/') + 1:f.rfind('.csv')]
        data = pd.read_csv(f, header=None)
        ueV, exc = add_upper_limits(data[0] * 1e6, data[1])
        mass_array.append(ueV)
        excl_array.append(exc)
        name_array.append(name)
    return mass_array, excl_array, name_array, color_array


def plot_exclusion():
    # load searches
    mass_array, excl_array, name_array, color_array = load_exclusion_data()
    # plot
    fig, ueV_ax = start_plot()
    plot_exclusions(ueV_ax, mass_array, excl_array, name_array, color_array, -1)
    last_z = len(mass_array) + 2
    end_plot(fig, ueV_ax, 'exclusion', last_z)


def plot_one_region(ueV, exc):
    plt.figure()
    plt.fill(ueV, exc, zorder=1)
    plt.plot(ueV, exc, zorder=2)
    plt.scatter(ueV, exc, zorder=3)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('mass (ueV)')
    plt.ylabel('$\\exc$')
    plt.show()


def main():
    plot_exclusion()


if __name__ == "__main__":
    main()
