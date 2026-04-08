import pandas as pd
import numpy as np

# Charger les données complètes
df = pd.read_csv('/home/ubuntu/sephora_cleaned.csv')

# On s'assure que nos clients types sont inclus dans le light
special_clients = [-9.22111e+18, -9.22281e+18, -3.5342e+18]
df_special = df[df['ID_CLIENT'].isin(special_clients)]

# On échantillonne 100 000 lignes du reste
df_other = df[~df['ID_CLIENT'].isin(special_clients)].sample(n=100000, random_state=42)

# On combine
df_light = pd.concat([df_special, df_other])

# Sauvegarde
df_light.to_csv('/home/ubuntu/sephora_light.csv', index=False)

# Vérification du poids
import os
size_mb = os.path.getsize('/home/ubuntu/sephora_light.csv') / (1024 * 1024)
print(f"Poids du fichier sephora_light.csv : {size_mb:.2f} Mo")
print(f"Nombre de lignes : {len(df_light)}")
