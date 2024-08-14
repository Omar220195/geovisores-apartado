import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")

# Customize the sidebar
markdown = """
Desarrollado por Effective Actions
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://github.com/Omar220195/Streamlit-prueba/raw/main/logo.png"
st.sidebar.image(logo)

# Customize page title
st.title("Geovisor operación Apartadó")

st.markdown(
    """
    Se encuentran desplegados los diferentes geovisores para el proyecto de actualización catastral en el municipio de Apartadó
    """
)

st.header("Apartadó")

markdown = """


"""

st.markdown(markdown)

m = leafmap.Map(minimap_control=True, center=[7.882293365998897 , -76.6249929671165],  # Coordinates for Colombia
        zoom=15,  )
m.add_basemap("SATELLITE")
m.to_streamlit(height=700)