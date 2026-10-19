import pandas as pd
import pydeck as pdk
import streamlit as st


st.title("Map and Pin")

lat = st.number_input("Latitude (-90 to 90)", min_value=-90.0, max_value=90.0, value=39.75, format="%.2f")
lon = st.number_input("Longitude (-180 to 180)", min_value=-180.0, max_value=180.0, value=-105.00, format="%.2f")

pin_svg = (
    "data:image/svg+xml;utf8,"
    "<svg xmlns='http://www.w3.org/2000/svg' width='128' height='128' viewBox='0 0 24 24'>"
    "<path fill='%23d62728' d='M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"
    "m0 9.5a2.5 2.5 0 0 1 0-5 2.5 2.5 0 0 1 0 5z'/>"
    "</svg>"
)
 
pin = pd.DataFrame({
    "lat": [lat],
    "lon": [lon],
    "icon": [{"url": pin_svg, "width": 128, "height": 128, "anchorY": 128}],
})

layer = pdk.Layer(
    "IconLayer",
    data=pin,
    get_icon="icon",
    get_position="[lon, lat]",
    get_size=4,
    size_scale=12,
)


view = pdk.ViewState(latitude=lat, longitude=lon, zoom=11)

st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view, map_style="road"))


# Used claude Sonnet 5.5 to find pin icon and map, as well as develop code to use these tools. 
# Tested the code by testing multiple lat and lon values to ensure the pin icon was placed correctly
# on the map. Success can be shown in GIF.