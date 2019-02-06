import pandas
from pixel_drawer import plots

df = pandas.read_csv('trixel_count_area_plot.csv', sep=';', index_col='HTM Level')
df['Trixel Count'] = df['Trixel Count']/1000

plot = plots.Plot()

plot.plot_pandas(df['Area'])
plot.plot_pandas_second_y(df['Trixel Count'])
plot.y_label('Area \n in \si{\square\kilo\meter}')
plot.y_label2('Count \n (thousands)')
plot.set_xlim(13, 18)
plot.save_fig('../figures/trixel_count_area.png')
plot.save_fig('../figures/trixel_count_area.pdf')
