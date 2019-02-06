from pyhdf.SD import SD
import modis_pixel
import constants


class Mod09File:

    def __init__(self, filename):
        self.hdf = SD(filename)
        self.latitude_sds = None
        self.longitude_sds = None
        self.data = []
        self.load_latitude_sds()
        self.load_longitude_sds()
        self.load_1km_data()

    def get_sds(self, hdf_key):
        sds_obj = self.hdf.select(hdf_key)
        data = sds_obj.get()
        return data

    def load_latitude_sds(self):
        self.latitude_sds = self.get_sds('Latitude')

    def load_longitude_sds(self):
        self.longitude_sds = self.get_sds('Longitude')

    def load_1km_data(self):
        for band in range(1, 17):
            sds_name = '1km Surface Reflectance Band {band}'.format(band=band)
            self.data.append(self.get_sds(sds_name))

    def return_data(self, track, scan):
        ret = []
        for data in self.data:
            ret.append(data[track, scan])
        return ret

    def n_tracks(self):
        return self.latitude_sds.shape[0]

    def n_scans(self):
        return self.latitude_sds.shape[1]

    def max_track_index(self):
        return self.n_tracks() - 1

    def max_scan_index(self):
        return self.n_scans() - 1

    def to_trapezoid_list(self, n_tracks=2030, n_scans=1354, track_start=0, scan_start=0):
        trapezoids = []
        track_end = min(constants.n_tracks, track_start+n_tracks)
        for track in range(track_start, track_end):
            prev_trap = None
            scan_group = int(track / 10)
            for scan in range(scan_start, scan_start+n_scans):
                lat = self.latitude_sds[track, scan]
                lon = self.longitude_sds[track, scan]
                pixel = modis_pixel.ModisPixel(lat=lat, lon=lon, scan=scan, scan_group=scan_group)
                pixel.data = self.return_data(track, scan)
                if prev_trap:
                    prev_trap.set_next_trap_center(pixel.center)
                    pixel.set_prev_trap_center(prev_trap.center)
                prev_trap = pixel
                trapezoids.append(pixel)
        return trapezoids
