from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from recommendation import recommend_career

app = Flask(__name__)

# Secret key for sessions
app.secret_key = "career_guidance_secret"


# =========================
# HOME
# =========================

@app.route("/")
def home():
    return render_template("index.html")


# =========================
# REGISTER
# =========================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        # Hash password before storing it
        hashed_password = generate_password_hash(password)

        conn = sqlite3.connect("career.db")
        cursor = conn.cursor()

        try:

            cursor.execute(
                "INSERT INTO users(name, email, password) VALUES(?, ?, ?)",
                (name, email, hashed_password)
            )

            conn.commit()

        except sqlite3.IntegrityError:

            conn.close()

            return """
            <h2>Email already registered!</h2>
            <a href="/register">Try Again</a>
            """

        conn.close()

        return redirect("/login")

    return render_template("register.html")


# =========================
# LOGIN
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():

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

            # Check hashed password
            if check_password_hash(user[3], password):

                # Store user's name in session
                session["name"] = user[1]

                return redirect("/dashboard")

        return """
        <h2>Invalid Email or Password</h2>
        <a href="/login">Try Again</a>
        """

    return render_template("login.html")


# =========================
# DASHBOARD
# =========================

@app.route("/dashboard")
def dashboard():

    if "name" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        name=session["name"]
    )


# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# =========================
# CAREER ASSESSMENT
# =========================

@app.route("/assessment", methods=["GET", "POST"])
def assessment():

    if "name" not in session:
        return redirect("/login")

    if request.method == "POST":

        interest = request.form["interest"]

        programming = int(request.form["programming"])
        problem_solving = int(request.form["problem_solving"])
        mathematics = int(request.form["mathematics"])
        ai_interest = int(request.form["ai_interest"])
        design = int(request.form["design"])
        security = int(request.form["security"])
        communication = int(request.form["communication"])


        # Get career recommendation
        career, scores, details = recommend_career(
            interest,
            programming,
            problem_solving,
            mathematics,
            ai_interest,
            design,
            security,
            communication
        )


        # =========================
        # SAVE ASSESSMENT
        # =========================

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


        # Display result
        return render_template(
            "result.html",
            career=career,
            scores=scores,
            details=details
        )

    return render_template("assessment.html")


# =========================
# ASSESSMENT HISTORY
# =========================

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
    """, (session["name"],))

    assessments = cursor.fetchall()

    conn.close()

    return render_template(
        "history.html",
        assessments=assessments
    )


# =========================
# RUN APPLICATION
# =========================

if __name__ == "__main__":
    app.run(debug=True)