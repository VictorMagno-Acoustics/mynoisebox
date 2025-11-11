import streamlit as st
import geopandas as gpd
import fiona
import pandas as pd
from shapely.geometry import Point
import numpy as np
import xlsxwriter
from io import BytesIO

fiona.drvsupport.supported_drivers['libkml'] = 'rw' # enable KML support which is disabled by default
fiona.drvsupport.supported_drivers['LIBKML'] = 'rw' # enable KML support which is disabled by default

def app():

    st.title('Toolbox for Noise Mapping')

    st.write("**Available tools:**")
    st.write("- Import measurement points from Google Maps (.kml) to noise mapping.")

    st.markdown('---')

    option = st.selectbox(
   "Which tool will you use?",
   ("Import measurement points from Google Maps"),
   index= None,
   placeholder="Select...",
    )
    st.write("You selected:", option)

    if option == "Import measurement points from Google Maps":

        epsg = st.text_input("Enter your EPSG-SIRGAS2000 code (e.g., 31983)", "")

        uploaded_file = st.file_uploader('Select the KML file of the measurement points', type='kml')
        if uploaded_file:
            st.markdown('---')

            # Lê o arquivo KML
            gdf = gpd.read_file(uploaded_file, driver='LIBKML')

            # Função para dividir as coordenadas em colunas separadas
            def split_coordinates(geometry):

                coords = []

                # Percorre cada ponto na linha
                for point in geometry.coords:
                    longitude, latitude, altitude = point
                    coords.append((longitude, latitude, altitude))
                
                return coords

            # Aplica a função para dividir as coordenadas em colunas separadas
            gdf['coordinates'] = gdf['geometry'].apply(split_coordinates)

            # Cria um novo DataFrame com as colunas divididas
            gdf_exploded = gdf.explode('coordinates')
            gdf_exploded[['longitude', 'latitude', 'altitude']] = pd.DataFrame(gdf_exploded['coordinates'].tolist(), index=gdf_exploded.index)
            gdf_exploded.drop(columns='coordinates', inplace=True)

            ############################### Reordenando formato do Dataframe para ASCII ###############################

            # Reordenando colunas ordem_1
            ordem_1 = ['Name', 'longitude','latitude','altitude']
            SoundPLAN_ASCII = gdf_exploded.reindex(columns=ordem_1)

            ############################### Convertendo Coordenadas para UTM ###############################

            # Convertendo as coordenadas para o formato de ponto do GeoPandas
            geometry = [Point(xy) for xy in zip(SoundPLAN_ASCII['longitude'], SoundPLAN_ASCII['latitude'])]

            # Criando um GeoDataFrame com as coordenadas
            gdf = gpd.GeoDataFrame(SoundPLAN_ASCII, geometry=geometry, crs="EPSG:4326")  # Define o sistema de coordenadas como WGS84 (latitude e longitude)

            # Convertendo para UTM
            gdf_utm = gdf.to_crs(epsg)  # Converte para o sistema de coordenadas UTM zona 23S (por exemplo, 31983)

            # Extraindo as coordenadas UTM (x e y)
            SoundPLAN_ASCII['latitude'] = gdf_utm.geometry.y
            SoundPLAN_ASCII['longitude'] = gdf_utm.geometry.x

            ############################### Exportando para csv ###############################

            # Criar um buffer de memória para salvar o arquivo Excel
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                SoundPLAN_ASCII.to_excel(writer, index=False,
                            sheet_name="Dados Processados")
                writer.close()

            # Preparar o arquivo para download
            output.seek(0)

            # Permitir exportar os dados processados para Excel
            st.download_button(
                label="Download Excel",
                data=output,
                file_name="MyNoiseBox_SoundPLAN_Receiver_Table.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

            st.success('Success!', icon="✅")







    
