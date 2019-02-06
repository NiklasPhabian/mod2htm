import datetime
import nvector
import hstm_apps
from matplotlib.patches import Polygon


class Trixel:

    def __init__(self, level=None, symbol=None, id=None):
        self.level = level
        self.id = id
        self.symbol = symbol
        self.corner1 = None
        self.corner2 = None
        self.corner3 = None
        self.lat = None
        self.lon = None

    def area(self):
        base = nvector.GeoPath(self.corner1, self.corner2)
        base_length = abs(base.track_distance(method='greatcircle').ravel()[0])
        height = abs(base.cross_track_distance(self.corner3, method='greatcircle').ravel()[0])
        area = 0.5 * height * base_length / 1000 / 1000
        return area

    def bootstrap(self):
        if self.id is not None:
            self.bootstrap_from_id()
        elif self.symbol is not None:
            self.bootstrap_from_symbolic()
        elif self.lat:
            self.bootstrap_from_coord()

    def bootstrap_from_id(self):
        self.corner1, self.corner2, self.corner3 = hstm_apps.lookup_corners(id=self.id)

    def bootstrap_from_symbolic(self):
        self.corner1, self.corner2, self.corner3 = hstm_apps.lookup_corners(symbol=self.symbol)

    def symbol_from_id(self):
        pass

    def get_id(self):
        if self.id is None:
            self.id = hstm_apps.name2id(self.symbol)
        return self.id

    def get_symbol(self):
        if self.symbol is None:
            self.symbol = hstm_apps.id2name(self.id)
        return self.symbol

    def bootstrap_from_coord(self):
        self.get_id()
        self.bootstrap_from_id()

    def plot(self, fig, color=None):
        if color is not None:
            fig.set_color(color)
        fig.plot_straight_line_from_nvector(self.corner1.to_nvector().normal, self.corner2.to_nvector().normal)
        fig.plot_straight_line_from_nvector(self.corner2.to_nvector().normal, self.corner3.to_nvector().normal)
        fig.plot_straight_line_from_nvector(self.corner1.to_nvector().normal, self.corner3.to_nvector().normal)

    def __str__(self):
        if self.symbol is not None:
            return self.symbol
        else:
            return str(self.id)

    def corners(self):
        return ((self.corner1.longitude_deg, self.corner1.latitude_deg),
                (self.corner2.longitude_deg, self.corner2.latitude_deg),
                (self.corner3.longitude_deg, self.corner3.latitude_deg))

    def print_corner_coords(self):
        ret = str(self.corner1) + '\n' \
            + str(self.corner2) + '\n' \
            + str(self.corner3) + '\n'
        print(ret)


class VisTrixel(Trixel):

    def get_range_symbol(self, level):
        self.get_symbol()
        low_symbol = self.symbol + '0' * (level-self.level)
        high_symbol = self.symbol + '3' * (level-self.level)
        return low_symbol, high_symbol

    def get_range_id(self, level):
        low_symbol, high_symbol = self.get_range_symbol(level)
        low_id = hstm_apps.name2id(low_symbol)
        high_id = hstm_apps.name2id(high_symbol)
        return low_id, high_id

    def bootstrap(self):
         Trixel.bootstrap(self)

    def to_polygon(self, color):
        if sum(color) == 0.0:
            color = 'white'
        return Polygon(self.corners(), facecolor=color)


if __name__ == '__main__':
    # Get corners from coordinates
    start = datetime.datetime.now()
    t = Trixel(level=10)
    for lon in range(0, 1000):
        t.from_coord_interactive(lat=70, lon=lon)
    print(datetime.datetime.now() - start)

    # Get corners from symbol
    start = datetime.datetime.now()
    t = Trixel(level=10)
    t.bootstrap_from_symbolic('N30120300')

