import pandas as pd
from typing import Dict
from pymongo import MongoClient

# Commentaire by gpt, revu par C.G.


# -------------------------------
# 1) Extraction des données
# -------------------------------
def extract_data() -> Dict[str, pd.DataFrame]:
    """
    Fonction qui charge les données brutes depuis un fichier CSV.
    Retourne un dictionnaire avec un DataFrame.
    """
    chemin_csv = "./data/questions.csv"  # chemin vers le fichier source, ne pas oublier de bien ce placer (cd miskatonic)
    dataframes = {}
    try:
        # Lecture du CSV dans un DataFrame pandas
        dataframes = {"csv": pd.read_csv(chemin_csv)}
        print("Dataframes OK.")
    except Exception as e:
        # Si une erreur survient, on l'affiche
        print("Erreur lors de l'extraction des données :", e)
    return dataframes


# -------------------------------
# 2) Transformation des données
# -------------------------------
def transform_data(donnees_brutes: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    """
    Fonction qui nettoie et transforme les données brutes.
    - Remplace les valeurs nulles dans la colonne responseD
    - Ajoute une colonne contenant le texte des bonnes réponses
    - Sélectionne les colonnes utiles
    - Exporte le résultat en JSON
    """
    print("Exécution de : Transform")

    # Récupération du DataFrame
    df = donnees_brutes.get("csv")
    if df is None:
        print("Aucune donnée à transformer")
        return {}

    # -------------------------------
    # Nettoyage de la colonne correct, responseC et responseD
    # On remplace None, "null" et "NULL" par un texte par défaut
    # Force str pour correct sinon pandas râle, on enleve les espaces au début et fin et on remplace les " " au milieu par des virgules
    # -------------------------------
    if "correct" in df.columns:
        df["correct"] = df["correct"].str.strip()
        df["correct"] = df["correct"].str.replace(r"\s+", ",", regex=True)
    if "responseC" in df.columns:
        df["responseC"] = df["responseC"].replace([None, "null", "NULL"], "C Balo")
    if "responseD" in df.columns:
        df["responseD"] = df["responseD"].replace(
            [None, "null", "NULL"], "La réponse D"
        )

    # -------------------------------
    # Création d'une nouvelle colonne avec le texte des bonnes réponses
    # -------------------------------
    def extraire_bonnes_reponses(row):
        """
        Fonction appliquée à chaque ligne du DataFrame.
        Elle va chercher les bonnes réponses selon la colonne 'correct'
        (ex: "A", "B,C") et retourne la liste du texte correspondant.
        """
        if pd.isna(row["correct"]):
            return []
        # On sépare les lettres de bonnes réponses (ex: "B,C" -> ["B", "C"])
        bonnes_lettres = [x.strip() for x in str(row["correct"]).split(",")]
        bonnes_reponses = []

        # Pour chaque lettre, on récupère le texte correspondant
        for lettre in bonnes_lettres:
            col = f"response{lettre}"  # ex: "responseA"
            if col in row and pd.notna(row[col]):
                bonnes_reponses.append(row[col])

        return bonnes_reponses

    # Application de la fonction à toutes les lignes
    df["good_answers_texte"] = df.apply(extraire_bonnes_reponses, axis=1)

    # filter out records using dropna method
    df_filtered = df[df["correct"].notna()].copy()  # <-- important: copy()

    # Crée la colonne responses directement dans df_filtered
    df_filtered["responses"] = df_filtered.apply(
        lambda row: [
            row["responseA"],
            row["responseB"],
            row["responseC"],
            row["responseD"],
        ],
        axis=1,
    )
    # -------------------------------
    # Sélection des colonnes finales
    # -------------------------------
    colonnes_finales = [
        "question",
        "subject",
        "use",
        "correct",
        "responses",
        "good_answers_texte",
        "remark",
    ]
    df_final = df_filtered[colonnes_finales].copy()

    # -------------------------------
    # Ajout d'une colonne id en position 0 autoIncr
    # -------------------------------
    df_final.insert(0, "id", range(1, len(df_final) + 1))


    df_final = df_final.where(pd.notna(df_final), None)
    # -------------------------------
    # Export du résultat en JSON
    # -------------------------------

    # output_path = "./data/questions.json"
    # df_final.to_json(output_path, orient="records", force_ascii=False, indent=4)
    # print(f"JSON créé avec succès : {output_path}")

    # return {"csv": df_final}
    return df_final


# ----------------------
# Insertion dans mongo directe
# ----------------------
def load_data(df: pd.DataFrame):
    if df.empty:
        print("Aucune donnée à insérer")
        return
    try:
        client = MongoClient("mongodb://isen:isen@localhost:27017/admin")
        db = client["miskatonic"]
        collection = db["question"]

        records = df.to_dict(orient="records")
        collection.insert_many(records)

        print(f"{len(records)} questions insérées dans MongoDB.")
    except:
        print("Erreur lors de l'insertion dans mongo")
    # -------------------------------


# 3) Point d'entrée du script
# -------------------------------


if __name__ == "__main__":
    # Étape 1 : Extraction
    dfs = extract_data()

    # Étape 2 : Transformation
    dfs_transformed = transform_data(dfs)

    load_data(dfs_transformed)
