import constants
import theoretical_pixel
from pixel_drawer import plots
import mod09File


def generate_lookup_table():
    tmp = []
    for scan in range(0, int(constants.n_scans/2)):
        trapezoid = theoretical_pixel.TheoreticalPixel()
        trapezoid.set_scan(scan)
        area = trapezoid.trapezoid_area()
        tmp.append(area)
    lookup = []
    for entry in reversed(tmp):
        lookup.append(entry)
    for entry in(tmp):
        lookup.append(entry)
    return lookup


def length_plots():
    areas = []
    angles = []
    scan_size = []
    track_size = []
    for scan in range(int(constants.n_scans/2), int(constants.n_scans)):
        trapezoid = theoretical_pixel.TheoreticalPixel()
        trapezoid.set_scan(scan)
        areas.append(trapezoid.trapezoid_area()/1000/1000)
        scan_size.append(trapezoid.scan_size()/1000)
        track_size.append(trapezoid.center_length()/1000)
        angles.append(trapezoid.center_view_angel)
    plt = plots.Plot()
    plt.plot(angles, scan_size, 'Along-scan pixel length')
    plt.plot(angles, track_size, 'Along-track pixel length')
    plt.add_arrows()
    plt.x_label('scan angle in \si{\degree}')
    plt.y_label('size \n in km')
    plt.save_fig('../figures/pixel_lengths.png')
    plt.save_fig('../figures/pixel_lengths.pdf')

    plt = plots.Plot()
    plt.plot(angles, areas, 'Pixel area')
    plt.add_arrows()
    plt.x_label('scan angle in \si{\degree}')
    plt.y_label('area \n in km^2')
    plt.save_fig('../figures/pixel_area.pdf')
    plt.save_fig('../figures/pixel_area.png')


def plot_scan_comparison():
    filename = '../../test_data/MYD09.A2017320.0800.006.2017322021802.hdf'  # Himalaya
    mod09 = mod09File.Mod09File(filename)
    pixels = mod09.to_trapezoid_list(n_tracks=1, n_scans=constants.n_scans)
    real_scan_size = []
    angles = []
    scan_size = []
    for scan in range(0, int(constants.n_scans)):
        pixel = pixels[scan]
        pixel.bootstrap()
        pixel.find_height()
        pixel.find_width()
        real_scan_size.append(pixel.height / 1000)

        trapezoid = theoretical_pixel.TheoreticalPixel()
        trapezoid.set_scan(scan)
        scan_size.append(trapezoid.scan_size() / 1000)
        angles.append(trapezoid.center_view_angel)

    plt = plots.Plot()
    plt.set_font_size(16)
    plt.plot(angles, real_scan_size, 'Actual along-scan pixel length')
    plt.plot(angles, scan_size, 'Theoretical along-scan pixel length')
    plt.add_arrows()
    plt.x_label('scan angle in \si{\degree}')
    plt.y_label('size \n in km')
    plt.save_fig('../figures/lengths/comparison_scan.pdf')
    plt.save_fig('../figures/lengths/comparison_scan.png')


def plot_track_comparison():
    filename = '../../test_data/MYD09.A2017320.0800.006.2017322021802.hdf'  # Himalaya
    mod09 = mod09File.Mod09File(filename)
    pixels = mod09.to_trapezoid_list(n_tracks=3, n_scans=constants.n_scans)
    real_track_size = []
    for n_pixel in range(constants.n_scans, constants.n_scans*2):
        pixel = pixels[n_pixel]
        pixel_prev = pixels[n_pixel-constants.n_scans]
        pixel_next = pixels[n_pixel + constants.n_scans]
        width1, _azia, _azib = pixel.center.distance_and_azimuth(pixel_prev.center)
        width2, _azia, _azib = pixel.center.distance_and_azimuth(pixel_next.center)
        real_track_size.append((width1+width2)/2/1000)

    track_size = []
    angles = []
    for scan in range(0, int(constants.n_scans)):
        trapezoid = theoretical_pixel.TheoreticalPixel()
        trapezoid.set_scan(scan)
        track_size.append(trapezoid.center_length() / 1000)
        angles.append(trapezoid.center_view_angel)

    plt = plots.Plot()
    plt.set_font_size(16)
    plt.plot(angles, real_track_size, 'Actual along-track pixel length')
    plt.plot(angles, track_size, 'Theoretical along-track pixel length')

    plt.add_arrows()
    plt.x_label('scan angle in \si{\degree}')
    plt.y_label('size \n in km')
    plt.setup_plot()
    plt.save_fig('../figures/lengths/comparison_track.pdf')
    plt.save_fig('../figures/lengths/comparison_track.png')


if __name__ == '__main__':
    length_plots()
    plot_scan_comparison()
    plot_track_comparison()


