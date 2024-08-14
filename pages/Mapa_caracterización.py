import streamlit as st
import leafmap.foliumap as leafmap

markdown = """
Desarrollado por Effective Actions.
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://github.com/Omar220195/Streamlit-prueba/raw/main/logo.png"
st.sidebar.image(logo)


st.title("Mapa caracterización")

col1, col2 = st.columns([4, 1])
options = list(leafmap.basemaps.keys())
index = options.index("OpenTopoMap")

with col2:

    basemap = st.selectbox("Select a basemap:", options, index)


with col1:

    m = leafmap.Map(
        locate_control=True, latlon_control=True, draw_export=True, minimap_control=True, center=[7.882293365998897 , -76.6249929671165],  # Coordinates for Colombia
        zoom=13,
    )
    m.add_basemap(basemap)
    m.to_streamlit(height=700)
