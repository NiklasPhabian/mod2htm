import constants
from pixel_drawer import plots
from trixel import Trixel


def plot(trixel_symbols, color):
    for symbol in trixel_symbols:
        fig.set_color(color)
        trixel = Trixel(symbol=symbol)
        trixel.bootstrap()
        trixel.plot(fig)


def plot_all():
    line_scale = 4
    global fig
    trixel_symbols = ['N10', 'N11', 'N12', 'N13']
    fig = plots.SpherePlot(constants.earth_radius)
    fig.make_sphere(wire=True, only_front=False)
    fig.scale_line_width(line_scale)
    plot(trixel_symbols, 'blue')
    fig.zoom_to(lat=-5, lon=20, field_size=3.5e6, elevation=0, set_azimuth=True)
    fig.save_fig('../figures/htm/level1.pdf')
    fig.save_fig('../figures/htm/level1.png')

    trixel_symbols = ['N130', 'N131', 'N132', 'N133']
    fig = plots.SpherePlot(constants.earth_radius)
    fig.make_sphere(wire=True, only_front=False)
    fig.scale_line_width(line_scale)
    plot(trixel_symbols, 'red')
    fig.zoom_to(lat=-5, lon=20, field_size=3.5e6, elevation=0, set_azimuth=True)
    fig.save_fig('../figures/htm/level2.pdf')
    fig.save_fig('../figures/htm/level2.png')

    trixel_symbols = ['N1330', 'N1331', 'N1332', 'N1333']
    fig = plots.SpherePlot(constants.earth_radius)
    fig.make_sphere(wire=True, only_front=False)
    fig.scale_line_width(line_scale)
    plot(trixel_symbols, 'green')
    fig.zoom_to(lat=-5, lon=20, field_size=3.5e6, elevation=0, set_azimuth=True)
    fig.save_fig('../figures/htm/level3.pdf')
    fig.save_fig('../figures/htm/level3.png')

    trixel_symbols = ['N13330', 'N13331', 'N13332', 'N13333']
    fig = plots.SpherePlot(constants.earth_radius)
    fig.make_sphere(wire=True, only_front=False)
    fig.scale_line_width(line_scale)
    plot(trixel_symbols, 'magenta')
    fig.zoom_to(lat=-5, lon=20, field_size=3.5e6, elevation=0, set_azimuth=True)
    fig.save_fig('../figures/htm/level4.pdf')
    fig.save_fig('../figures/htm/level4.png')


plot_all()


trixel_symbols = ['S0', 'S1', 'S2', 'S3', 'N0', 'N1', 'N2', 'N3' ]
fig = plots.SpherePlot(constants.earth_radius)
fig.make_sphere(wire=True, only_front=False)
fig.scale_line_width(4)
plot(trixel_symbols, 'blue')
fig.zoom_to(lat=-5, lon=20, field_size=3.5e6, elevation=0, set_azimuth=True)
fig.save_fig('../figures/htm/level0.pdf')
fig.save_fig('../figures/htm/level0.png')


