import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from streamlit_option_menu import option_menu

def drawMap():
    chart_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

    st.pydeck_chart(pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=37.76,
            longitude=-122.4,
            zoom=11,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
            'HexagonLayer',
            data=chart_data,
            get_position='[lon, lat]',
            radius=200,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
            ),
            pdk.Layer(
                'ScatterplotLayer',
                data=chart_data,
                get_position='[lon, lat]',
                get_color='[200, 30, 0, 160]',
                get_radius=200,
            ),
        ],
    ))

def sidebar():
    with st.sidebar:
        selected = option_menu("Main Menu", ["home", "settings"], icons=['house','gear'], menu_icon="cast", default_index=1)
        selected

def main():
    st.title("OptiRoute")
    sidebar()
    drawMap()

if __name__ == "__main__":
    main()