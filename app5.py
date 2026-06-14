from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)
app.secret_key = "admin123"

# ---------------- DATABASE CONNECTION ----------------

def get_db_connection():
    conn = psycopg2.connect(
        os.environ.get("DATABASE_URL")
    )
    return conn

# ---------------- CREATE TABLE ----------------

def init_db():

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS volunteers(
        id SERIAL PRIMARY KEY,
        username VARCHAR(100),
        email VARCHAR(100),
        phone VARCHAR(20),
        city VARCHAR(100),
        interest VARCHAR(100),
        password VARCHAR(100)
    )
    """)

    conn.commit()
    cur.close()
    conn.close()

init_db()

# ---------------- TEMP STORAGE FOR ADMIN ----------------

stories = []
values_list = []
programs_list = []
team_list = []

# ---------------- HOME ----------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/gallery")
def gallery():
    return render_template("gallery.html")


@app.route("/donate")
def donate():
    return render_template("donate.html")


# ---------------- VOLUNTEER REGISTRATION ----------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        phone = request.form["phone"]
        city = request.form["city"]
        interest = request.form["interest"]
        password = request.form["password"]

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO volunteers
        (username,email,phone,city,interest,password)
        VALUES (%s,%s,%s,%s,%s,%s)
        """,
        (username, email, phone, city, interest, password))

        conn.commit()

        cur.close()
        conn.close()

        return render_template(
            "dash.html",
            name=username
        )

    return render_template("register11.html")


# ---------------- VIEW VOLUNTEERS ----------------

@app.route("/volunteers")
def volunteers():

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT * FROM volunteers
    """)

    data = cur.fetchall()

    cur.close()
    conn.close()

    return str(data)


# ---------------- ADMIN DASHBOARD ----------------

@app.route("/admin")
def admin():

    return render_template(
        "admin.html",
        story=stories,
        values=values_list,
        programs=programs_list,
        team=team_list
    )


# ---------------- STORY ----------------

@app.route("/add_story", methods=["POST"])
def add_story():

    content = request.form["content"]

    stories.append({
        "id": len(stories) + 1,
        "content": content
    })

    return redirect("/admin")


# ---------------- CORE VALUES ----------------

@app.route("/add_value", methods=["POST"])
def add_value():

    value = request.form["value"]

    values_list.append({
        "id": len(values_list) + 1,
        "value": value
    })

    return redirect("/admin")


# ---------------- PROGRAMS ----------------

@app.route("/add_program", methods=["POST"])
def add_program():

    name = request.form["name"]

    programs_list.append({
        "id": len(programs_list) + 1,
        "name": name
    })

    return redirect("/admin")


# ---------------- TEAM MEMBERS ----------------

@app.route("/add_team", methods=["POST"])
def add_team():

    name = request.form["name"]
    role = request.form["role"]

    team_list.append({
        "id": len(team_list) + 1,
        "name": name,
        "role": role
    })

    return redirect("/admin")


# ---------------- CLEAR DATA ----------------

@app.route("/clear_story")
def clear_story():

    stories.clear()
    return redirect("/admin")


@app.route("/clear_values")
def clear_values():

    values_list.clear()
    return redirect("/admin")


@app.route("/clear_programs")
def clear_programs():

    programs_list.clear()
    return redirect("/admin")


@app.route("/clear_team")
def clear_team():

    team_list.clear()
    return redirect("/admin")


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    return redirect("/")


# ---------------- RUN APP ----------------

if __name__ == "__main__":
    app.run(debug=True)