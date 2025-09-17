import sqlite3
from datetime import datetime
from hashlib import sha256
import os
from dotenv import load_dotenv
from getpass import getpass

load_dotenv()

DB_PATH = "./data/Miskatonik_users.db"

def admin_login():
    username = input("Username ? -> ").strip()
    if username != os.getenv("ADMIN_USER"):
        print("Utilisateur inconnu")
        return False

    for essais in range(3, 0, -1):
        password = getpass("Password: ")
        password_hash = sha256(password.encode("utf-8")).hexdigest()
        if password_hash == os.getenv("ADMIN_PASSWORD"):
            print("Vous êtes connecté")
            return True
        print(f"Mot de passe incorrect, il vous reste {essais-1} essai(s).")
    print("Trop de tentatives.")
    return False

def setup_roles(cursor):
    roles = [("Admin",), ("Teacher",), ("Student",)]
    try:
        cursor.executemany("INSERT OR IGNORE INTO Roles (role_name) VALUES (?)", roles)
        print(f"{len(roles)} rôles insérés ou déjà existants.")
    except Exception as e:
        print("Erreur lors de l'insertion des rôles :", e)

def add_user(cursor):
    print("\n--- Ajouter un nouvel utilisateur ---")
    user_name = input("Nom de l'utilisateur: ").strip()
    password = getpass("Mot de passe: ")
    password_hash = sha256(password.encode("utf-8")).hexdigest()

    cursor.execute("SELECT role_id, role_name FROM Roles")
    available_roles = cursor.fetchall()
    print("Rôles disponibles :")
    for role in available_roles:
        print(f"{role[0]}: {role[1]}")

    role_ids = [r[0] for r in available_roles]
    try:
        role_id = int(input("ID du rôle: ").strip())
        if role_id not in role_ids:
            print("ID invalide. Utilisateur non ajouté.")
            return
    except ValueError:
        print("ID invalide. Utilisateur non ajouté.")
        return

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
    if not admin_login():
        return

    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
    except Exception as e:
        print("Erreur de connexion :", e)
        return

    setup_roles(cur)
    add_user(cur)  # Ajouter un user à la fois

    con.commit()
    con.close()
    print("Fermeture de la connexion.")

if __name__ == "__main__":
    main()
