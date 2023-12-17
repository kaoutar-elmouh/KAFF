import streamlit as st

import numpy as np
import folium
import plotly.express as px
import altair as alt
from PIL import ImageFont
from rasterio.plot import reshape_as_image
from streamlit_folium import folium_static

import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from ipyleaflet import Map, SplitMapControl, TileLayer

from rasterio.transform import from_origin
from rasterio.enums import Resampling
import rasterio
import imageio
from folium import plugins
from folium.plugins import Geocoder

from io import BytesIO


import leafmap.foliumap as leafmap
import altair as alt
import rasterio as rio
import streamlit as st
from pyproj import Transformer
import folium
from streamlit_folium import folium_static
from branca.colormap import LinearColormap
from rasterio.windows import Window
import tempfile
from PIL import Image, ImageDraw
import imageio
import io
import os




with st.sidebar:
    selected = option_menu(None, ["Home","SplitMap","Timeseries","chart de changement"], 
                       icons=['house','map', 'clock', "bar-chart",'cloud-upload','clock','search','envelope'],                 
                       menu_icon="cast", default_index=0,
                       styles={
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "brown"},
    })


if selected == "Home":
    # Add HTML and CSS for the background GIF
    st.markdown(
        f"""
        <style>
            .background-container {{
                background-image: url('https://assatfatima.github.io/image/Iow4.gif');
                background-size: cover;
                background-position: center;
                height: 100vh;
                margin: 0;
                overflow: hidden;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
            }}

            @keyframes colorChange {{
                0% {{ color: #ff0000; }}
                25% {{ color: #00ff00; }}
                50% {{ color: #0000ff; }}
                75% {{ color: #ff00ff; }}
                100% {{ color: #ff0000; }}
            }}

            h1 {{
                animation: colorChange 5s infinite, bounce 2s infinite;
                color: white;
            }}

            .content {{
                color: white;
            }}
        </style>
        """
        , unsafe_allow_html=True
    )

    # Your Streamlit content goes here
    # Interactive welcome section with animated and colorful title
    st.write(
        """
        <div class="background-container">
            <h1>Welcome to our application</h1>
        </div>
        """, 
        unsafe_allow_html=True
    )

if selected=="SplitMap":
    with st.sidebar:
        selecte = option_menu(None, ["visualisation de changement","visualisation de diffirence entre methode"]) 
    if selecte=="visualisation de changement":
        def main():
            st.markdown("<h1 style='color: #2e07f8; text-align: center;'>Visualisation de changement</h1>", unsafe_allow_html=True)

            annee_attributs = ["2015", "2017", "2018", "2021"]

                # Sélecteur pour l'année à gauche et droit
            left_column, right_column = st.columns(2)

            with left_column:
                left_annee = st.selectbox("Sélectionner l'année à gauche", list(annee_attributs))

            with right_column:
                annees_disponibles = list(annee_attributs)
                annees_disponibles.remove(left_annee)
                right_annee = st.selectbox("Sélectionner l'année à droite", annees_disponibles)

            left_image_url = f"https://fatielkadd.github.io/traitementdesimages/IMAGESFINALE/RandomForest{left_annee}.tif"
            right_image_url = f"https://fatielkadd.github.io/traitementdesimages/IMAGESFINALE/RandomForest{right_annee}.tif"
            m = leafmap.Map(center=[32.71, -5.86], zoom=20)
            col1, col2 = st.columns([2, 1])
            with col2:
              st.write("legende")
              legend_dict = {
                "eau": "#2e07f8",
                "sol nu": "#f9ff02",
                "vegetatio": "#87ff04"
            }

              st.markdown(
                    """
                    <style>
                        .legend {
                            display: flex;
                            flex-direction: column;
                        }

                        .legend-item {
                            display: flex;
                            align-items: center;
                            margin-bottom: 5px;
                        }

                        .legend-color {
                            width: 20px;
                            height: 20px;
                            margin-right: 5px;
                        }
                    </style>
                    """
                , unsafe_allow_html=True)

              st.markdown("<div class='legend'>", unsafe_allow_html=True)
              for label, color in legend_dict.items():
                    st.markdown(
                        f"<div class='legend-item'><div class='legend-color' style='background-color:{color};'></div>{label}</div>",
                        unsafe_allow_html=True
                    )
                    st.markdown("</div>", unsafe_allow_html=True)
            with col1:
                m.split_map(left_image_url, right_image_url)
                m.to_streamlit(height=450)
        if __name__ == "__main__":
            main()
    if selecte=="visualisation de diffirence entre methode":
        def main():
          
          st.markdown("<h1 style='color: #f9ff02; text-align: center;'>visualisation de diffirence entre methode</h1>", unsafe_allow_html=True)
          annee_attribut = ["2015", "2021"]

    # Sélecteurs pour les methode gauche et droit
          annee_key = st.selectbox("Sélectionner une annee", list(annee_attribut))
          left_column, right_column = st.columns(2)
          attributs_annee =["arbredecision", "basederegles", "distanceminimaleenvi","RandomForest","ReseauNeuroneArtificiel","oumrabie"]
          with left_column:
            left_annee = st.selectbox("Sélectionner la methode gauche", list(attributs_annee))

          with right_column:
                annees_disponibles = list(attributs_annee)
                annees_disponibles.remove(left_annee)
                right_annee = st.selectbox("Sélectionner la methode droite", annees_disponibles)

          left_image_url = f"https://fatielkadd.github.io/traitementdesimages/IMAGESFINALE/{left_annee}{annee_key}.tif"
          right_image_url = f"https://fatielkadd.github.io/traitementdesimages/IMAGESFINALE/{right_annee}{annee_key}.tif"
          m = leafmap.Map(center=[32.71, -5.86], zoom=20)
                
            # Custom legend
          col1, col2 = st.columns([2, 1])
          with col2:
              st.write("legende")
              legend_dict = {
                "eau": "#2e07f8",
                "sol nu": "#f9ff02",
                "vegetatio": "#87ff04"
            }

              st.markdown(
                    """
                    <style>
                        .legend {
                            display: flex;
                            flex-direction: column;
                        }

                        .legend-item {
                            display: flex;
                            align-items: center;
                            margin-bottom: 3px;
                        }

                        .legend-color {
                            width: 20px;
                            height: 20px;
                            margin-right: 5px;
                        }
                    </style>
                    """
                , unsafe_allow_html=True)

              st.markdown("<div class='legend'>", unsafe_allow_html=True)
              for label, color in legend_dict.items():
                    st.markdown(
                        f"<div class='legend-item'><div class='legend-color' style='background-color:{color};'></div>{label}</div>",
                        unsafe_allow_html=True
                    )
                    st.markdown("</div>", unsafe_allow_html=True)
          with col1:          
            try:
                m.split_map(left_image_url, right_image_url)

                m.to_streamlit(height=450)
            except Exception as e:
                st.error(f"Error: {e}")
        if __name__ == "__main__":
            main()
