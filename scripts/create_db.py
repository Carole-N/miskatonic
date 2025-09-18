import sqlite3   # On importe le module sqlite3 qui permet de manipuler une base SQLite

# Commentaire by gpt, revu par C.G.

def create_db():
    print("Execution de : Create")
    try: 
        # Connexion (ou création si elle n'existe pas) à une base de données SQLite
        # Le fichier sera enregistré à l'emplacement ./data/Miskatonik_users.db
        con = sqlite3.connect("./data/Miskatonik_users.db")
        cur = con.cursor()  # Création d'un curseur pour exécuter les requêtes SQL
    except Exception as e:
        # Gestion d'erreur si la connexion échoue
        print("Erreur lors de la connexion à SQLite3 :", e)
        return  # On arrête la fonction si on ne peut pas se connecter

    # --- Création de la table "Roles" ---
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Roles (
                role_id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Identifiant unique auto-incrémenté
                role_name TEXT UNIQUE                      -- Nom du rôle (doit être unique)
            );
        """)
        print("1/2 Table 'Roles' créée avec succès.")
    except Exception as e:
        # Gestion d'erreur si la création échoue
        print("Erreur lors de la création de 'Roles' :", e)

    # --- Création de la table "Users" ---
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Identifiant unique auto-incrémenté
                user_name TEXT NOT NULL,                    -- Nom de l’utilisateur (obligatoire)
                user_date_create TEXT NOT NULL,             -- Date de création du compte (obligatoire)
                password_hash TEXT NOT NULL,                -- Mot de passe chiffré (obligatoire)
                role_id INTEGER NOT NULL,                   -- Clé étrangère : rôle de l’utilisateur
                FOREIGN KEY (role_id) REFERENCES Roles(role_id)  -- Relation avec la table Roles
            );
        """)
        print("2/2 Table 'Users' créée avec succès.")
    except Exception as e:
        # Gestion d’erreur si la création échoue
        print("Erreur lors de la création de 'Users' :", e)

    # --- Validation et fermeture ---
    con.commit()   # Sauvegarde (commit) des changements dans la base
    con.close()    # Fermeture de la connexion
    print("Fermeture.")

# Point d’entrée du script
if __name__ == "__main__":
    create_db()   # Exécute la fonction si le fichier est lancé directement
