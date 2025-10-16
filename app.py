from flask import Flask, render_template, request, redirect, url_for, session, flash
from hashlib import sha256
import requests
from dto.services import QuestionService, QuizzService 
from random import sample


app = Flask(__name__)
app.secret_key = "miufdzpiugfeza"

FASTAPI_URL = "http://localhost:8000"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = request.form["user"]
        password = request.form["pwd"]
        password2 = request.form["pwd2"]

        if password != password2:
            return render_template("register.html", message="Passwords do not match")

        pwd_hash = sha256(password.encode()).hexdigest()
        res = requests.post(
            f"{FASTAPI_URL}/users", json={"user_name": user, "password_hash": pwd_hash}
        )

        if res.status_code == 200:
            return redirect(url_for("login"))
        return render_template("register.html", message="Registration failed")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        user = request.form["user"]
        pwd = request.form["pwd"]
        pwd_hash = sha256(pwd.encode()).hexdigest()

        try:
            res = requests.post(
                f"{FASTAPI_URL}/login",
                json={"user_name": user, "password_hash": pwd_hash},
            )

            if res.status_code == 200:
                session["user"] = user
                role = request.form.get("role")

                if role == "student":
                    return redirect(url_for("student_home"))
                elif role == "teacher":
                    return redirect(url_for("teacher_home"))
                else:
                    return redirect(url_for("home"))
            else:
                message = res.json().get("detail", "Invalid credentials")

        except Exception as e:
            print("Erreur lors de l'appel :", e)
            message = f"Database error: {e}"

    return render_template("login.html", message=message)


@app.route("/logout")
def logout():
    session.pop("user", None)
    # Nettoyage supplémentaire pour éviter les anciennes données de quiz corrompues
    session.pop("quiz_preview", None)
    session.pop("quiz_subject", None)
    session.pop("quiz_to_save", None) # On nettoie aussi la nouvelle clé de session
    return redirect(url_for("index"))

@app.route("/home")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("home.html", user=session["user"])

def get_subjects_from_mongo():
    questions = QuestionService.get_all_questions()
    subjects = sorted(set(q.get("subject", "").strip() for q in questions if q.get("subject")))
    return subjects


def get_questions_by_subject(subject):
    all_questions = QuestionService.get_all_questions()
    print("Toutes les questions récupérées :", all_questions)

    filtered = [
        q for q in all_questions
        if q.get("subject") == subject and (q.get("question") or (isinstance(q.get("question_text"), dict) and q.get("question_text", {}).get("question"))) and q.get("responses")
    ]
    
    print(f"Questions filtrées pour le sujet '{subject}' :", filtered)
    print(f"Nombre de questions filtrées : {len(filtered)}")

    return filtered


@app.route("/student")
def student_home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("student_home.html", user=session["user"])


@app.route("/teacher")
def teacher_home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("teacher_home.html", user=session["user"])


@app.route("/teacher/quiz-setup", methods=["GET", "POST"])
def teacher_quiz_setup():
    subjects = QuizzService.get_subjects_from_mongo()
    selected_subject = None

    if request.method == "POST":
        selected_subject = request.form.get("subject")
        nb_questions = request.form.get("nb")

        if not selected_subject:
            flash("Veuillez choisir un sujet.")
            return redirect(url_for("teacher_quiz_setup"))
        
        try:
            nb_questions = int(nb_questions)
            if nb_questions <= 0:
                raise ValueError
        except ValueError:
            flash("Le nombre de questions doit être un entier positif.")
            return redirect(url_for("teacher_quiz_setup"))

        quiz_generated = QuestionService.get_questions_by_subject(selected_subject)
        print("[DEBUG] Questions récupérées :", quiz_generated)

        if not quiz_generated:
            flash(f"Aucune question trouvée pour le sujet '{selected_subject}'.")
            return redirect(url_for("teacher_quiz_setup"))

        if len(quiz_generated) > nb_questions:
            quiz_generated = sample(quiz_generated, nb_questions)
        else:
            flash(f"Seulement {len(quiz_generated)} questions disponibles pour ce sujet.")

        session["quiz_preview"] = quiz_generated
        session["quiz_subject"] = selected_subject
        session["quiz_nb"] = nb_questions

        return redirect(url_for("teacher_quiz_preview"))

    return render_template(
        "teacher_quiz_setup.html",
        subjects=subjects,
        selected_theme=selected_subject
    )


@app.route("/teacher/quiz-preview")
def teacher_quiz_preview():
    if "quiz_preview" not in session or "quiz_subject" not in session:
        flash("Aucun quiz en session. Veuillez générer un quiz avant l'aperçu.")
        return redirect(url_for("teacher_quiz_setup"))

    quizz = session.get("quiz_preview", [])
    subject = session.get("quiz_subject", "Inconnu")

    normalized_questions = []
    for q in quizz:
        question_text = None
        responses = []
        good_answers = []
        remark = None

        # Cas 1: La clé "question" contient un dictionnaire avec les détails
        question_data = q.get("question")
        if isinstance(question_data, dict):
            question_text = question_data.get("question")
            responses = question_data.get("responses", [])
            good_answers = question_data.get("good_answers_texte", [])
            remark = question_data.get("remark")
        # Cas 2: La clé "question" est le texte lui-même
        elif isinstance(question_data, str):
            question_text = question_data
            responses = q.get("responses", [])
            good_answers = q.get("good_answers_texte", [])
            remark = q.get("remark")
        # Cas 3: Fallback pour une structure imbriquée sous "question_text"
        else:
            nested_data = q.get("question_text")
            if isinstance(nested_data, dict):
                question_text = nested_data.get("question")
                responses = nested_data.get("responses", [])
                good_answers = nested_data.get("good_answers_texte", [])
                remark = nested_data.get("remark")
            else: # Si aucune structure ne correspond, on prend les champs au premier niveau
                responses = q.get("responses", [])
                good_answers = q.get("good_answers_texte", [])
                remark = q.get("remark")

        # S'assurer que le texte de la question est une chaîne et non None
        question_text = question_text or "Question manquante"
        subject_q = q.get("subject") or subject


        if not responses or question_text == "Question manquante":
            print(f"[Alerte] Question incomplète ou manquante, ignorée: {q}")
            continue

        normalized_questions.append({
            "question_text": question_text, 
            "responses": responses,
            "good_answers_texte": good_answers,
            "remark": remark,
            "subject": subject_q,
            "question_id": str(q.get("_id") or q.get("id") or "")
        })

    #On stocke la liste propre dans la session
    session['quiz_to_save'] = normalized_questions

    return render_template(
        "teacher_quiz_preview.html",
        subject=subject,
        total=len(normalized_questions),
        questions=normalized_questions
    )

