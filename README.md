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
|------------|-------------|
| **Backend principal** | Flask |
| **API REST** | FastAPI |
| **Base NoSQL** | MongoDB (questions, quizz archivés) |
| **Base SQL** | SQLite (utilisateurs) |
| **ETL / Data** | Pandas |
| **Langage** | Python 3.x |

---

## Structure du projet

```text
miskatonic
├── Dockerfile
├── README.md
├── app.js
├── app.py
├── data
│   ├── questions.csv
│   └── questions.json
├── database
│   ├── miskatonic_users.db
│   ├── mongo.py
│   └── sqlite.py
├── docker-compose.yml
├── dto
│   ├── config.py
│   ├── connexion.py
│   └── services.py
├── livrables
│   ├── openapi.json
│   ├── projet_miskatonic_presentation.pdf
│   ├── projet_miskatonic_presentation-avec-videos.pptx
│   ├── redoc-static.html
│   ├── sqlite3.drawio.png
│   ├── template_mongo.json
│   └── user_stories_miskatonic.pdf
├── main.py
├── models
│   ├── questions.py
│   ├── user_db.py
│   └── user_dto.py
├── requirements.txt
├── scripts
│   ├── create_db.py
│   ├── etl.py
│   ├── fastapi_test.py
│   └── load_data.py
├── static
│   ├── images/
│   ├── script.js
│   └── style.css
└── templates
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

## Installation

**Cloner le dépôt**
```bash
git clone https://github.com/Carole-N/miskatonic.git
cd miskatonic
```

**Créer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate    # sous Linux/Mac
venv\Scripts\activate       # sous Windows
```

**Installer les dépendances**
```bash
pip install -r requirements.txt
```

**Configurer MongoDB et SQLite**  
- Lancer un serveur MongoDB local (ou distant).  
- Créer la base SQLite via :
```bash
python create_db.py
```

---

## Scripts ETL

### etl.py
Nettoie un fichier CSV de questions brutes et les charge dans MongoDB.  
Exemple :
```bash
python etl.py --input questions.csv
```

### create_db.py
Crée la base SQLite (structure des utilisateurs, rôles, etc.).  
Exemple :
```bash
python create_db.py
```

### load_data.py
Ajoute des utilisateurs en base SQLite directement via la console.  
Exemple :
```bash
python load_data.py
```

---

## Lancement du projet

### Lancer le backend FastAPI
```bash
uvicorn main:app --reload --port 8000
```
*(L’option `--reload` recharge automatiquement l’application après chaque modification du code.)*

### Lancer Flask
```bash
python app.py
```
L’application sera alors accessible sur le port **5000**.

---

## Endpoints principaux

| Route | Méthode | Description |
|-------|----------|-------------|
| `/users` | GET | Liste des utilisateurs |
| `/users` | POST | Ajout d’un utilisateur |
| `/login` | POST | Authentification utilisateur |
| `/question` | GET | Liste des questions MongoDB |
| `/question/{id}` | GET | Détail d’une question |
| `/quizz` | GET | Liste des quizz archivés |
| `/quizz/{id}` | GET | Détail d’un quizz archivé |

---

## Workflow typique

1. L’administrateur charge les questions dans MongoDB via `etl.py`.  
2. Les utilisateurs peuvent s’inscrire et se connecter via Flask.  
3. Un utilisateur passe un quiz → les réponses sont enregistrées.  
4. Les résultats sont sauvegardés dans la collection *quizz* de MongoDB.  
5. Les enseignants peuvent consulter les quizz archivés depuis l’interface, à partir d’un ID unique.

---

## Authentification

- Les utilisateurs sont stockés dans SQLite (`user_name`, `password_hash`, `role_id`).  
- Le hashage des mots de passe se fait via **SHA256**.  
- Gestion de session **Flask** pour les connexions.

---

### Informations

- Ce dépôt correspond à **mon fork personnel** du projet *Miskatonic University – Générateur de quiz*, réalisé initialement en binôme avec **CortoGyt**.  
- **Branche principale :** `main` — dépôt nettoyé et mise à jour du `.gitignore`.  
- **Version du rendu :** finale (alignée sur `upstream/main`)  
- **Date :** Octobre 2025  
- **Auteure du fork :** [Carole-N](https://github.com/Carole-N)

---

### Livrables

L’ensemble des documents de rendu se trouve dans le dossier [`livrables/`](livrables/).

- **OpenAPI** : [`livrables/openapi.json`](livrables/openapi.json) – aperçu : [`livrables/redoc-static.html`](livrables/redoc-static.html)  
- **Template MongoDB** : [`livrables/template_mongo.json`](livrables/template_mongo.json)  
- **MCD SQLite** : [`livrables/sqlite3.drawio.png`](livrables/sqlite3.drawio.png)  
- **User Stories** : [`livrables/user_stories_miskatonic.pdf`](livrables/user_stories_miskatonic.pdf)  
- **Présentation (PDF)** : [`livrables/projet_miskatonic_presentation.pdf`](livrables/projet_miskatonic_presentation.pdf)  
- **Présentation (PPTX — avec vidéos)** : [`livrables/projet_miskatonic_presentation-avec-videos.pptx`](livrables/projet_miskatonic_presentation-avec-videos.pptx)
