**Geo Visualisation Library (in progress)**

*Splyne* is a python library for quick interactive visualisation of Geo Data. It uses [Pydeck](https://pydeck.gl) to draw objects, automatically fills some fields and provides more simple api. It is designed for quickly drawing things, but instead is less flexible than Pydeck. The goal is to make drawing on interactive maps as easy as drawing in matplotlib, where everything is precalculated, filled with default values and easy to use.


*Example*: here is comparision of code in Pydeck and Splyne:

Given the following points:
```python
import pandas as pd
df = pd.DataFrame([
    {'lat': 55.7, 'lon': 37.8, 'key': 1},
    {'lat': 56.4, 'lon': 35.9, 'key': 2},
    {'lat': 55.7, 'lon': 38.9, 'key': 2},
    {'lat': 55.9, 'lon': 34.2, 'key': 1},
    {'lat': 53.3, 'lon': 36.4, 'key': 3},
    {'lat': 55.9, 'lon': 37.7, 'key': 2},
    {'lat': 54.9, 'lon': 38.0, 'key': 1},
])
```

<table>
<tr> 
    <th> Pydeck </th> <th> Splyne </th>
</tr>
<tr>
<td valign="top">

```python
import pydeck

colors = {
    1: [255, 0, 0],
    2: [0, 255, 0],
    3: [0, 0, 255],
}
df['color'] = df['key'].apply(lambda x: colors[x])

# Note that zoom should be chosen manually
initial_view_state = pydeck.ViewState(
    latitude=center.lat,
    longitude=center.lon,
    bearing=0, pitch=0,
    zoom=11,
)

scatterplot_layer = pydeck.Layer(
    "ScatterplotLayer",
    data=data,
    get_position=['lon', 'lat'],
    get_coloor=['color'],
    pickable=True,
    stroked=True,
    filled=True,
    get_radius=100,
    radius_scale=10,
    radius_min_pixels=10,
    radius_max_pixels=10,
    line_width_min_pixels=1,
    line_width_max_pixels=1,
)

deck = pydeck.Deck(
    layers=[scatterplot_layer],
    initial_view_state=initial_view_state,
    map_style="light",
)

deck.to_html('tmp.html')
```
    
</td>
<td valign="top">
    
```python
import splyne

splyne.scatterplot(data=df, color='key')
```
    
</td>
</tr>
</table>
