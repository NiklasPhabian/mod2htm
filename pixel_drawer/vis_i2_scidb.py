from scidb_array import Database, I2Array
import pickle
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from pixel_drawer.plots import GeoPlot

db = Database()
data_array = I2Array(db)

scale = 10000
pixel_size = 1000
lat_min = -20
lat_max = 80
lon_min = -120
lon_max = -40


def get_grid():
    polies = []
    for ilat in range(lat_min*scale, lat_max*scale, pixel_size):
        for ilon in range(lon_min * scale, lon_max * scale, pixel_size):
            rgb = data_array.get_avg_rgb(lat_min=ilat, lat_max=ilat+pixel_size, lon_min=ilon, lon_max=ilon+pixel_size)
            if sum(rgb) == 0:
                rgb = (1, 1, 1)
            lat = ilat / scale
            lon = ilon / scale
            corners = ((lon - pixel_size/scale/2, lat - pixel_size/scale/2),
                       (lon - pixel_size/scale/2, lat + pixel_size/scale/2),
                       (lon + pixel_size/scale/2, lat + pixel_size/scale/2),
                       (lon + pixel_size/scale/2, lat - pixel_size/scale/2))
            p = Polygon(corners, facecolor=rgb)
            polies.append(p)

    with open('i2.dump', 'wb') as dump_file:
        pickle.dump(polies, dump_file)
    return polies


def make_plot():
    with open('i2.dump', 'rb') as dump_file:
        polies = pickle.load(dump_file)
    plt = GeoPlot()
    plt.add_collection(PatchCollection(polies, alpha=0.5, edgecolor='black', linewidth=0.001, match_original=True))
    plt.set_xlim(-120, -40)
    plt.set_ylim(-15, 80)
    plt.save_fig('../figures/i2.pdf')


get_grid()
make_plot()






