import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")

markdown = """
Desarrollado por Effective Actions.
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://github.com/Omar220195/Streamlit-prueba/raw/main/logo.png"
st.sidebar.image(logo)

st.title("Mapa comparación No.pisos 2014-2024.")


st.title("Mapa caracterización")

col1, col2 = st.columns([4, 1])
options = list(leafmap.basemaps.keys())
index = options.index("SATELLITE")

with col2:
    basemap = st.selectbox("Select a basemap:", options, index)

with col1:
    m = leafmap.Map(
        locate_control=True,
        latlon_control=True,
        draw_export=True,
        minimap_control=True,
        center=[7.882293365998897, -76.6249929671165],  # Coordinates for Colombia
        zoom=15,
    )
    m.add_basemap(basemap)
m.split_map(
    left_layer="ESA WorldCover 2020 S2 FCC", right_layer="ESA WorldCover 2020"
        )
m.add_legend(title="ESA Land Cover", builtin_legend="ESA_WorldCover")

m.to_streamlit(height=700)