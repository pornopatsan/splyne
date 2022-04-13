"""
ScatterplotLayer
================
Plot of the number of exits for various subway stops within San Francisco, California.
Adapted from the pydeck documentation.
"""

import math

import pandas as pd
from splyne import scatterplot

SCATTERPLOT_LAYER_DATA = "https://raw.githubusercontent.com/pornopatsan/splyne/main/examples/resources/bart-stations.json"


if __name__ == '__main__':
    df = pd.read_json(SCATTERPLOT_LAYER_DATA)
    df['lon'] = df['coordinates'].apply(lambda x: x[0])
    df['lat'] = df['coordinates'].apply(lambda x: x[1])
    df['exits_radius'] = df['exits'].apply(lambda exits_count: math.sqrt(exits_count))
    df['city'] = df['address'].apply(lambda x: x.split(',')[-1].split('CA')[0])

    scatterplot(data=df, color='city', size='exits_radius')
