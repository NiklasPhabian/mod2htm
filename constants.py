import math
import nvector
earth_radius = 6371e3
n_scans = 1354                # samples per scan
n_tracks = 2030                # samples per scan
swath_angel = 55              # degrees
orbit_height = 705e3          # km
nadir_pixel_size = 1e3        # km
n_scan_groups = 203
earth_surface_sphere = 4 * math.pi * (earth_radius/1000)**2
pixel_angel = 2 * math.degrees(math.atan(0.5 * nadir_pixel_size / orbit_height))
earth = nvector.FrameE(a=earth_radius, f=0)
