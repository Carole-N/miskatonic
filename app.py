from flask import Flask, redirect, url_for, request, render_template, session
import sqlite3
from hashlib import sha256
from dto.connexion import Connexion

# Nom de la base de données SQLite
DATABASE = 'data/miskatonic_users.db'

# Création de l'application Flask
app = Flask(__name__)

# Clé secrète nécessaire pour utiliser les sessions (à changer en production)
app.secret_key = "change_me_to_a_secure_random_key"

@app.route('/')
def index():
    # Page d'accueil, rend simplement le template index.html
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Message affiché en cas d'erreur ou de succès
    message = ''
    # Si l'utilisateur envoie un formulaire (méthode POST)
    if request.method == 'POST':
        # Récupération du nom d'utilisateur et du mot de passe
        user = request.form.get('user')
        pwd = request.form.get('pwd')
        # Hachage du mot de passe avec SHA-256
        pwd_hash = sha256(pwd.encode("utf-8")).hexdigest()

        try:
            # Connexion à la base de données SQLite
            with sqlite3.connect(DATABASE) as conn:
                cur = conn.cursor()
                # Vérifie si un utilisateur avec ce nom et ce mot de passe existe
                query = "SELECT COUNT(*) FROM Users WHERE user_name = ? AND password_hash = ?"
                cur.execute(query, (user, pwd_hash))
                result = cur.fetchone()

                # Si un utilisateur est trouvé
                if result and result[0] > 0:
                    # On sauvegarde l'utilisateur dans la session
                    session['user'] = user
                    print("Welcome")
                    # Redirige vers la page d'accueil protégée
                    return redirect(url_for('home'))
                else:
                    # Aucun utilisateur correspondant
                    message = "Unknown username or password."
        except Exception as e:
            # En cas d'erreur de base de données
            print("Erreur lors de l'appel :", e)
            message = "Database error"
    # Affiche la page de login avec un éventuel message d'erreur
    return render_template('login.html', message=message)

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Message affiché pour informer l'utilisateur
    message = ""
    if request.method == 'POST':
        # Récupération des champs du formulaire
        user = request.form['user']
        password = request.form['pwd']
        password2 = request.form['pwd2']

        # Vérifie si les deux mots de passe correspondent
        if password != password2:
            message = "Passwords do not match"
            return render_template('register.html', message=message)

        # Hachage du mot de passe avant insertion
        password_hash = sha256(password.encode("utf-8")).hexdigest()

        try:
            # Connexion à la base de données
            with sqlite3.connect(DATABASE) as conn:
                cursor = conn.cursor()

                # Vérifie si l'utilisateur existe déjà
                cursor.execute("SELECT COUNT(*) FROM Users WHERE user_name = ?", (user,))
                result = cursor.fetchone()
                if result and result[0] > 0:
                    # Nom d'utilisateur déjà pris
                    message = "Username already taken"
                    return render_template('register.html', message=message)

                # Insère le nouvel utilisateur dans la base
                cursor.execute(
                    "INSERT INTO Users (user_name, password_hash, role_id) VALUES (?, ?, 3)",
                    (user, password_hash)
                )
                conn.commit()

        except Exception as e:
            # Gestion d'une erreur d'insertion en base
            print("Erreur lors de l'insertion :", e)
            message = "Database error"
            return render_template('register.html', message=message)

        # Si l'inscription réussit, affiche la page de connexion
        message = "Registration successful! Please login."
        return render_template('login.html', message=message)

    # Affiche la page d'inscription pour une requête GET
    return render_template('register.html', message=message)

@app.route('/home')
def home():
    # Vérifie si l'utilisateur est connecté en regardant la session
    if 'user' not in session:
        # S'il n'est pas connecté, redirige vers la page de connexion
        return redirect(url_for('login'))
    # Si l'utilisateur est connecté, affiche la page d'accueil protégée
    return render_template('home.html', user=session['user'])

@app.route('/logout')
def logout():
    # Supprime l'utilisateur de la session pour le déconnecter
    session.pop('user', None)
    # Redirige vers la page d'accueil publique
    return redirect(url_for('index'))

@app.route('/quizz')
def quizz():
    if 'user' not in session:
        return redirect(url_for('login'))

    Connexion.connect()
    questions = Connexion.get_all_questions()
    Connexion.disconnect()

    return render_template(
        'quizz.html',
        user=session['user'],
        questions=questions
    )


@app.route("/question/<int:_id>")
def question_detail(_id):
    question = next((q for q in Connexion.get_question_by_id if q["_id"] == _id), None)
    if not question:
        return "Question not found", 404
    return render_template("question_detail.html", question=question)

@app.route("/submit/<string:_id>", methods=["POST"])
def submit_answer(_id):
    Connexion.connect()
    question = Connexion.get_question_by_id(_id)
    Connexion.disconnect()

    if not question:
        return "Question not found", 404

    selected = request.form.getlist("response")

    correct = set(selected) == set(question.get("good_answers_texte", []))

    if correct:
        return f" Correct! {', '.join(question['good_answers_texte'])} is the right answer."
    else:
        return f" Incorrect. The correct answer is {', '.join(question['good_answers_texte'])}."

    

if __name__ == "__main__":
    # Lancement de l'application Flask en mode debug
    app.run(debug=True)
