import pydeck


def parse_data(data, lat='lat', lon='lon', color='color'):
    return data


def scatterplot_layer(data):
    layer = pydeck.Layer(
        "ScatterplotLayer",
        data=data,
        pickable=True,
        stroked=True,
        filled=True,
        radius_scale=6,
        radius_min_pixels=10,
        radius_max_pixels=20,
        line_width_min_pixels=1,
        line_width_max_pixels=1,
        get_position=['lat', 'lon'],
        get_radius=2,
        get_fill_color='color',
        get_line_color='color',
    )
    return layer
