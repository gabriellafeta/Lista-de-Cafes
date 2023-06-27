# Lista-de-Cafes

Tenho uma amiga que precisa ir à São Paulo constantemente a trabalho e acaba ficando refém dos preços de airbnb de última hora, além de não saber se seus cafés favoritos estão perto de onde ela vai passar as noite. O intuito do projeto é gerar uma base de dados contendo uma lista com os airbnb's dos bairros que ela frequenta, contendo a média da distância de uma lista de cafés prestigiados de SP, o estabelecimento mais perto e o preço da diária do airbnb.

## Início da modelagem

A base de dados utilizada foi extraída do [Apify](https://console.apify.com/) , que com poucos cliques podemos exportar uma base robusta contendo informações sobre moradias para aluguel em determinada cidade e em determinado período, no caso São Paulo. O arquivo gerado tem o nome de 'dataset_airbnb-scraper_2023-06-24_02-26-45-977'.

Importando os pacotes

```
import pandas as pd
import openpyxl
import matplotlib.pyplot as plt
```

Importando minha base de dados e transformando em data frame

```
airbnb_data = pd.read_excel("dataset_airbnb-scraper_2023-06-24_02-26-45-977.xlsx")
airbnb_df = pd.DataFrame(airbnb_data)
```
Como a base é grandes farei um subset coletando apenas as colunas de interesse

```
colunas_interesse = ["address", "location/lat", "location/lng", "url", "roomType", "stars",
                     "pricing/rateBreakdown/6/priceFormatted"]

airbnb_df_resumido = airbnb_df[colunas_interesse].copy()
print(airbnb_df_resumido.shape[0]) # -> atualmente com 2749 linhas
```
- As colunas escolhidas foram:
    - address: Contém o Bairro e a cidade
    - location/lat: coordenadas em latitude
    - location/lng: coordenadas em longitude
    - url: Link para o anúncio
    - roomType: Tipo do quarto
    - stars: Classificação
    - pricing/rateBreakdown/6/priceFormatted: Preço da diária formatado em R$

Existem bairros de interesse para a minha análise, por isso criarei uma lista com eles

```
airbnb_df_resumido[["Bairro", "Complemento"]] = airbnb_df_resumido["address"].str.split(",", n=1, expand=True)

bairros_interesse_lista = ["Vila Olímpia", "Vila Mariana", "Santo Amaro", "Moema", "Vila Madalena"]
bairros_interesse = airbnb_df_resumido["Bairro"].isin(bairros_interesse_lista)

print(airbnb_df_resumido[bairros_interesse].shape[0])

```

Criando um novo data frame aplicando os filtros

```
airbnb_sp = airbnb_df_resumido[bairros_interesse].copy()
```

Agora irei o levantamento das primeiras grandezas de interesse, começando pelo gráfico da distribuição de airbnbs por bairro.

```
airbnb_por_bairro = airbnb_sp['Bairro'].value_counts()
print(airbnb_por_bairro)
airbnb_por_bairro.plot(kind="bar", rot = 45)
plt.xlabel('Bairro')
plt.ylabel('Airbnbs')
plt.show()
```

<img src="Cafe_airbnb_consolidado/Imagens/novo graf.png"
   width="600"
     height="400">

Percebi que para extratir informações da coluna de preços seria necessário aplicar uma formatação para convertê-lo em float.
```
airbnb_sp["Preço formatado"] = (
    airbnb_sp["pricing/rateBreakdown/6/priceFormatted"]
    .str.lstrip('R$')
    .str.replace(",", ".")
    .astype(float)
)
```
Calculando agrupamentos por bairro
```
medias = airbnb_sp.groupby("Bairro")[["Preço formatado", "stars"]].mean().round(2)
print(medias)
<img src="Cafe_airbnb_consolidado/Imagens/novo graf.png"
   width="600"
     height="400">

```