if selected=="Timeseries":
    st.markdown("<h2 style='font-size:32px;color: #f9ff02; text-align:center;'>TIMELAPSE </h2>", unsafe_allow_html=True)
    col1, col2 = st.columns([5, 1])
    with col1:    
        # Dossier de sortie pour les timelapses
        output_folder = "timelapses"
        os.makedirs(output_folder, exist_ok=True)
        attributs = ['RandomForest']
        def download_image(url):
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    return response.content
                else:
                    st.error(f"Échec du téléchargement de l'image depuis {url}. Code d'erreur : {response.status_code}")
                    return None
            except Exception as e:
                st.error(f"Erreur lors du téléchargement de l'image depuis {url}. Erreur : {str(e)}")
                return None

        def create_timelapse(attribute, DAY_names, duration, gif_size=(256, 240)):
            images = []
            for i in DAY_names:
                url = f"https://fatielkadd.github.io/traitementdesimages/IMAGESFINALE/{attribute}{i}.tif"
                image_content = download_image(url)

                if image_content:
                    with rasterio.open(BytesIO(image_content), driver='GTiff') as src:
                        # Lire les données raster
                        raster_data = src.read()

                        # Convertir en image PIL
                        image_data = Image.fromarray(reshape_as_image(raster_data))

                        # Créer un objet de dessin
                        draw = ImageDraw.Draw(image_data)

                        font_size = 24  # Adjust the font size as needed

                        # Charger une police avec la taille spécifiée
                        font = ImageFont.truetype("arial.ttf", font_size)

                        # Annoter chaque image avec les noms des jours
                        draw.text((60, 60), f'{attribute} jour {i}', fill='black', font=font)

                        # Ajouter l'image annotée à la liste
                        images.append(np.array(image_data))

            if images:
                # Générer le GIF à partir des images annotées
                gif_filename = f'timelapse_{attribute}.gif'
                with imageio.get_writer(gif_filename, mode='I', duration=duration, loop=0, size=gif_size) as writer:
                    for image in images:
                        writer.append_data(image)

                return gif_filename
            else:
                return None

        # Liste des noms de jours
        DAY_names = [2015, 2017, 2018, 2021]
        duration = 350
        maroc_coordinates = {
            "latitude": [27.6664, 35.9225],  # Latitude du bas et du haut
            "longitude": [-17.0205, -1.1256]  # Longitude de la gauche et de la droite
        }

        # Utiliser la première image pour définir les limites
        first_image_url = f"https://fatielkadd.github.io/traitementdesimages/IMAGESFINALE/{attributs[0]}{DAY_names[0]}.tif"
        first_image_content = download_image(first_image_url)

        if first_image_content:
            with rasterio.open(BytesIO(first_image_content), driver='GTiff') as src:
                # Lire les données raster
                raster_data = src.read()

                # Convertir en image PIL
                first_image_data = Image.fromarray(reshape_as_image(raster_data))
                gif_size = (256, 240)
                bounds = [
                    [maroc_coordinates["latitude"][0], maroc_coordinates["longitude"][0]],
                    [maroc_coordinates["latitude"][1], maroc_coordinates["longitude"][1]]
                ]

                # Créer les timelapses pour chaque attribut
                gif_filename = create_timelapse(attributs[0], DAY_names, duration)
                
                if gif_filename:
                        # Reste du code pour afficher la carte avec Folium
                        m = folium.Map(location=[32.73, -5.86], zoom_start=12.4)

                        bounds_morocco = [
                            [32.76543856,-5.81236995],  # Coin supérieur droit (nord-ouest)
                            [32.68876521,-5.90718824]   # Coin inférieur gauche (sud-est)
                        ]
                        gif_layer = folium.raster_layers.ImageOverlay(
                            gif_filename,
                            bounds=bounds_morocco,
                            opacity=0.7,
                            name=f'GIF Layer - {attributs[0]}'
                        ).add_to(m)
                        folium.LayerControl().add_to(m)
                    
                        folium_static(m, width=700, height=450)

                        # Vous pouvez utiliser st.success pour informer l'utilisateur que les GIF ont été créés
                else:
                    st.error("Aucune image disponible pour créer le timelapse.")
        else:
            st.error("Aucune image disponible pour définir les limites.")
