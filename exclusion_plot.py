import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

h_eVs = 4.135667696E-15  # eV * s
h_ueV = h_eVs * 1e6  # ueV * s
upper_limit = 10  # highest limit for data
put_legend = True
save_plots = True


def end_plot(fig, ueV_ax, plot_name, last_z, tlim, llim, rlim):
    plot_path_name = '../plots/img' + str(last_z) + plot_name
    GHz_ax = ueV_ax.secondary_xaxis('top', functions=(ueV_to_GHz, GHz_to_ueV))
    GHz_ax.set_xlabel('Frequency (GHz)')
    plt.xlim((llim, rlim))
    plt.ylim(top=tlim)
    if put_legend:
        legend = plt.legend(bbox_to_anchor=(1.05, 1))
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
    ueV_ax.set_ylabel('$\\chi$')
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
        ueV_ax.fill(masses, limits, color, label=label, zorder=n + i)


def add_upper_limits(mass_ueV, chi_array, order=True):
    if order:
        mass_ueV, chi_array = zip(*sorted(zip(mass_ueV, chi_array)))
    mass_ueV2 = np.append(mass_ueV[0], mass_ueV)
    mass_ueV2 = np.append(mass_ueV2, mass_ueV2[-1])
    chi_array2 = np.append(upper_limit, chi_array)
    chi_array2 = np.append(chi_array2, upper_limit)
    return mass_ueV2, chi_array2


def get_order_of_curves(full_range=False):
    # first haloscopes, then HAYSTAC, then everything else
    names = [
        'Review_ev_vs_chi_Arias calculations',
        'LSW_ev_vs_chi_CMB',
        'Review_ev_vs_chi_ALPS',
        'ev_vs_chi_YMCE',
        'Jaekel_ev_vs_chi_Coulomb',
        'LSW_ev_vs_chi_Earth',
        'LSW_ev_vs_chi_Jupiter',
        'ADMX_ev_vs_chi_ADMX',
        'LSW_ev_vs_chi_CAST',
        'Review_ev_vs_chi_HB',
        'LSW_ev_vs_chi_Solar',
        'LSW_ev_vs_chi_LSW',
        'Jaekel_ev_vs_chi_Rydberg',
        'special/LSW_ev_vs_chi_aeu',
        'LSW_ev_vs_chi_Thermal HP DM',
        'LSW_ev_vs_chi_Y(3s)',
        'LSW_ev_vs_chi_EW'
    ]

    colors = ['lightgray', 'darkviolet', 'yellow', 'lightskyblue', 'lightgreen',
              'violet', 'brown',
              'darksalmon', 'pink', 'olive', 'goldenrod', 'midnightblue', 'teal',
              'tab:grey',
              'blue',
              'darkslategrey', 'fuchsia'
              ]
    if full_range:
        return names, colors
    else:
        indices = [0, 1, 2, 3, 4, 7, 8, 9, 10, 11, 12, 14]
        cropped_names = [names[i] for i in indices]
        cropped_colors = [colors[i] for i in indices]
        return cropped_names, cropped_colors


def load_exclusion_data(full_range=False):
    # load previous searches
    mass_array = []
    excl_array = []
    name_array = []
    name_list, color_array = get_order_of_curves(full_range=full_range)
    file_list = ['../data/' + n + '.csv' for n in name_list]
    for f in file_list:
        name = f[f.rfind('chi_') + 4:f.rfind('.csv')]
        print(f[f.rfind('/') + 1:f.rfind('.csv')])
        data = pd.read_csv(f, header=None)
        ueV, chi = add_upper_limits(data[0] * 1e6, data[1])
        if 'Y(3s)' in name:
            name = '$\\gamma(3s)$'
        mass_array.append(ueV)
        excl_array.append(chi)
        name_array.append(name)
    return mass_array, excl_array, name_array, color_array


def plot_exclusion():
    # load searches
    mass_array, excl_array, name_array, color_array = load_exclusion_data(full_range=True)
    # plot
    fig, ueV_ax = start_plot()
    plot_exclusions(ueV_ax, mass_array, excl_array, name_array, color_array, -1)
    last_z = len(mass_array) + 2
    plot_name = '../plots/img' + str(last_z) + 'full_range'
    end_plot(fig, ueV_ax, plot_name, last_z, 0.5, 5e-10, 5e16)


def plot_one_region(ueV, chi):
    plt.figure()
    plt.fill(ueV, chi, zorder=1)
    plt.plot(ueV, chi, zorder=2)
    plt.scatter(ueV, chi, zorder=3)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('mass (ueV)')
    plt.ylabel('$\\chi$')
    plt.show()


def main():
    plot_exclusion()


if __name__ == "__main__":
    main()
