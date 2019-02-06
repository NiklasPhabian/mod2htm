import copy
import math
import numpy
import nvector
import hstm_apps
import trixel


from constants import earth


class Trapezoid:
    def __init__(self, corners):
        self.base1 = Line()
        self.base2 = Line()
        self.leg1 = Line()
        self.leg2 = Line()
        self.leg1.set_points_from_coord(corners[0], corners[1])
        self.leg2.set_points_from_coord(corners[2], corners[3])
        self.base1.set_points_from_coord(corners[1], corners[3])
        self.base2.set_points_from_coord(corners[2], corners[0])
        self.trixels = []
        self.area = None
        self.height = None
        self.center = None
        self.width = None
        self.bootstrap()

    def bootstrap(self):
        self.find_height()
        self.find_area()
        self.find_center()

    def find_center(self):
        path = nvector.GeoPath(self.base1.center, self.base2.center)
        self.center = path.interpolate(0.5).to_geo_point()

    def set_color(self, fig):
        fig.set_color_from_index(3, 10)

    def plot(self, fig, color=None, center=False, bases=True, legs=True, corners=False, base_center=False):
        if color is None:
            self.set_color(fig)
        else:
            fig.set_color(color)
        if center:
            fig.plot_geo_point(self.center)
        if bases:
            self.base1.plot(fig)
            self.base2.plot(fig)
        if legs:
            self.leg1.plot(fig)
            self.leg2.plot(fig)
        if corners:
            self.base1.plot(fig, line=False, vertex=True)
            self.base2.plot(fig, line=False, vertex=True)
        if base_center:
            self.base1.plot(fig, line=False, center=True)
            self.base2.plot(fig, line=False, center=True)

    def tesselate(self, level=None, process=None, visTrixels=False, interior=False):
        if process is not None:
            ids = process.intersect(corners=self.corners())
        else:
            ids = hstm_apps.simple_intersect(corners=self.corners(), level=level, interior=interior)
        for id in ids:
            if visTrixels:
                t = trixel.VisTrixel(id=int(id), level=level)
            else:
                t = trixel.Trixel(id=int(id), level=level)
            self.trixels.append(t)

    def corners(self):
        corners = []
        corners.append((self.base1.point_a.latitude_deg, self.base1.point_a.longitude_deg))
        corners.append((self.base2.point_b.latitude_deg, self.base2.point_b.longitude_deg))
        corners.append((self.base1.point_b.latitude_deg, self.base1.point_b.longitude_deg))
        corners.append((self.base2.point_a.latitude_deg, self.base2.point_a.longitude_deg))
        return corners

    def corners_norm(self):
        outstr = ''
        for corner in self.corners():
            for row in corner.to_nvector().normal:
                outstr += str(row[0]) + ' '
            outstr += '\n'
        return outstr

    def find_area(self):
        area = (self.base1.length * self.base2.length)*self.height/2
        self.area = area/1000/1000/1000

    def find_width(self):
        self.width = (self.base2.length + self.base1.length)/2

    def find_height(self):
        height, _azia, _azib = self.base1.center.distance_and_azimuth(self.base2.center)
        self.height = height

    def __str__(self):
        ret = str(self.leg1.point_a.latitude_deg) + ' ' + str(self.leg1.point_a.longitude_deg) + '\n'
        ret += str(self.leg1.point_b.latitude_deg) + ' ' + str(self.leg1.point_b.longitude_deg) + '\n'
        ret += str(self.leg2.point_a.latitude_deg) + ' ' + str(self.leg2.point_a.longitude_deg) + '\n'
        ret += str(self.leg2.point_b.latitude_deg) + ' ' + str(self.leg2.point_b.longitude_deg)
        return ret


