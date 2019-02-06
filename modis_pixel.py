import constants
from geometries import Trapezoid, TrapezoidLeg, TrapezoidBase
import theoretical_pixel


class ModisPixel(Trapezoid):

    def __init__(self, lat, lon, scan, scan_group=None):
        self.lat = lat
        self.lon = lon
        self.scan = scan
        self.scan_group = scan_group
        self.center = constants.earth.GeoPoint(lat, lon, degrees=True)
        self.base1 = None
        self.base2 = None
        self.leg1 = None
        self.leg2 = None
        self.next_trap_center = None
        self.prev_trap_center = None
        self.area = None
        self.height = None
        self.trixels = []
        self.data = None

    def set_next_trap_center(self, next_trap_center):
        self.next_trap_center = next_trap_center

    def set_prev_trap_center(self, prev_trap_center):
        self.prev_trap_center = prev_trap_center

    def bootstrap(self):
        self.find_base1()
        self.find_base2()
        self.find_legs()

    def find_legs(self):
        self.leg1 = TrapezoidLeg(point_a=self.base1.point_a, point_b=self.base2.point_b)
        self.leg2 = TrapezoidLeg(point_a=self.base1.point_b, point_b=self.base2.point_a)

    def find_base1(self):
        self.base1 = TrapezoidBase(trap=self, length=self.base1_length())
        if self.prev_trap_center:
            self.base1.bootstrap_from_adjacent_trap(adjacent_trap_center=self.prev_trap_center)
        else:
            self.base1.bootstrap_from_opposite_trap(opposite_trap_center=self.next_trap_center)

    def find_base2(self):
        self.base2 = TrapezoidBase(trap=self, length=self.base2_length())
        if self.next_trap_center:
            self.base2.bootstrap_from_adjacent_trap(adjacent_trap_center=self.next_trap_center)
        else:
            self.base2.bootstrap_from_opposite_trap(opposite_trap_center=self.prev_trap_center)

    def base1_length(self):
        length = theoretical_pixel.base1_length(self.scan)
        return length

    def base2_length(self):
        length = theoretical_pixel.base2_length(self.scan)
        return length

    def set_color(self, fig):
        fig.set_color_from_index(self.scan_group, 10)




