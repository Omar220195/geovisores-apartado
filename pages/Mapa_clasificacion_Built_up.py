import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import folium

# Define the path to your shapefile
shapefile_path = "https://github.com/Omar220195/Streamlit-prueba/raw/main/year_const.shp" 

# Sidebar configuration
markdown = """
Desarrollado por Effective Actions.
"""

st.sidebar.title("Mapa clasificación Built up")
st.sidebar.info(markdown)
logo = "https://github.com/Omar220195/Streamlit-prueba/raw/main/logo.png"
st.sidebar.image(logo)

# Main title
st.title("Mapa clasificación Built Up")

# Layout configuration
col1, col2 = st.columns([4, 1])
options = list(leafmap.basemaps.keys())
index = options.index("SATELLITE")

with col2:
    basemap = st.selectbox("Select a basemap:", options, index)

with col1:
    # Create the map instance
    m = leafmap.Map(
        center=[7.882293365998897 , -76.6249929671165],  # Coordinates for Colombia
        zoom=13,  
        locate_control=True, latlon_control=True, draw_export=True, minimap_control=True
    )

    # Add basemap
    m.add_basemap(basemap)

    
    # Load the shapefile
    try:
        gdf = gpd.read_file(shapefile_path)

        # Remove rows with null values in 'const_year'
        gdf = gdf[gdf['const_year'].notnull()]

        # Ensure 'const_year' is of type float
        gdf['const_year'] = gdf['const_year'].astype(float)

        # Define colormap and normalization
        colormap = plt.get_cmap('viridis')  # Choose your colormap here
        norm = mcolors.Normalize(vmin=1985, vmax=2024)

        # Function to style each feature
        def style_function(feature):
            const_year = feature['properties']['const_year']
            color = mcolors.to_hex(colormap(norm(const_year)))
            return {
                'fillColor': color,
                'color': color,
                'weight': 1,
                'fillOpacity': 0.7
            }

        # Add the shapefile to the map with styles
        folium.GeoJson(
            gdf,
            style_function=style_function,
            name="Shapefile Layer"
        ).add_to(m)

        # Create a ScalarMappable and add the colorbar
        sm = plt.cm.ScalarMappable(cmap=colormap, norm=norm)
        sm.set_array([])  # You can set an empty array or your data array

        # Create the colorbar
        fig, ax = plt.subplots(figsize=(4, 0.4))  # Adjust size as needed
        cbar = fig.colorbar(sm, cax=ax, orientation="horizontal")
        cbar.set_label("const_year")

        # Save the colorbar as an image
        cbar_image_path = "colorbar.png"
        fig.savefig(cbar_image_path, bbox_inches='tight')

        # Add the colorbar image to the map
        m.add_image(cbar_image_path, layer_name="Colorbar")

    except FileNotFoundError:
        st.error("Shapefile not found. Please check the path.")
    except TypeError as e:
        st.error(f"An error occurred due to a type issue: {e}")
    except Exception as e:
        st.error(f"An error occurred while processing the shapefile: {e}")

    # Render the map in Streamlit
    try:
        m.to_streamlit(height=700)
    except Exception as e:
        st.error(f"An error occurred while rendering the map: {e}")