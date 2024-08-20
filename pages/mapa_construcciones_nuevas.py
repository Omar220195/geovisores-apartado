import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd
import folium

st.set_page_config(layout="wide")

# Define the path to your shapefiles
shapefile_path_terreno = "https://github.com/Omar220195/geovisores-apartado/raw/main/shape_salida_area.shp"

# Load the shapefiles using geopandas
try:
    terreno_gdf = gpd.read_file(shapefile_path_terreno)
except Exception as e:
    st.error(f"Error loading shapefile: {e}")
    st.stop()

# Convert Timestamp columns to string
for col in terreno_gdf.select_dtypes(include='datetime64').columns:
    terreno_gdf[col] = terreno_gdf[col].astype(str)

markdown = """
Desarrollado por Effective Actions.
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://github.com/Omar220195/Streamlit-prueba/raw/main/logo.png"
st.sidebar.image(logo)

st.title("Mapa construcciones nuevas comuna 3")

col1, col2 = st.columns([4, 1])
options = list(leafmap.basemaps.keys())
index = options.index("SATELLITE")

with col2:
    basemap = st.selectbox("Select a basemap:", options, index)

with col1:
    # Create the map instance
    m = leafmap.Map(
        center=[7.8787, -76.6269],  # Coordinates for Colombia
        zoom=15,
        locate_control=True, latlon_control=True, draw_export=True, minimap_control=True
    )

    # Add basemap
    m.add_basemap(basemap)

    # Define a function to style the features based on the 'clasificac' attribute
    def style_function(feature):
        clasificacion = feature['properties'].get('clasificac', '')
        if clasificacion == 'aumentó':
            return {
                'fillColor': 'yellow',
                'color': 'yellow',
                'weight': 1,
                'fillOpacity': 0.7
            }
        elif clasificacion == 'nueva construcción':
            return {
                'fillColor': 'red',
                'color': 'red',
                'weight': 1,
                'fillOpacity': 0.7
            }
        elif clasificacion == 'demolición total':
            return {
                'fillColor': 'purple',
                'color': 'purple',
                'weight': 1,
                'fillOpacity': 0.7
            }
        else:
            return {
                'fillColor': 'lightgrey',
                'color': 'lightgrey',
                'weight': 1,
                'fillOpacity': 0.7
            }

    # Define a function to create popups with specific fields
    def create_popup(feature):
        properties = feature['properties']
        popup_content = '<br>'.join([
            f'Dirección: {properties.get("Direccion", "N/A")}',
            f'Área 2014: {properties.get("area_2014", "N/A")}',
            f'Área 2024: {properties.get("area_2024", "N/A")}',
            f'Diferencia Área: {properties.get("diff_area", "N/A")}',
            f'Clasificación: {properties.get("clasificac", "N/A")}'
        ])
        return folium.Popup(popup_content, max_width=300)

    # Create a folium.FeatureGroup for the GeoJSON layer
    terreno_layer = folium.FeatureGroup(name='Terreno')

    # Create GeoJSON layer with style and popup
    geojson_layer = folium.GeoJson(
        terreno_gdf,  # Use GeoJSON string directly
        style_function=style_function,
        # Use the custom create_popup function to handle popups
        popup=folium.GeoJsonPopup(fields=[
            'Direccion', 'area_2014', 'area_2024', 'diff_area', 'clasificac'
        ])
    )

    # Add GeoJSON layer to the feature group
    geojson_layer.add_to(terreno_layer)

    # Add the feature group to the map
    terreno_layer.add_to(m)

    # Add a legend to the map
    legend_html = """
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 250px; height: 180px; 
                border:2px solid grey; background-color:white; 
                z-index:9999; font-size:14px;
                ">
    <b>Leyenda</b><br>
    <i style="background: yellow; width: 24px; height: 24px; display: inline-block;"></i> Predio con aumento en area<br>
    <i style="background: red; width: 24px; height: 24px; display: inline-block;"></i> Nueva construccion<br>
    <i style="background: purple; width: 24px; height: 24px; display: inline-block;"></i> Demolicion total<br>
    <i style="background: lightgrey; width: 24px; height: 24px; display: inline-block;"></i> Sin cambios considerables<br>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    # Add layer control
    folium.LayerControl().add_to(m)

    # Render the map in Streamlit
    try:
        m.to_streamlit(height=700)
    except Exception as e:
        st.error(f"An error occurred while rendering the map: {e}")
