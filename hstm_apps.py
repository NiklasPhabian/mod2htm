import subprocess
import nvector
import constants

bin_folder = '../hstm/'
earth = nvector.FrameE(a=constants.earth_radius, f=0)


class IntersectionProcess:

    def __init__(self, level, symbol=False, keepalive=False, interior=False):
        self.level = level
        self.symbol = symbol
        self.process = None
        self.interior = interior
        self.keepalive = keepalive
        self.start_process()

    def kill(self):
        self.process.kill()

    def start_process(self):
        bin = 'simpleIntersect'
        command = [bin_folder + bin, '--quiet', '--latlon']
        if self.keepalive:
            command.append('--keepalive')
        if self.symbol:
            command.append('--symbolic')
        if self.interior:
            command.append('--interior')
        command.append('--searchlevel')
        command.append(str(self.level))
        self.process = subprocess.Popen(command,
                                        stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE,
                                        universal_newlines=True,
                                        bufsize=1)

    def intersect(self, corners):
        htmids = []
        corner_string = ''
        for corner in corners:
            corner_string += '{lat} {lon} '.format(lat=corner[0], lon=corner[1])
        self.process.stdin.write(corner_string + '\n')
        while True:
            line = self.process.stdout.readline().replace('\n', '')
            if line == 'done':
                break
            else:
                htmids.append(int(line))
        if not self.keepalive:
            self.process.kill()
        return htmids


class CornerLookupProcess:
    def __init__(self):
        pass


def simple_intersect(corners, level, symbol=False, interior=False):
    p = IntersectionProcess(level=level, symbol=symbol, keepalive=False, interior=interior)
    return p.intersect(corners)


def lookup_corners(symbol=None, id=None):
    bin = 'lookupCorners'
    if symbol is not None:
        command = (bin_folder+bin, '--quiet', '--latlon', '--symbol', symbol)
    elif id is not None:
        command = (bin_folder+bin, '--quiet', '--latlon', '--id', str(id))
    popen = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
    output = popen.communicate()[0].replace('\n', ' ').split(' ')
    corner1 = nvector.GeoPoint(float(output[0]), float(output[1]), degrees=True)
    corner2 = nvector.GeoPoint(float(output[2]), float(output[3]), degrees=True)
    corner3 = nvector.GeoPoint(float(output[4]), float(output[5]), degrees=True)
    return corner1, corner2, corner3


def name2id(symbol):
    bin = 'lookupCorners'
    command = (bin_folder+bin, '--quiet', '--nocorner', '--symbol', symbol)
    popen = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
    output = popen.communicate()[0].replace('\n', ' ').split(' ')
    id = int(output[0])
    return id


def id2name(id):
    bin = 'lookupCorners'
    command = (bin_folder + bin, '--quiet', '--nocorner', '--id', str(id))
    popen = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
    output = popen.communicate()[0].replace('\n', ' ').split(' ')
    name = output[0]
    return name


if __name__ == '__main__':
    p = IntersectionProcess(level=5)
    p.start_process()
    corners = [(86.877796556100009, 26.1078377931), (86.843174588699995, 26.611282689999999), (86.888995656500001, 26.367022696700001), (86.8544436488, 26.869226976100002)]
    p.intersect(corners)
    p.intersect(corners)


