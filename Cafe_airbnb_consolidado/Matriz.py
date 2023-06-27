# importando pacotes

import pandas as pd
import requests
import openpyxl

# abrindo os arquivos

airbnb_df = pd.read_excel("Airbnbs.xlsx")
cafes_df = pd.read_excel("lista de cafes.xlsx")
airbnb_end_df = pd.read_excel("airbnbs_com_endereco_excel.xlsx")


# Inserindo API google

chave_google = "AIzaSyCtH6OP6WUR4IhrXVyH52X3m8zlihnFoCo"

# Encontrando endereço dos cafes pelas coordenadas

def obter_endereco(lat, lng, chave_api):
    url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={chave_api}'
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200 and data['status'] == 'OK':
        if len(data['results']) > 0:
            endereco = data['results'][0]['formatted_address']
            return endereco
    return None

latitude = airbnb_df["location/lat"]
longitude = airbnb_df["location/lng"]
api_key = chave_google

enderecos = []

for index, row in airbnb_df.iterrows():
    latitude = row['location/lat']
    longitude = row['location/lng']

    endereco = obter_endereco(latitude, longitude, api_key)
    enderecos.append(endereco)

airbnb_df['Endereço'] = enderecos
airbnb_df.to_excel('airbnbs_com_endereco', index=False, engine='openpyxl')

# Començando as iterações e gerando a matriz

lista_distancia = []

for cafe in cafes_df["Endereço"]:
    lista_cafes = []
    for cord in airbnb_end_df["Endereço"]:
        origem = cord
        destino = cafe
        rota = "https://maps.googleapis.com/maps/api/distancematrix/json?" + 'origins=' + cord + '&destinations='+ cafe +'&key=' + chave_google
        req = requests.get(url=rota)
        req_json = req.json()
        distancia = req_json['rows'][0]['elements'][0]['distance']['value']
        lista_cafes.append(distancia)
    lista_distancia.append(lista_cafes)

matriz = pd.DataFrame(lista_distancia)

matriz.index = cafes_df["Estabelecimento"]
matriz.columns = airbnb_end_df["url"]


matriz.to_excel("distancias_vf.xlsx", index=False)