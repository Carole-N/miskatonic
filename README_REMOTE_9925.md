# Miskatonic

**Miskatonic** est une application web de quiz permettant la gestion des utilisateurs, la création et le passage de questionnaires, ainsi que l’archivage des résultats.  
Les questions sont stockées dans **MongoDB**, les utilisateurs dans une base **SQLite**, et un pipeline **ETL** permet de nettoyer et importer des questions depuis un fichier CSV initial.

---

## Objectifs

- Application web de quiz interactive (interface Flask)
- API RESTful (FastAPI) pour la gestion des données
- Authentification utilisateur (SQLite)
- Gestion et archivage des quizz (MongoDB)
- Pipeline ETL complet pour préparer et charger les données de questions depuis un fichier CSV brut

---

## Stack technique

| Composant | Description |
|------------|--------------|
| **Backend principal** | Flask |
| **API REST** | FastAPI |
| **Base NoSQL** | MongoDB (questions, quizz archivés) |
| **Base SQL** | SQLite (utilisateurs) |
| **ETL / Data** | Pandas |
| **Langage** | Python 3.x |

---

## Structure du projet


```
miskatonic
├─ README.md
├─ __pycache__
│  └─ main.cpython-312.pyc
├─ app.js
├─ app.py
├─ data
│  ├─ questions.csv
│  └─ questions.json
├─ database
│  ├─ __pycache__
│  │  ├─ mongo.cpython-312.pyc
│  │  └─ sqlite.cpython-312.pyc
│  ├─ miskatonic_users.db
│  ├─ mongo.py
│  └─ sqlite.py
├─ dto
│  ├─ __pycache__
│  │  ├─ config.cpython-312.pyc
│  │  ├─ connexion.cpython-312.pyc
│  │  └─ services.cpython-312.pyc
│  ├─ config.py
│  ├─ connexion.py
│  └─ services.py
├─ main.py
├─ models
│  ├─ __pycache__
│  │  ├─ questions.cpython-312.pyc
│  │  ├─ user.cpython-312.pyc
│  │  ├─ user_db.cpython-312.pyc
│  │  └─ user_dto.cpython-312.pyc
│  ├─ questions.py
│  ├─ user_db.py
│  └─ user_dto.py
├─ movies.json
├─ requirements.txt
├─ scripts
│  ├─ __pycache__
│  │  └─ fastapi_test.cpython-312.pyc
│  ├─ create_db.py
│  ├─ etl.py
│  ├─ fastapi_test.py
│  └─ load_data.py
├─ static
│  ├─ images
│  │  ├─ bangerblazon.png
│  │  ├─ bannieremiska.png
│  │  ├─ favicon.ico
│  │  ├─ miskabaniere.png
│  │  └─ warning.png
│  ├─ script.js
│  └─ style.css
└─ templates
   ├─ archivedquizz.html
   ├─ form.html
   ├─ home.html
   ├─ index.html
   ├─ login.html
   ├─ privacy.html
   ├─ quizz.html
   ├─ register.html
   ├─ results.html
   ├─ student_home.html
   ├─ teacher_home.html
   ├─ teacher_quiz_preview.html
   └─ teacher_quiz_setup.html

```


---

## Installation

 **Cloner le dépôt**

```bash
git clone https://github.com/CortoGyt/miskatonic.git
cd miskatonic
```
 **Créer un environnement virtuel**
```
python -m venv venv
source venv/bin/activate    # sous Linux/Mac
venv\Scripts\activate       # sous Windows
```
 **Installer les dépdendaces**
```
pip install -r requirements.txt
```

 **Configurer MongoDB et SQLite** 
Lancer un serveur MongoDB local (ou distant)
Créer la base SQLite via :
python create_db.py

## Scripts ETL

#### etl.py
Nettoie un fichier CSV de questions brutes et les charge dans MongoDB.
Exemple : python etl.py --input questions.csv

#### create_db.py
Crée la base SQLite (structure des utilisateurs, rôles, etc.)
Exemple : python create_db.py

#### load_data.py
Ajoute des utilisateurs en base SQLite directement via la console.
Exemple : python load_data.py

##  Lancement du projet
#### Lancer le backend FastAPI
uvicorn main:app --reload --port 8000
reload permet de recharger automatiquement la page après qu'une modification est été apportée dans le code. + Selection du port.

#### Lancer Flask
python app.py
L’application sera alors accessible sur le port 5000

## Endpoint principaux
Route	Méthode	Description
/users	GET	Liste des utilisateurs
/users	POST	Ajout d’un utilisateur
/login	POST	Authentification utilisateur
/question	GET	Liste des questions MongoDB
/question/{id}	GET	Détail d’une question
/quizz	GET	Liste des quizz archivés
/quizz/{id}	GET	Détail d’un quizz archivé

## Workflow typique

L’administrateur charge les questions dans MongoDB via etl.py
Les utilisateurs peuvent s’inscrire et se connecter via Flask
Un utilisateur passe un quiz → les réponses sont enregistrées
Les résultats sont sauvegardés dans la collection quizz de MongoDB
Les enseignants peuvent consulter les quizz archivés depuis l’interface avec un id unique.

## Authentification

Les utilisateurs sont stockés dans SQLite (user_name, password_hash, role_id)
Le hashage des mots de passe se fait via SHA256
Gestion de session Flask pour les connexions
