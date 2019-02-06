import math
from constants import earth_radius, orbit_height, pixel_angel, n_scans


def cot(radians):
    return 1/math.tan(radians)


def cot2(radians):
    return (1 / math.tan(radians)) ** 2


def distance_from_nadir(viewing_angel):
    x, y = view_interception_point(viewing_angel)
    beta = (math.atan(x / y))
    distance = beta * earth_radius
    return distance


def view_interception_point(viewing_angel):
    if viewing_angel == 0:
        return 0, earth_radius
    alpha = math.radians(viewing_angel)
    x1 = (-math.sqrt(4 * cot2(alpha) * earth_radius ** 2 - 8 * earth_radius * orbit_height - 4 * orbit_height ** 2) +
          2 * earth_radius * cot(alpha) + 2 * orbit_height * cot(alpha)) / (2 * (cot2(alpha) + 1))
    x2 = (math.sqrt(4 * cot2(alpha) * earth_radius ** 2 - 8 * earth_radius * orbit_height - 4 * orbit_height ** 2) +
          2 * earth_radius * cot(alpha) + 2 * orbit_height * cot(alpha)) / (2 * (cot2(alpha) + 1))
    if abs(x1) < abs(x2):
        x = x1
    else:
        x = x2
    y = math.sqrt(earth_radius ** 2 - x ** 2)
    return x, y


def view_vector_length(viewing_angel):
    x, y = view_interception_point(viewing_angel)
    length = math.sqrt((orbit_height + earth_radius - y) ** 2 + x ** 2)
    return length


def track_length(viewing_angel):
    # length in track direction
    length = math.tan(math.radians(pixel_angel)) * view_vector_length(viewing_angel)
    return length


class TheoreticalPixel:

    def __init__(self):
        self.center_view_angel = None
        self.scan = None
        self.area = None
        self.pixel_angel = pixel_angel

    def set_viewing_angle(self, center_view_angel):
        self.center_view_angel = center_view_angel

    def set_scan(self, scan):
        self.scan = scan
        self.scan2viewing_angel(scan)

    def scan2viewing_angel(self, scan):
        # We would like: view_angel = -55 + scan * pixel_angel
        # but because of floating precision, we exploit symmetry
        scans_from_nadir = abs(scan-n_scans/2)
        center_view_angel = scans_from_nadir*self.pixel_angel
        if scan < n_scans/2:
            center_view_angel *= -1
        self.set_viewing_angle(center_view_angel)

    def scan_size(self):
        # Pixel size in scan direction
        l1 = distance_from_nadir(self.center_view_angel - 0.5 * self.pixel_angel)
        l2 = distance_from_nadir(self.center_view_angel + 0.5 * self.pixel_angel)
        return l2-l1

    def base1_length(self):
        viewing_angle = self.center_view_angel - self.pixel_angel
        return track_length(viewing_angle)

    def base2_length(self):
        viewing_angle = self.center_view_angel + self.pixel_angel
        return track_length(viewing_angle)

    def small_base_length(self):
        viewing_angle = abs(self.center_view_angel) - self.pixel_angel
        return track_length(viewing_angle)

    def center_length(self):
        return track_length(self.center_view_angel)

    def large_base_length(self):
        viewing_angle = abs(self.center_view_angel) + self.pixel_angel
        return track_length(viewing_angle)

    def trapezoid_area(self):
        a = self.small_base_length()
        b = self.large_base_length()
        h = self.scan_size()
        area = (a+b)/2*h
        self.area = area
        return area

    def rectangular_area(self):
        a = self.center_length()
        h = self.scan_size()
        area = a * h
        self.area = area
        return area


base1_lengths = []
base2_lengths = []
for scan in range(1354):
    tp = TheoreticalPixel()
    tp.set_scan(scan)
    base1_lengths.append(tp.base1_length())
    base2_lengths.append(tp.base2_length())


def base1_length(scan):
    return base1_lengths[scan]


def base2_length(scan):
    return base2_lengths[scan]

