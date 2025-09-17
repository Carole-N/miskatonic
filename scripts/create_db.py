import sqlite3

def create_db():
    print("Execution de : Create")
    try: 
        con = sqlite3.connect("./data/Miskatonik_users.db")
        cur = con.cursor()
    except Exception as e:
        print("Erreur lors de la connexion à SQLite3 :", e)
        return

    # Création de la table Roles
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Roles (
                role_id INTEGER PRIMARY KEY AUTOINCREMENT,
                role_name TEXT UNIQUE
            );
        """)
        print("1/2 Table 'Roles' créée avec succès.")
    except Exception as e:
        print("Erreur lors de la création de 'Roles' :", e)

    # Création de la table Users
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT NOT NULL,
                user_date_create TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                role_id INTEGER NOT NULL,
                FOREIGN KEY (role_id) REFERENCES Roles(role_id)
            );
        """)
        print("2/2 Table 'Users' créée avec succès.")
    except Exception as e:
        print("Erreur lors de la création de 'Users' :", e)

    # Commit et fermeture
    con.commit()
    con.close()
    print("Fermeture.")

if __name__ == "__main__":
    create_db()
