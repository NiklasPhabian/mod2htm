import constants
from pixel_drawer import plots

prev_area = constants.earth_surface_sphere / 8
areas = []
levels = []
cutoffs = []
for level in range(1, 22):
    this_area = (prev_area/4)
    cutoffs.append((this_area+prev_area)/2)
    areas.append(prev_area)
    levels.append(level)
    prev_area = this_area


def area2level(area):
    level = 0
    while area < cutoffs[level]:
        level += 1
    return level


def do_plot():
    plt = plots.Plot()
    plt.plot(levels[11:17], areas[11:17], 'Along-scan pixel length', marker='.')
    plt.set_ylim(0, 10)
    plt.add_arrows()
    plt.x_label('HID level')
    plt.y_label('area \n in km^2')

    plt.save_fig('../figures/trixel_areas.pdf')
    plt.save_fig('../figures/trixel_areas.png')


do_plot()