import datetime
import constants
import hstm_apps
import mod09File
import multiprocessing
from pixel_drawer import plots

filename = '../../test_data/MOD09.A2017058.0010.006.2017059023206.hdf'  # Northpole
#filename = '../../test_data/MYD09.A2017331.2050.006.2017333022131.hdf'  # Cali
#filename = '../../test_data/MYD09.A2017320.0800.006.2017322021802.hdf'  # Himalaya


mod09 = mod09File.Mod09File(filename)
n_scans = 2#constants.n_scans
n_tracks = 1


def tesselate_pixel(pixel, process=None):
    pixel.tesselate(process=process)
    return pixel


def bootstrap_trixels(pixel):
    for trixel in pixel.trixels:
        trixel.bootstrap()
    return pixel


print("reading")
pixels = mod09.to_trapezoid_list(n_tracks=n_tracks, n_scans=n_scans, scan_start=600-n_scans)


def bootstrap_pixels():
    global pixel
    print("bootstraping traps")
    for pixel in pixels:
        pixel.bootstrap()


def tesselate_pixels():
    print("Tesselating pixels")
    start = datetime.datetime.now()
    process = hstm_apps.IntersectionProcess(level=14, interior=False, keepalive=True)
    for pixel in pixels:
        tesselate_pixel(pixel, process)
    print("finished within {}".format(datetime.datetime.now() - start))


def get_trixel_corners():
    global start, pool, pixels
    print("getting trixel corners")
    start = datetime.datetime.now()
    with multiprocessing.Pool(processes=8) as pool:
        pixels = pool.map(bootstrap_trixels, pixels)
    print("finished within {}".format(datetime.datetime.now() - start))


def get_areas():
    global pixel
    tessel_area = 0
    pixel_area = 0
    for pixel in pixels:
        for trixel in pixel.trixels:
            tessel_area += trixel.area()
        pixel_area += pixel.area
    print(tessel_area)
    print(pixel_area)
    print(tessel_area / pixel_area)


def get_trixel_count():
    count = 0
    for pixel in pixels:
        count += len(pixel.trixels)
    print(count)


def plot():
    print("plotting")
    fig = plots.SpherePlot(constants.earth_radius)
    print(pixels[int(1)])
    fig.zoom_to(lat=pixels[int(1)].lat, lon=pixels[int(1)].lon, set_azimuth=False, field_size=2e3)
    for pixel in pixels:
        fig.set_color('red')
        pixel.plot(fig)
    for trixel in pixels[0].trixels:
            fig.set_color('blue')
            trixel.plot(fig)
    # fig.plot_axes()
    # fig.make_sphere()
    fig.save_fig('../figures/tesselation.pdf')
    fig.save_fig('../figures/tesselation.png')



bootstrap_pixels()
tesselate_pixels()
get_trixel_corners()
#get_areas()
#get_trixel_count()
plot()


