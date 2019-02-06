import constants
from pixel_drawer import plots
import mod09File
import multiprocessing

filename = '../../test_data/MOD09.A2017122.1640.006.2017124020332.hdf'

fig = plots.SpherePlot(constants.earth_radius)
fig.scale_line_width(0.2)
fig.make_sphere(only_north=True, wire=True)


fig.zoom_to(lat=90, lon=-80, field_size=1.2e6, set_azimuth=True)


def bootstrap_pixel(pixel):
    pixel.bootstrap()
    return pixel


n_scans = constants.n_scans
n_tracks = 10
mod09 = mod09File.Mod09File(filename)
pixels1 = mod09.to_trapezoid_list(n_tracks=20, n_scans=n_scans)
pixels2 = mod09.to_trapezoid_list(n_tracks=10, n_scans=n_scans, track_start=60)
pixels = pixels1 + pixels2

with multiprocessing.Pool(processes=8) as pool:
    pixels = pool.map(bootstrap_pixel, pixels)

fig.scale_line_width(10)
for pixel in pixels:
    pixel.plot(fig)

fig.save_fig('../figures/swath/swath_single_plot_center.pdf')
fig.save_fig('../figures/swath/swath_single_plot_center.png')
