import datetime
import multiprocessing
import numpy
import constants
import hstm_apps
import mod09File
import glob
from scidb_array import HstmArrayLoad, HstmArray, Database

db = Database()


def load_pixels(filename, n_tracks, n_scans, track_start):
    mod09 = mod09File.Mod09File(filename)
    pixels = mod09.to_trapezoid_list(n_tracks=n_tracks, n_scans=n_scans, track_start=track_start)
    return pixels


def bootstrap_pixel(pixel):
    pixel.bootstrap()
    return pixel


def bootstrap_pixels(pixels):
    with multiprocessing.Pool(processes=8) as pool:
        pixels = pool.map(bootstrap_pixel, pixels)
    return pixels


def tesselate_pixels(pixels):
    process = hstm_apps.IntersectionProcess(level=14, keepalive=True, interior=True)
    for pixel in pixels:
        pixel.tesselate(process=process)
    process.kill()
    return pixels


def upload_range(pixels):
    array = []
    for pixel in pixels:
        for trixel in pixel.trixels:
            array.append((trixel.id, pixel.scan_group, pixel.data[1], pixel.data[2], pixel.data[3], pixel.data[4]))
    data = numpy.array(array, dtype=[('hid', 'int64'), ('scan_group', 'int8'), ('band1', 'int16'), ('band2', 'int16'), ('band3', 'int16'), ('band4', 'int16')])
    final_array = HstmArray(db)
    #final_array.create()
    load_array = HstmArrayLoad(db)
    load_array.create()
    load_array.upload_data(data)
    load_array.redimension(destination_array=final_array.name)
    final_array.remove_old_versions()
    load_array.remove()



if __name__ == '__main__':
    n_scans = constants.n_scans
    n_tracks = 5  # constants.n_tracks
    filenames = glob.glob('/home/griessbaum/ca_swath/*.hdf')
    file_id = 0
    for filename in filenames:
        print(filename)
        for track_start in range(0, constants.n_tracks, n_tracks):
            print(track_start)
            pixels = load_pixels(filename=filename, n_scans=n_scans, n_tracks=n_tracks, track_start=track_start)
            pixels = bootstrap_pixels(pixels)
            pixels = tesselate_pixels(pixels)
            start = datetime.datetime.now()
            upload_range(pixels)
            print("inserted {} tracks within {}".format(n_tracks, datetime.datetime.now() - start))
        file_id += 1

