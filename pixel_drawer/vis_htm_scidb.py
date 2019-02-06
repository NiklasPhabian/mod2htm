from scidb_array import Database, HstmArray
from matplotlib.collections import PatchCollection
import geometries
from pixel_drawer.plots import GeoPlot

db = Database()
data_array = HstmArray(db)


def get_grid():
    corner_north_east = [62.81387, 309.410145]
    corner_north_west = [70.31865, 257.66612]
    corner_south_east = [-4.4317884, 271.274185]
    corner_south_west = [-1.4073523, 250.55374]
    bbox = geometries.Trapezoid([corner_south_west, corner_south_east, corner_north_east, corner_north_west])
    bbox.tesselate(9, visTrixels=True, interior=False)
    polies = []
    for trixel in bbox.trixels:
        low, high = trixel.get_range_id(14)
        color = data_array.get_avg_rgb(low, high)
        #color = (0,0,0)
        trixel.bootstrap()
        polies.append(trixel.to_polygon(color))
    return polies

polies = get_grid()

plt = GeoPlot()
plt.add_collection(PatchCollection(polies, alpha=0.5, facecolors='white', edgecolor='black', linewidth=0.001, match_original=True))
plt.set_xlim(-160, -20)
plt.set_ylim(-15, 80)
plt.x_label('longitude')
plt.y_label('latitude')
plt.save_fig('figures/htm.pdf')