@app.route("/teacher/save-quiz", methods=["POST"])
def save_quiz():
    if "user" not in session:
        flash("Aucun utilisateur connecté.")
        return redirect(url_for("teacher_quiz_setup"))

    questions_preview = session.pop('quiz_to_save', None)
    subject = session.get("quiz_subject") # On peut aussi le récupérer de la session

    if not questions_preview or not subject:
        flash("Erreur : les données du quiz sont introuvables dans la session. Veuillez réessayer.")
        return redirect(url_for("teacher_quiz_setup"))

    questions_to_save = []
    for q in questions_preview:
        questions_to_save.append({
            "question_id": str(q.get("question_id") or ""),
            "question_text": q.get("question_text", "Question manquante"), 
            "responses": q.get("responses", []),
            "good_answers_texte": q.get("good_answers_texte", []),
            "remark": q.get("remark"),
            "subject": q.get("subject") or subject,
            "selected": [],  # Initialisé vide pour la réponse de l'étudiant
            "correct_answers": q.get("good_answers_texte", []) # Assure la cohérence
        })

    try:
        QuizzService.save_quizz_result(
            user=session["user"],
            subject=subject,
            questions=questions_to_save
        )
    except Exception as e:
        print("[ERREUR MONGO DB] Échec de la sauvegarde du quiz :", e)
        flash("Erreur critique lors de l'enregistrement du quiz dans la base de données.")
        return redirect(url_for("teacher_quiz_setup"))

    flash("Quiz enregistré avec succès !")
    return redirect(url_for("archived_quizz_list"))

@app.route("/teacher/quizz/archived", methods=["GET"])
def archived_quizz_list():
    if "user" not in session:
        flash("Veuillez vous connecter pour accéder aux quiz archivés.")
        return redirect(url_for("login"))

    quizz_list = QuizzService.get_all_quizzs()
    user_quizz = [q for q in quizz_list if q.get("user") == session["user"]]

    return render_template("archived_quizz_list.html", quizz_list=user_quizz)

@app.route("/teacher/quizz/archived/<quizz_id>", methods=["GET"])
def archived_quizz(quizz_id):
    if "user" not in session:
        flash("Veuillez vous connecter.")
        return redirect(url_for("login"))

    quizz = QuizzService.get_quizz_by_id(quizz_id)
    print("DEBUG quizz:", quizz)
    if not quizz:
        flash("Quiz introuvable.")
        return redirect(url_for("archived_quizz_list"))

    return render_template("archivedquizz.html", quizz=quizz)

@app.route("/student/quizz/<quizz_id>", methods=["GET", "POST"])
def student_quizz(quizz_id):
    if "user" not in session:
        return redirect(url_for("login"))

    quizz = QuizzService.get_quizz_by_id(quizz_id)
    if not quizz:
        flash("Quiz introuvable.")
        return redirect(url_for("student_home"))

    if request.method == "POST":
        user_answers = {}
        score = 0
        for q in quizz["questions"]:
            q_id = str(q["question_id"])
            selected = request.form.getlist(f"response_{q_id}")
            user_answers[q_id] = selected

            correct_answers = q.get("good_answers_texte", [])
            if set(selected) == set(correct_answers):
                score += 1

        session["last_quizz_results"] = {
            "quizz": quizz,
            "answers": user_answers,
            "score": score
        }
        print("DEBUG user_answers:", session.get("last_quizz_results") or user_answers)
        return render_template(
            "results.html",
            quizz=quizz,
            answers=user_answers,
            score=score,
            user=session["user"]
        )

    return render_template("quizz.html", user=session["user"], questions=quizz["questions"], quizz=quizz)


@app.route("/student/quizz/<quizz_id>/result")
def student_quizz_result(quizz_id):
    if "user" not in session:
        return redirect(url_for("login"))

    results = session.get("last_quizz_results")
    if not results or str(results["quizz"]["_id"]) != quizz_id:
        flash("Aucun résultat disponible pour ce quiz.")
        return redirect(url_for("student_home"))

    return render_template(
        "quizz_result.html",
        user=session["user"],
        quizz=results["quizz"],
        answers=results["answers"]
    )

@app.route("/student/access_quizz", methods=["GET"])
def student_access_quizz():
    if "user" not in session:
        return redirect(url_for("login"))

    quizz_id = request.args.get("quizz_id")
    if not quizz_id:
        flash("Veuillez entrer un code de quiz valide.")
        return redirect(url_for("student_home"))

    return redirect(url_for("student_quizz", quizz_id=quizz_id))

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

if __name__ == "__main__":
    app.run(port=5000, debug=True)

