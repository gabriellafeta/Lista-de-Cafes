# importando pacotes
import matplotlib.pyplot as plt
import pandas as pd
import openpyxl

# Descobrindo qual airbnb possui a menor distância média aos cafes da lista

matriz = pd.read_excel("distancias_vf.xlsx")
lista_cafes = pd.read_excel("lista de cafes.xlsx")
airbnb_1 = pd.read_excel("airbnbs_com_endereco_excel.xlsx")

# Criando dicionário vazio para agrupar as grandezas de interesse

lista_url = matriz.columns.to_list()
dict_dist = {}

# Definindo indices da matriz para os nomes dos estabelecimentos
id_matriz = matriz.set_index(lista_cafes["Estabelecimento"])

for url in lista_url:
    dict_dist = {
        "URL": lista_url,
        "dist_media": matriz.mean(axis=0).to_list(),
        "dist_min": matriz.min(axis=0).to_list(),
        "estabelecimento": id_matriz.idxmin(axis=0).tolist()
    }

df_url = pd.DataFrame(dict_dist)

# Trazendo outras informações
# Primeiro o preço

df_url["preco diaria"] = None

for index, row in df_url.iterrows():
    url = row["URL"]
    preco_diaria = airbnb_1.loc[airbnb_1["url"] == url, "Preço formatado"].values
    if len(preco_diaria) > 0:
        df_url.at[index, "preco diaria"] = preco_diaria[0]

# Também irei trazer o roomType para plotar algumas análises

df_url["tipo_quarto"] = None

for index, row in df_url.iterrows():
    url = row["URL"]
    tipo_quarto = airbnb_1.loc[airbnb_1["url"] == url, "roomType"].values
    if len(tipo_quarto) > 0:
        df_url.at[index, "tipo_quarto"] = tipo_quarto[0]

# print(df_url.head())
#
# # Exportando o arquivo em excel
# df_url.to_excel("Base_final.xlsx")

# importando a nova base e fazendo algumas analises

base_final = pd.read_excel("Base_final.xlsx")

# Descobrindo o estabelecimento que aparece com a maior frequencia de menor distância

estab_freq = base_final['estabelecimento'].value_counts()
estab_freq.plot(kind="bar", rot=45)
plt.xlabel('Estabelecimentos')
plt.title('Frequência dos estabelecimentos em relação a menor distância')
plt.show()

# Descobrindo qual tipo de quarto

tipo_quart_graf = base_final['tipo_quarto'].value_counts()
tipo_quart_graf.plot(kind="bar", rot=45)
plt.xlabel('Tipo de quarto')
plt.show()

#Afunilando as analises para "Entire rental unit" e vendo se existe correlação entre
#distancia minima e preco medio

base_final[base_final["tipo_quarto"]=="Entire rental unit"]["preco diaria"].hist()
plt.xlabel('Preço diária')
plt.show()

base_final[base_final["tipo_quarto"]=="Entire rental unit"]["dist_min"].hist(alpha=0.7)
plt.xlabel('Distância média [m]')
plt.show()

# Estrtuturando o entregavel final

base_final_only_ert = base_final["tipo_quarto"] == "Entire rental unit"
base_final_ordenada = base_final[base_final_only_ert].sort_values(['preco diaria', 'dist_min'], ascending=[True, True])


print(base_final_ordenada.head())

base_final_ordenada.to_excel("base_final_ordenada.xlsx")