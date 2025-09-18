import sqlite3
from datetime import datetime
from hashlib import sha256
import os
from dotenv import load_dotenv
from getpass import getpass

# Commentaire by gpt, revu par C.G.

# Chargement des variables d'environnement depuis le fichier .env
load_dotenv()

# Chemin vers la base de données SQLite
DB_PATH = "./data/Miskatonik_users.db"

def admin_login():
    """
    Fonction de connexion pour l'administrateur.
    Vérifie le nom d'utilisateur et le mot de passe en utilisant des variables d'environnement.
    """
    username = input("Username ? -> ").strip()
    if username != os.getenv("ADMIN_USER"):
        print("Utilisateur inconnu")
        return False

    # Autorise 3 essais de mot de passe
    for essais in range(3, 0, -1):
        password = getpass("Password: ")
        password_hash = sha256(password.encode("utf-8")).hexdigest()  # Hashage du mot de passe
        if password_hash == os.getenv("ADMIN_PASSWORD"):  # Vérifie le hash avec celui stocké
            print("Vous êtes connecté")
            return True
        print(f"Mot de passe incorrect, il vous reste {essais-1} essai(s).")

    print("Trop de tentatives.")
    return False

def setup_roles(cursor):
    """
    Crée les rôles par défaut (Admin, Teacher, Student) dans la table Roles.
    Utilise INSERT OR IGNORE pour éviter les doublons.
    """
    roles = [("Admin",), ("Teacher",), ("Student",)]
    try:
        cursor.executemany("INSERT OR IGNORE INTO Roles (role_name) VALUES (?)", roles)
        print(f"{len(roles)} rôles insérés ou déjà existants.")
    except Exception as e:
        print("Erreur lors de l'insertion des rôles :", e)

def add_user(cursor):
    """
    Ajoute un nouvel utilisateur dans la table Users.
    Demande un nom, un mot de passe, puis un rôle existant.
    """
    print("\n--- Ajouter un nouvel utilisateur ---")
    user_name = input("Nom de l'utilisateur: ").strip()
    password = getpass("Mot de passe: ")
    password_hash = sha256(password.encode("utf-8")).hexdigest()  # Hashage du mot de passe

    # Récupère les rôles disponibles dans la BDD
    cursor.execute("SELECT role_id, role_name FROM Roles")
    available_roles = cursor.fetchall()
    print("Rôles disponibles :")
    for role in available_roles:
        print(f"{role[0]}: {role[1]}")

    # Vérifie si l'ID du rôle est valide
    role_ids = [r[0] for r in available_roles]
    try:
        role_id = int(input("ID du rôle: ").strip())
        if role_id not in role_ids:
            print("ID invalide. Utilisateur non ajouté.")
            return
    except ValueError:
        print("ID invalide. Utilisateur non ajouté.")
        return

    # Insère le nouvel utilisateur dans la table Users
    try:
        cursor.execute("""
            INSERT INTO Users 
            (user_name, user_date_create, password_hash, role_id)
            VALUES (?, ?, ?, ?)
        """, (user_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), password_hash, role_id))
        print(f"Utilisateur '{user_name}' ajouté avec succès.")
    except Exception as e:
        print("Erreur lors de l'insertion de l'utilisateur :", e)

def main():
    """
    Fonction principale :
    - Vérifie la connexion admin
    - Ouvre la base de données
    - Initialise les rôles
    - Ajoute un utilisateur
    - Sauvegarde et ferme la connexion
    """
    if not admin_login():
        return

    try:
        con = sqlite3.connect(DB_PATH)  # Connexion à la base SQLite
        cur = con.cursor()
    except Exception as e:
        print("Erreur de connexion :", e)
        return

    setup_roles(cur)  # Initialise les rôles si nécessaires
    add_user(cur)     # Ajoute un nouvel utilisateur

    con.commit()  # Sauvegarde les changements
    con.close()   # Ferme la connexion
    print("Fermeture de la connexion.")

if __name__ == "__main__":
    main()
