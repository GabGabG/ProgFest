import pandas as pd
import os

#################################################################################################################
# Attention, il se peut que des noms soient de trop (par exemple un autre P. Desrosiers qui n'est pas Patrick)  #
# dans les fichiers, tout comme il se peut qu'il manque des publications. On ne fait pas la distinction entre   #
# les papiers dont les auteurs étaient peut-être étudiants ou les papiers dont les auteurs sont professeurs.    #
# Le tri entre les publications qui n'ont pas rapport se fait naturellement (il n'y a pas 2 P. Desrosiers qui   #
# ont fait une publication avec D. Côté!)                                                                       #
# Attention: un tri manuel a été fait dans "liens.csv" par après, ne pas toucher au fichier                     #
#################################################################################################################

profs = ["Allard, A", "Allen, C", "Archambault, L", "Beaulieu, L", "Bernier, M", "Cote, D", "Desjardins, M",
         "Despres, P", "Desrosiers, P", "Drissen, L", "Fortin, JF", "Galstian, T", "Joncas, G", "Knystautas, E",
         "Marleau, L", "Martel, H", "McCarthy, N", "Messaddeq, Y", "Piche, M", "Rainville, S", "Robert, C",
         "Thibault, S", "Vallee, R", "Witzel, B"]

dataframes = []
cwd = os.getcwd()
all_files = os.listdir(cwd)
for file in all_files:
    full_file = os.path.join(cwd, file)
    if full_file.endswith(".xls"):
        df = pd.read_excel(full_file)
        dataframes.append(df)
all_data = pd.concat(dataframes)

cols_to_keep = ("Authors", "Article Title", "Times Cited, All Databases")

data: pd.DataFrame = all_data.loc[:, cols_to_keep]
# print(data)
data.to_csv("tout_le_monde.csv")

liens = set()

for i, auteurs in enumerate(data.iloc[:, 0]):
    auteurs = str(auteurs)
    auteurs = auteurs.split(";")
    lien = []
    liste_auteurs = []
    for auteur in auteurs:
        for prof in profs:
            if prof in auteur:
                liste_auteurs.append(prof)
    liste_auteurs.sort()
    lien.append(tuple(liste_auteurs))
    if len(lien[0]) > 1:
        lien.sort()
        title = data.iloc[i, 1]
        citations = data.iloc[i, 2]
        lien = lien + [title, citations]
        print(lien)
        liens.add(tuple(lien))
print(len(liens))
nouv_entrees = []
liens_to_remove = []
for lien in liens:
    auteurs = lien[0]
    if len(auteurs) == 2:
        continue
    for i in range(len(auteurs)):
        for j in range(i + 1, len(auteurs)):
            nouv_entrees.append(((auteurs[i], auteurs[j]), lien[1], lien[2]))
    liens_to_remove.append(lien)

for lien in liens_to_remove:
    liens.remove(lien)

for lien in nouv_entrees:
    liens.add(lien)

print(len(liens))

liens_clean = []
for lien in liens:
    liens_clean.append([lien[0][0], lien[0][1], lien[1], lien[2]])

liens_df = pd.DataFrame(liens_clean, columns=["Auteur1", "Auteur2", "Titre", "Citations"])
print(liens_df)
liens_df.to_csv("liens.csv", index=False)

profs_df = pd.DataFrame(profs, columns=["Prof"])
print(profs_df)
profs_df.to_csv("profs.csv", index=False)
