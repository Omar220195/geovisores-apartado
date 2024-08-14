import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd
import folium

st.set_page_config(layout="wide")

# Define the path to your shapefiles
shapefile_path_vias = "https://github.com/Omar220195/geovisores-apartado/raw/main/Street.shp" 
shapefile_path_manzanas = "https://github.com/Omar220195/geovisores-apartado/raw/main/Block3.shp"

# Load the shapefiles using geopandas
vias_gdf = gpd.read_file(shapefile_path_vias)
manzanas_gdf = gpd.read_file(shapefile_path_manzanas)

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
    
    # Add the shapefiles to the map with the specified styles using Folium
    
    # Convert GeoDataFrames to GeoJSON
    vias_geojson = vias_gdf.to_json()
    manzanas_geojson = manzanas_gdf.to_json()

    # Create a folium.FeatureGroup for each GeoJSON layer
    vias_layer = folium.FeatureGroup(name='Calles')
    folium.GeoJson(
        vias_geojson,
        style_function=lambda feature: {
            'color': 'red',
            'opacity': 0.5
        }
    ).add_to(vias_layer)
    
    manzanas_layer = folium.FeatureGroup(name='Manzanas')
    folium.GeoJson(
        manzanas_geojson,
        style_function=lambda feature: {
            'color': 'yellow',
            'opacity': 0.5
        }
    ).add_to(manzanas_layer)
    
    # Add the layers to the map
    vias_layer.add_to(m)
    manzanas_layer.add_to(m)

    # Add layer control
    folium.LayerControl().add_to(m)

    m.to_streamlit(height=700)
