from flask import Flask, render_template, request, redirect, url_for, session, flash
from hashlib import sha256
import random
import requests
from dto.services import QuestionService, QuizzService

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
    filtered = [q for q in all_questions if q.get("subject") == subject]
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


@app.route("/teacher/quiz-setup")
def teacher_quiz_setup():
    if "user" not in session:
        return redirect(url_for("login"))
    subjects = get_subjects_from_mongo()
    return render_template("teacher_quiz_setup.html", subjects=subjects)


@app.route("/teacher/quiz-preview")
def teacher_quiz_preview():
    if "user" not in session:
        return redirect(url_for("login"))

    subject = request.args.get("theme")
    try:
        n = int(request.args.get("nb", "5"))
    except ValueError:
        n = 5

    pool = get_questions_by_subject(subject)
    if not pool:
        flash(f"Aucune question trouvée pour le thème « {subject} »")
        return redirect(url_for("teacher_quiz_setup"))

    k = min(n, len(pool))
    sample = random.sample(pool, k)

    QuizzService.get_collection_quizz().insert_one({
        "subject": subject,
        "questions": sample,
        "count": k
    })

    return render_template(
        "teacher_quiz_preview.html",
        subject=subject,
        questions=sample,
        count=k,
        total=len(pool)
    )


@app.route("/quizz/archivedquizz/")
def archived_quizz_list():
    if "user" not in session:
        return redirect(url_for("login"))

    quizzes = QuizzService.get_all_quizzs()
    return render_template("archivedquizz.html", quizzes=quizzes)


@app.route("/quizz/archivedquizz/<quizz_id>")
def archived_quizz(quizz_id):
    if "user" not in session:
        return redirect(url_for("login"))

    quizz = QuizzService.get_quizz_by_id(quizz_id)
    print("DEBUG quizz:", quizz)
    if not quizz:
        return render_template("error.html", message="Quiz introuvable")

    return render_template("archived_quizz_detail.html", quizz=quizz)

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

if __name__ == "__main__":
    app.run(port=5000, debug=True)

