import constants
from pixel_drawer import plots

fig = plots.SpherePlot(constants.earth_radius)
fig.scale_line_width(2)
fig.make_sphere(wire=True, only_north=True)
fig.zoom_to(lat=90, lon=0, field_size=3.5e6, elevation=90)
fig.save_fig('../figures/pole.pdf')
fig.save_fig('../figures/pole.png')


fig = plots.SpherePlot(constants.earth_radius)
fig.scale_line_width(2)
fig.make_sphere(wire=True, only_front=True)
fig.zoom_to(lat=0, lon=0, field_size=3.5e6, elevation=0)
fig.save_fig('../figures/frontal.pdf')
fig.save_fig('../figures/frontal.png')