class Line:
    def __init__(self):
        self.point_a = None
        self.point_b = None
        self.pvector_a = None
        self.pvector_b = None
        self.line_points = None
        self.length = None
        self.center = None
        self.path = None

    def set_points_from_coord(self, point_a, point_b):
        self.point_a = earth.GeoPoint(point_a[0], point_a[1], degrees=True)
        self.point_b = earth.GeoPoint(point_b[0], point_b[1], degrees=True)
        self.bootstrap()

    def bootstrap(self):
        self.get_pvectors()
        self.find_path()
        self.find_length()
        self.find_center()

    def find_length(self):
        self.length = abs(self.path.track_distance(method='greatcircle').ravel()[0])
        return self.length

    def find_path(self):
        self.path = nvector.GeoPath(self.point_a, self.point_b)
        return self.path

    def find_center(self):
        self.center = self.path.interpolate(0.5).to_geo_point()
        return self.center

    def line_points_pvector(self):
        path = self.path()
        xs = []
        ys = []
        zs = []
        n_steps = 5
        for step in range(n_steps+1):
            pvector = path.interpolate(step / n_steps).to_ecef_vector().pvector
            xs.append(pvector[0][0])
            ys.append(pvector[1][0])
            zs.append(pvector[2][0])
        return xs, ys, zs

    def line_points(self):
        path = self.path()
        positions = []
        n_steps = 5
        for step in range(n_steps+1):
            positions.append(path.interpolate(step/n_steps).to_geo_point())
        return positions

    def plot_line(self, fig):
        xs, ys, zs = self.line_points_pvector()
        fig.plot_geo_line_carthesian(xs, ys, zs)

    def plot_straight_line(self, fig):
        fig.plot_straight_line_from_pvector(self.pvector_a, self.pvector_b)

    def get_pvectors(self):
        pva = self.point_a.to_ecef_vector().pvector
        pvb = self.point_b.to_ecef_vector().pvector
        self.pvector_a = (pva[0][0], pva[1][0], pva[2][0])
        self.pvector_b = (pvb[0][0], pvb[1][0], pvb[2][0])

    def plot(self, fig, vertex=False, center=False, line=True):
        if line:
            self.plot_straight_line(fig)
        if vertex:
            fig.plot_geo_point(self.point_a)
            fig.plot_geo_point(self.point_b)
        if center:
            fig.plot_geo_point(self.center)


class TrapezoidLeg(Line):
    def __init__(self, point_a, point_b):
        super(TrapezoidLeg, self).__init__()
        self.point_a = point_a
        self.point_b = point_b
        self.get_pvectors()


class TrapezoidBase(Line):
    def __init__(self, trap, length):
        super(TrapezoidBase, self).__init__()
        self.trap_center = trap.center
        self.length = length
        self.azimuth = None
        self.center = None

    def bootstrap_from_adjacent_trap(self, adjacent_trap_center):
        self.azimuth_from_other_trap_center(adjacent_trap_center)
        self.center_from_adjacent_trap(adjacent_trap_center)
        self.find_point_a()
        self.find_point_b()
        self.get_pvectors()

    def bootstrap_from_opposite_trap(self, opposite_trap_center):
        self.azimuth_from_other_trap_center(opposite_trap_center)
        self.center_from_opposite_trap(opposite_trap_center)
        self.find_point_a()
        self.find_point_b()
        self.switch_points()
        self.get_pvectors()

    def switch_points(self):
        point_a = copy.deepcopy(self.point_a)
        self.point_a = self.point_b
        self.point_b = point_a

    def ortho_azimuth(self, other_trap_center):
        # Azimuth of line orthogonal to the divider
        path_ab_e = nvector.diff_positions(self.trap_center, other_trap_center)
        frame_n = nvector.FrameN(self.trap_center)
        path_ab_n = path_ab_e.change_frame(frame_n)
        path_ab_n = path_ab_n.pvector.ravel()
        azimuth = numpy.arctan2(path_ab_n[1], path_ab_n[0])
        return azimuth

    def azimuth_from_other_trap_center(self, other_trap_center):
        # Get azimuth of Base from
        orthogonal_azimuth = self.ortho_azimuth(other_trap_center)
        self.azimuth = orthogonal_azimuth + math.pi/2

    def center_from_adjacent_trap(self, adjacent_trap_center):
        # Center of the divider
        orthogonal_path = nvector.GeoPath(self.trap_center, adjacent_trap_center)
        self.center = orthogonal_path.interpolate(0.5).to_geo_point()

    def center_from_opposite_trap(self, opposite_trap_center):
        orthogonal_path = nvector.GeoPath(self.trap_center, opposite_trap_center)
        self.center = orthogonal_path.interpolate(-0.5).to_geo_point()

    def find_point_a(self):
        point_a, azimuthb = self.center.geo_point(distance=self.length / 2, azimuth=self.azimuth, degrees=False)
        self.point_a = point_a

    def find_point_b(self):
        point_b, azimuthb = self.center.geo_point(distance=-self.length / 2, azimuth=self.azimuth, degrees=False)
        self.point_b = point_b

    def __str__(self):
        lat_a = str(self.point_a().latitude_deg)
        lon_a = str(self.point_a().longitude_deg)
        lat_b = str(self.point_b().latitude_deg)
        lon_b = str(self.point_b().longitude_deg)
        return '{} {} to {} {} length {}'.format(lat_a, lon_a, lat_b, lon_b, self.length)