if selected=="chart de changement": 
 


    # Data
    years = [2015, 2017, 2018, 2021]
    categories = ['eau', 'vegetation', 'solnu']
    values = {
        2015: {'eau': {'Percentage': 25.05, 'Area': 19000000},
            'vegetation': {'Percentage': 44.76, 'Area': 33953200},
            'solnu': {'Percentage': 30.2, 'Area': 22908800}},
        2017: {'eau': {'Percentage': 22.77, 'Area': 17273600},
            'vegetation': {'Percentage': 33.23, 'Area': 25211600},
            'solnu': {'Percentage': 44, 'Area': 33376800}},
        2018: {'eau': {'Percentage': 19.25, 'Area': 14601200},
            'vegetation': {'Percentage': 33.06, 'Area': 25078000},
            'solnu': {'Percentage': 47.7, 'Area': 36182800}},
        2021: {'eau': {'Percentage': 12.25, 'Area': 9292400},
            'vegetation': {'Percentage': 24.71, 'Area': 18746000},
            'solnu': {'Percentage': 63.04, 'Area': 47823600}},
    }

    # Image URL from GitHub
    image_url = 'https://fatielkadd.github.io/traitementdesimages/cartechangement.jpeg'

    # Create Streamlit app layout
    st.markdown("<h2 style='font-size:32px;color: #f9ff02; text-align:center;'>Change Detection Results Over the Years </h2>", unsafe_allow_html=True)
    # Columns for layout

    # Column 1 - Carte de changement and Bar Chart (Area)
   
    st.subheader('Carte de changement')
        # Display change image
    st.image(image_url, caption='Change Image', use_column_width=True)

        
    st.write('Bar Chart (Area)')
    
        
    fig_area = px.bar()
    custom_colors = ['#2e07f8', '#f9ff02', '#87ff04']  # Specify your custom colors here
    for i, category in enumerate(categories):
            fig_area.add_bar(x=years, y=[values[year][category]['Area'] for year in years],
                            name=f'{category} - Area [metre^2]', marker_color=custom_colors[i])
    fig_area.update_layout(barmode='group', xaxis_title='Year', yaxis_title='Area [metre^2]', legend_title='Category')
    st.plotly_chart(fig_area)
    
    st.subheader('Pie Chart (Percentage)')
        
        # Create a list of Pie Charts for each year
    pie_charts = []

        # Loop through each year
    for year in years:
            # Create a pie chart for the current year
        pie_chart = px.pie(names=categories,
                            values=[values[year][category]['Percentage'] for category in categories],
                            title=f'Percentage Distribution in {year}',
                            color_discrete_sequence=custom_colors)

            # Append the pie chart to the list
        pie_chart.update_layout(width=300, height=300)
        pie_charts.append(pie_chart)
    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(pie_charts[0])
        st.plotly_chart(pie_charts[2])

    with col4:
        st.plotly_chart(pie_charts[1])
        st.plotly_chart(pie_charts[3])

       
                


    