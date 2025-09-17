import pandas as pd
from typing import Dict

def extract_data() -> Dict[str, pd.DataFrame]:
    chemin_csv = "./data/questions.csv"
    
    try :
        dataframes = {
            "csv": pd.read_csv(chemin_csv)
        }
        print("Dataframes OK.")
    except Exception as e :
        print("Erreur lors de l'extraction des données", e)
    return dataframes

if __name__=="__main__":

    # Récupère les données extraites
    dfs = extract_data()

    # Affiche les données de chaque DataFrame du dictionnaire
    for nom, df in dfs.items():
        print(f"\n--- {nom.upper()} ---")
        print(df.head())