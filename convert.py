from glob import glob
from tabula import read_pdf
from pager import *
import pandas as pd

documents = glob('*/*.pdf')

measurement_stations = []

for station_data in documents:

    station = read_pdf(station_data, pages='all', lattice=True, silent=True)

    j = -2

    pages = []

    while (j := j + 3) < len(station):

            pages.append(clean(station, j))

    measurement_stations.append(pd.concat(pages))

vstacked = pd.concat(measurement_stations)

vstacked.to_csv('stations.csv', sep=';', decimal='.')
