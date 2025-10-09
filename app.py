from flask import Flask, render_template, request, redirect, url_for, session
import requests
from hashlib import sha256
import random
from dto.services import QuestionService

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
    if request.method == "POST":
        user = request.form["user"]
        pwd = request.form["pwd"]
        pwd_hash = sha256(pwd.encode()).hexdigest()

        res = requests.post(
            f"{FASTAPI_URL}/login", json={"user_name": user, "password_hash": pwd_hash}
        )
        if res.status_code == 200:
            session["user"] = user
            return redirect(url_for("home"))
        return render_template("login.html", message="Invalid username or password")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))

@app.route("/home")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("home.html", user=session["user"])


@app.route("/quizz", methods=["GET", "POST"])
def quizz():
    if "user" not in session:
        return redirect(url_for("login"))

    # post
    if request.method == "POST":
        answers = request.form.to_dict(flat=False)
        print("Réponses utilisateur:", answers)

        questions = session.get("quiz_questions", [])

        results = []
        score = 0

        for q in questions:
            q_id = str(q.get("_id", q.get("id")))
            user_selected = answers.get(f"response_{q_id}", [])
            correct_answers = q.get("good_answers_texte", [])

            is_correct = sorted(user_selected) == sorted(q["good_answers_texte"])
            if is_correct:
                score += 1

            results.append({
                "question": q,
                "selected": user_selected,
                "correct_answers": correct_answers,
                "correct": is_correct
            })

        total = len(questions)
        QuestionService.save_quizz_result(results)
        session.pop("quiz_questions", None)

        return render_template(
            "results.html",
            user=session["user"],
            results=results,
            score=score,
            total=total
        )

    # get
    res = requests.get(f"{FASTAPI_URL}/question")
    all_questions = res.json() if res.status_code == 200 else []

    if len(all_questions) > 20:
        selected_questions = random.sample(all_questions, 20)
    else:
        selected_questions = all_questions

    # ✅ On garde les 20 questions dans la session
    session["quiz_questions"] = selected_questions

    return render_template("quizz.html", user=session["user"], questions=selected_questions)


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
