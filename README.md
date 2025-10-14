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
   └─ results.html

```