from flask import Flask, render_template, request, redirect, session
import sqlite3

from werkzeug.security import generate_password_hash, check_password_hash

from recommendation import recommend_career, get_top_careers


app = Flask(__name__)
app.secret_key = "career_guidance_secret"


def init_db():

    conn = sqlite3.connect("career.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            interest TEXT,
            programming INTEGER,
            problem_solving INTEGER,
            mathematics INTEGER,
            ai_interest INTEGER,
            design INTEGER,
            security INTEGER,
            communication INTEGER,
            recommended_career TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


init_db()


# =========================================
# HOME
# =========================================

@app.route("/")
def home():

    return render_template("index.html")


# =========================================
# REGISTER
# =========================================

@app.route("/register", methods=["GET", "POST"])
def register():

    error = None

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        conn = sqlite3.connect("career.db")
        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                INSERT INTO users(name, email, password)
                VALUES (?, ?, ?)
                """,
                (
                    name,
                    email,
                    hashed_password
                )
            )

            conn.commit()

        except sqlite3.IntegrityError:

            conn.close()

            error = "This email is already registered."

            return render_template(
                "register.html",
                error=error
            )

        conn.close()

        return redirect("/login")

    return render_template(
        "register.html",
        error=error
    )


# =========================================
# LOGIN
# =========================================

@app.route("/login", methods=["GET", "POST"])
def login():

    error = None

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("career.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        )

        user = cursor.fetchone()

        conn.close()

        if user:

            if check_password_hash(
                user[3],
                password
            ):

                session["name"] = user[1]

                return redirect("/dashboard")

        error = "Incorrect email or password."

    return render_template(
        "login.html",
        error=error
    )


# =========================================
# DASHBOARD
# =========================================

@app.route("/dashboard")
def dashboard():

    if "name" not in session:

        return redirect("/login")

    return render_template(
        "dashboard.html",
        name=session["name"]
    )


# =========================================
# LOGOUT
# =========================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# =========================================
# ASSESSMENT
# =========================================

@app.route("/assessment", methods=["GET", "POST"])
def assessment():

    if "name" not in session:

        return redirect("/login")

    if request.method == "POST":

        interest = request.form["interest"]

        programming = int(
            request.form["programming"]
        )

        problem_solving = int(
            request.form["problem_solving"]
        )

        mathematics = int(
            request.form["mathematics"]
        )

        ai_interest = int(
            request.form["ai_interest"]
        )

        design = int(
            request.form["design"]
        )

        security = int(
            request.form["security"]
        )

        communication = int(
            request.form["communication"]
        )


        (
            career,
            scores,
            details,
            match_percentages
        ) = recommend_career(

            interest,

            programming,

            problem_solving,

            mathematics,

            ai_interest,

            design,

            security,

            communication
        )


        top_careers = get_top_careers(
            scores
        )


        conn = sqlite3.connect("career.db")
        cursor = conn.cursor()


        cursor.execute("""
            INSERT INTO assessments
            (
                user_name,
                interest,
                programming,
                problem_solving,
                mathematics,
                ai_interest,
                design,
                security,
                communication,
                recommended_career
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (

            session["name"],

            interest,

            programming,

            problem_solving,

            mathematics,

            ai_interest,

            design,

            security,

            communication,

            career
        ))


        conn.commit()
        conn.close()


        return render_template(
            "result.html",

            career=career,

            scores=scores,

            details=details,

            top_careers=top_careers,

            match_percentages=match_percentages
        )


    return render_template(
        "assessment.html"
    )


# =========================================
# HISTORY
# =========================================

@app.route("/history")
def history():

    if "name" not in session:

        return redirect("/login")


    conn = sqlite3.connect("career.db")
    cursor = conn.cursor()


    cursor.execute("""
        SELECT
            id,
            interest,
            programming,
            problem_solving,
            mathematics,
            ai_interest,
            design,
            security,
            communication,
            recommended_career
        FROM assessments
        WHERE user_name=?
        ORDER BY id DESC
    """, (
        session["name"],
    ))


    assessments = cursor.fetchall()

    conn.close()


    return render_template(
        "history.html",
        assessments=assessments
    )


# =========================================
# HISTORY RESULT
# =========================================

@app.route("/history/result/<int:assessment_id>")
def history_result(assessment_id):

    if "name" not in session:

        return redirect("/login")


    conn = sqlite3.connect("career.db")
    cursor = conn.cursor()


    cursor.execute("""
        SELECT
            id,
            interest,
            programming,
            problem_solving,
            mathematics,
            ai_interest,
            design,
            security,
            communication,
            recommended_career
        FROM assessments
        WHERE id=? AND user_name=?
    """, (

        assessment_id,

        session["name"]
    ))


    assessment_record = cursor.fetchone()

    conn.close()


    if assessment_record is None:

        return """
        <h2>Assessment Result Not Found</h2>

        <p>
            The selected assessment could not be found.
        </p>

        <a href="/history">
            Back to Assessment History
        </a>
        """


    (
        assessment_id,
        interest,
        programming,
        problem_solving,
        mathematics,
        ai_interest,
        design,
        security,
        communication,
        saved_career
    ) = assessment_record


    (
        calculated_career,
        scores,
        calculated_details,
        match_percentages
    ) = recommend_career(

        interest,

        programming,

        problem_solving,

        mathematics,

        ai_interest,

        design,

        security,

        communication
    )


    # Keep the career that was saved
    # when the original assessment was submitted.

    career = saved_career


    from recommendation import CAREER_DETAILS


    details = CAREER_DETAILS[career]


    top_careers = get_top_careers(
        scores
    )


    return render_template(

        "result.html",

        career=career,

        scores=scores,

        details=details,

        top_careers=top_careers,

        match_percentages=match_percentages
    )


# =========================================
# SHORT HISTORY RESULT URL
# =========================================

@app.route("/history/<int:assessment_id>")
def history_result_short(assessment_id):

    return redirect(
        f"/history/result/{assessment_id}"
    )


# =========================================
# RESULT BY ID
# =========================================

@app.route("/result/<int:assessment_id>")
def result_by_id(assessment_id):

    return redirect(
        f"/history/result/{assessment_id}"
    )


# =========================================
# RUN APPLICATION
# =========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )