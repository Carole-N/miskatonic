# Miskatonic

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Framework-lightgrey?logo=flask)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green?logo=fastapi)
![MongoDB](https://img.shields.io/badge/MongoDB-NoSQL-brightgreen?logo=mongodb)
![SQLite](https://img.shields.io/badge/SQLite-SQL-blue?logo=sqlite)
![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)
![License](https://img.shields.io/badge/License-MIT-yellow?logo=open-source-initiative)

> Application web de quiz : gestion des utilisateurs, création/passage de questionnaires, archivage des résultats.
> Questions en **MongoDB** (NoSQL), utilisateurs en **SQLite** (SQL), pipeline **ETL** pour nettoyer/charger un CSV.

---

## Table des matières
1. [Description](#-description)
2. [Fonctionnalités](#-fonctionnalités)
3. [Pré-requis](#-pré-requis)
4. [Technologies et langages](#-technologies-et-langages)
5. [Fonctionnement global](#-fonctionnement-global)
6. [Installation](#-installation)
7. [Configuration de l’environnement](#-configuration-de-lenvironnement)
8. [Scripts ETL](#-scripts-etl)
9. [Lancement du projet](#-lancement-du-projet)
10. [Endpoints principaux](#-endpoints-principaux)
11. [Workflow typique](#-workflow-typique)
12. [Guide de développement](#-guide-de-développement)
13. [Structure du projet](#-structure-du-projet)
14. [Architecture du projet](#-architecture-du-projet)
15. [Schéma de la base SQLite](#-schéma-de-la-base-sqlite)
16. [Informations](#-informations)
17. [Livrables](#-livrables)
18. [Licence](#-licence)
19. [Créateurs du projet](#-créateurs-du-projet)

---

## Description
Le **projet Miskatonic** propose une application web permettant la **création, le passage et l’archivage de quiz**.  
Il comprend une **interface web Flask** pour les utilisateurs, une **API FastAPI** pour la gestion des données, et un **pipeline ETL** chargé de nettoyer et d’importer les questions depuis un fichier CSV initial (`data/questions.csv`).  
Les **questions** sont stockées dans **MongoDB**, tandis que les **utilisateurs et rôles** sont gérés dans une base **SQLite**.  
Les mots de passe y sont sécurisés par **hachage**, garantissant la confidentialité des identifiants.  

**Objectifs principaux :**  
- Création de quiz par les enseignants  
- Passage de quiz par les étudiants  
- Authentification et gestion des rôles (enseignant / étudiant)  
- Archivage et consultation des résultats

---

## Fonctionnalités
- Authentification (inscription, connexion) et rôles.
- Création de quiz (sélection de questions).
- Passage de quiz, calcul des résultats.
- Archivage et consultation d’anciens quiz.
- ETL pour charger des questions depuis un CSV en base MongoDB.
- API REST (FastAPI) pour la gestion des données (questions/quiz).

---

## Pré-requis
- Python **3.x**
- (Optionnel) Docker & Docker Compose
- MongoDB local ou distant
- Git

---

## Technologies et langages
| Outil / Langage | Rôle dans le projet |
|---|---|
| **Flask** | Interface web (templates Jinja, routes UI) |
| **FastAPI** | API REST (endpoints de données) |
| **SQLite** | Stockage des utilisateurs (SQL) |
| **MongoDB** | Stockage des questions & quiz archivés (NoSQL) |
| **Pandas** | Pipeline ETL (nettoyage CSV) |
| **Docker** | Exécution conteneurisée (optionnelle) |

---

## Fonctionnement global
1) L’enseignant prépare les questions (CSV) → **ETL** → MongoDB.  
2) Les utilisateurs créent un compte (SQLite), se connectent (Flask).  
3) L’enseignant compose un quiz, l’étudiant le passe (Flask).  
4) Les résultats sont archivés (MongoDB) et consultables (UI + API).

---

## Installation

**Cloner le dépôt**
```bash
git clone https://github.com/Carole-N/miskatonic.git
cd miskatonic
```

**Créer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows
```

**Installer les dépendances**
```bash
pip install -r requirements.txt
```

---

## Configuration de l’environnement
Variables d’environnement (exemples) :

```bash
# Chemin SQLite (par défaut dans database/)
export SQLITE_PATH=database/miskatonic_users.db

# Connexion MongoDB (adapter au besoin)
export MONGO_URI="mongodb://localhost:27017"
export MONGO_DB="miskatonic"
```

> Si vous utilisez un fichier `.env`, vérifiez que son contenu n’est **pas** versionné (voir `.gitignore`).

---

## Scripts ETL

### `etl.py`
Nettoie un CSV de questions et charge en base MongoDB.
```bash
python scripts/etl.py --input data/questions.csv
```

### `create_db.py`
Crée la base SQLite (tables utilisateurs/roles).
```bash
python scripts/create_db.py
```

### `load_data.py`
Ajoute des utilisateurs en base SQLite via la console.
```bash
python scripts/load_data.py
```

---

## Lancement du projet

### Lancer le backend **FastAPI**
```bash
uvicorn main:app --reload --port 8000
```
> `--reload` recharge automatiquement à chaque modification.

### Lancer **Flask**
```bash
python app.py
```
> L’UI est accessible par défaut sur **http://127.0.0.1:5000**

*(Option Docker : utilisez `docker-compose up --build` si vous avez configuré vos services.)*

---

## Endpoints principaux
| Route | Méthode | Description |
|---|---|---|
| `/users` | GET | Liste des utilisateurs |
| `/users` | POST | Ajout d’un utilisateur |
| `/login` | POST | Authentification |
| `/question` | GET | Liste des questions (Mongo) |
| `/question/{id}` | GET | Détail question |
| `/quizz` | GET | Liste des quizz archivés |
| `/quizz/{id}` | GET | Détail d’un quizz archivé |

> **OpenAPI** : voir [`livrables/openapi.json`](livrables/openapi.json) ou l’aperçu [`livrables/redoc-static.html`](livrables/redoc-static.html).

---

## Workflow typique
1. ETL → `questions` (MongoDB).  
2. Inscription / connexion (SQLite).  
3. Passage d’un quiz.  
4. Archivage des résultats (MongoDB).  
5. Consultation des quizz archivés (UI + API).

---

## Guide de développement
- **Organisation** : Flask pour l’UI (templates/`templates`, assets/`static`), FastAPI pour l’API (`main.py`).  
- **Données** : `database/sqlite.py` (SQLite), `database/mongo.py` (MongoDB).  
- **DTO / Services** : `dto/` (connexion, services).  
- **Modèles** : `models/` (questions, user DTO/DB).  
- **Qualité** : `.gitignore` renforcé pour éviter `.venv/`, `__pycache__/`, `*.db`, etc.

---

## Structure du projet
```text
miskatonic
├── Dockerfile
├── README.md
├── app.py                      # Flask (UI)
├── main.py                     # FastAPI (API)
├── data/
│   ├── questions.csv
│   └── questions.json
├── database/
│   ├── miskatonic_users.db
│   ├── mongo.py
│   └── sqlite.py
├── docker-compose.yml
├── dto/
│   ├── config.py
│   ├── connexion.py
│   └── services.py
├── livrables/
│   ├── openapi.json
│   ├── projet_miskatonic_presentation.pdf
│   ├── projet_miskatonic_presentation-avec-videos.pptx
│   ├── redoc-static.html
│   ├── sqlite3.drawio.png
│   ├── template_mongo.json
│   └── user_stories_miskatonic.pdf
├── models/
│   ├── questions.py
│   ├── user_db.py
│   └── user_dto.py
├── scripts/
│   ├── create_db.py
│   ├── etl.py
│   ├── fastapi_test.py
│   └── load_data.py
├── static/
│   ├── images/
│   ├── script.js
│   └── style.css
└── templates/
    ├── archived_quizz_detail.html
    ├── archived_quizz_list.html
    ├── archivedquizz.html
    ├── form.html
    ├── home.html
    ├── index.html
    ├── login.html
    ├── privacy.html
    ├── quizz.html
    ├── register.html
    ├── results.html
    ├── student_home.html
    ├── teacher_home.html
    ├── teacher_quiz_preview.html
    └── teacher_quiz_setup.html
```

---

## Architecture du projet
```                +----------------------+
                |       Flask (UI)     |
                |  templates / static  |
                +----------+-----------+
                           |
                           | (requêtes API / formulaires)
                           v
                +----------+-----------+
                |       FastAPI        |
                |   main.py (API REST) |
                +----+-----------+-----+
                     |           |
                     |           |
          +----------+           +-----------+
          |                                  |
+------------------+              +---------------------+
|   SQLite (SQL)   |              |     MongoDB         |
|   users / roles  |              | questions / quizz   |
+------------------+              +---------------------+
                     ^
                     |
                     | (ETL : chargement CSV → Mongo)
                     |
                 +---+---+
                 |  ETL  |
                 +-------+

```

---

## Schéma de la base SQLite
- Voir l’image : [`livrables/sqlite3.drawio.png`](livrables/sqlite3.drawio.png)  
- Modèles côté SQL : `models/user_db.py`, `models/user_dto.py`  
- Connexion/CRUD : `database/sqlite.py`

---

## ℹInformations
- Ce dépôt correspond à **mon fork personnel** du projet, réalisé initialement en binôme avec **CortoGyt**.  
- **Branche principale :** `main` — dépôt nettoyé et mise à jour du `.gitignore`.  
- **Version du rendu :** finale (alignée sur `upstream/main`)  
- **Date :** Octobre 2025  
- **Auteure du fork :** [Carole-N](https://github.com/Carole-N)

---

## Livrables
Dans [`livrables/`](livrables/) :

- **OpenAPI** : [`openapi.json`](livrables/openapi.json) – aperçu : [`redoc-static.html`](livrables/redoc-static.html)  
- **Template MongoDB** : [`template_mongo.json`](livrables/template_mongo.json)  
- **MCD SQLite** : [`sqlite3.drawio.png`](livrables/sqlite3.drawio.png)  
- **User Stories** : [`user_stories_miskatonic.pdf`](livrables/user_stories_miskatonic.pdf)  
- **Présentation (PDF)** : [`projet_miskatonic_presentation.pdf`](livrables/projet_miskatonic_presentation.pdf)  
- **Présentation (PPTX — avec vidéos)** : [`projet_miskatonic_presentation-avec-videos.pptx`](livrables/projet_miskatonic_presentation-avec-videos.pptx)

---

## Licence
Ce projet est distribué sous la licence **MIT**.  
Vous êtes libre de réutiliser, modifier et distribuer le code, à condition d’en mentionner l’auteure.

> Pour ajouter un fichier de licence à la racine :
> ```bash
> printf 'MIT License\n\nCopyright (c) 2025 Carole ...
> ' > LICENSE
> ```

---

## Créateurs du projet
- **[Carole-N](https://github.com/Carole-N)**
- **[CortoGyt](https://github.com/CortoGyt)**
