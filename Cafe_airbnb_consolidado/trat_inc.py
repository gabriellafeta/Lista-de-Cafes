# Importando os pacotes que serão utilizados no projeto
import pandas as pd
import openpyxl
import matplotlib.pyplot as plt

# Importando minha base de dados e transformando em data frame

airbnb_data = pd.read_excel("dataset_airbnb-scraper_2023-06-24_02-26-45-977.xlsx")
airbnb_df = pd.DataFrame(airbnb_data)

# Como a base é muito grande farei um subset apenas com as colunas de interesse
# Criando uma lista com as colunas de interesse

colunas_interesse = ["address", "location/lat", "location/lng", "url", "roomType", "stars",
                     "pricing/rateBreakdown/6/priceFormatted"]

airbnb_df_resumido = airbnb_df[colunas_interesse].copy()

#print(airbnb_df_resumido.shape[0]) -> atualmente com 2749 linhas
# Existem bairros de interesse para a minha análise, por isso criarei uma lista com eles

airbnb_df_resumido[["Bairro", "Complemento"]] = airbnb_df_resumido["address"].str.split(",", n=1, expand=True)

bairros_interesse_lista = ["Vila Olímpia", "Vila Mariana", "Santo Amaro", "Moema", "Vila Madalena"]
bairros_interesse = airbnb_df_resumido["Bairro"].isin(bairros_interesse_lista)

print(airbnb_df_resumido[bairros_interesse].shape[0])
# Criando um novo data frame aplicando os filtros

airbnb_sp = airbnb_df_resumido[bairros_interesse].copy()

# Criando as primeiras estatisticas descritivas
# Contando número de airbnb por bairro e plotando o gráfico

airbnb_por_bairro = airbnb_sp['Bairro'].value_counts()
print(airbnb_por_bairro)
airbnb_por_bairro.plot(kind="bar", rot = 45)
plt.xlabel('Bairro')
plt.ylabel('Airbnbs')
plt.show()

# Tratando a coluna de preços para transformar em float

airbnb_sp["Preço formatado"] = (
    airbnb_sp["pricing/rateBreakdown/6/priceFormatted"]
    .str.lstrip('R$')
    .str.replace(",", ".")
    .astype(float)
)

# Calculando estatísticas descritvas com groupby

medias = airbnb_sp.groupby("Bairro")[["Preço formatado", "stars"]].mean().round(2)
print(medias)

# Histograma por faixa de preço
airbnb_sp["Preço formatado"].hist()
plt.xlabel('Distribuição de preço da diária')
plt.show()


# Removendo outliers de preço
airbnb_sp_vf = airbnb_sp[airbnb_sp["Preço formatado"] > 100]

# Exportar para um novo arquivo Excel
nome_arquivo = "Airbnbs.xlsx"
airbnb_sp_vf.to_excel(nome_arquivo, index=False)
