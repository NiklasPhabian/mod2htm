import constants
import mod09File
import numpy
from scidb_array import I2Array, I2ArrayLoad, Database

db = Database()

load_array = I2ArrayLoad(db)
load_array.remove()
load_array.create()

array = I2Array(db)
array.remove()
array.create()


def load_pixels(filename, n_tracks, n_scans, track_start):
    mod09 = mod09File.Mod09File(filename)
    pixels = mod09.to_trapezoid_list(n_tracks=n_tracks, n_scans=n_scans, track_start=track_start)
    return pixels


if __name__ == '__main__':
    n_scans = constants.n_scans
    n_tracks = 100#constants.n_tracks
    filenames = []
    filenames.append('/home/griessbaum/no_swath/MOD09.A2017122.1700.006.2017124021013.hdf')
    filenames.append('/home/griessbaum/no_swath/MOD09.A2017122.1655.006.2017124020806.hdf')
    filenames.append('/home/griessbaum/no_swath/MOD09.A2017122.1650.006.2017124020624.hdf')
    filenames.append('/home/griessbaum/no_swath/MOD09.A2017122.1645.006.2017124020459.hdf')
    file_id = 0
    scale = 10000
    for filename in filenames:
        print(filename)
        for track_start in range(0, constants.n_tracks, n_tracks):
            pixels = load_pixels(filename=filename, n_scans=n_scans, n_tracks=n_tracks, track_start=track_start)
            data = []
            for pixel in pixels:
                ilat = int(pixel.lat * scale)
                ilon = int(pixel.lon * scale)
                data.append((ilat, ilon, pixel.scan_group, pixel.data[1], pixel.data[2], pixel.data[3], pixel.data[4]))
            data = numpy.array(data, dtype=[('ilat', 'int64'), ('ilon', 'int64'), ('scan_group', 'int16'),
                                            ('band1', 'int16'), ('band2', 'int16'), ('band3', 'int16'), ('band4', 'int16')])
            load_array.upload_data(data)
            load_array.redimension(destination_array=array.name)
            array.remove_old_versions()
        file_id += 1
