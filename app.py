import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

import sys
import hashlib
print("RUNNING PYTHON:", sys.executable)
print("SCRYPT AVAILABLE:", hasattr(hashlib, "scrypt"))

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["TEMPLATES_AUTO_RELOAD"] = True
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///busyb.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show home page"""
    if session.get("user_id"):
        return render_template("index.html")

@app.route("/goal")
@login_required
def goal():
    return render_template("goal.html")

@app.route("/save_goal", methods=["POST"])
@login_required
def save_goal():
    main_goal = request.form.get("main_goal")
    subtask1 = request.form.get("subtask1")
    subtask2 = request.form.get("subtask2")
    subtask3 = request.form.get("subtask3")
    subtask4 = request.form.get("subtask4")

    if not main_goal:
        return apology("Please enter a main goal")

    # Insert goal into `goals` table
    goal_id = db.execute(
        "INSERT INTO goals (user_id, goal_text) VALUES (?, ?)",
        session["user_id"],
        main_goal
    )

    # Insert subtasks (skip empty ones)
    subtasks = [subtask1, subtask2, subtask3, subtask4]
    for task in subtasks:
        if task and task.strip():
            db.execute(
                "INSERT INTO subtasks (goal_id, task_text, completed) VALUES (?, ?, 0)",
                goal_id,
                task
            )

    # Redirect back to /tasks page to continue working
    return redirect("/tasks")


@app.route("/tasks")
@login_required
def tasks():
    user_id = session["user_id"]

    # Get all goals belonging to this user
    goals = db.execute("SELECT * FROM goals WHERE user_id = ?", user_id)

    for goal in goals:
        subtasks = db.execute("SELECT * FROM subtasks WHERE goal_id = ?", goal["id"])
        goal["subtasks"] = subtasks
        goal["completed_count"] = sum(1 for s in subtasks if s["completed"])
        goal["total_subtasks"] = len(subtasks)

    return render_template("tasks.html", goals=goals)

@app.route("/complete_task", methods=["POST"])
@login_required
def complete_task():
    import random

    task_id = request.form.get("task_id")
    if not task_id:
        return apology("No task ID provided")

    # Mark the task completed
    db.execute("UPDATE subtasks SET completed = 1 WHERE id = ?", task_id)

    # Get goal_id for this task
    goal_id = db.execute("SELECT goal_id FROM subtasks WHERE id = ?", task_id)[0]["goal_id"]

    # Count completed vs total subtasks
    total = db.execute("SELECT COUNT(*) AS n FROM subtasks WHERE goal_id = ?", goal_id)[0]["n"]
    completed = db.execute(
        "SELECT COUNT(*) AS n FROM subtasks WHERE goal_id = ? AND completed = 1", goal_id
    )[0]["n"]

    # Only assign a flower color if goal is fully completed
    if completed == total:
        flower_options = ["orange.png", "pink.png", "purple.png", "blue.png"]

        existing_color = db.execute(
            "SELECT flower_color FROM goals WHERE id = ?", goal_id
        )[0]["flower_color"]

        if not existing_color:  # handles None or empty string
            new_color = random.choice(flower_options)
            db.execute(
                "UPDATE goals SET flower_color = ? WHERE id = ?", new_color, goal_id
            )
            print(f"Goal {goal_id} completed! Assigned flower color: {new_color}")

    return redirect("/tasks")

@app.route("/garden")
@login_required
def garden():
   user_id = session["user_id"]
   goals = db.execute("""
    SELECT g.id,
           g.goal_text,
           g.flower_color,
           COALESCE(SUM(CASE WHEN s.completed = 1 THEN 1 ELSE 0 END), 0) AS completed_count,
           COUNT(s.id) AS total_subtasks
    FROM goals g
    LEFT JOIN subtasks s ON g.id = s.goal_id
    WHERE g.user_id = ?
    GROUP BY g.id
""", (user_id,))
   return render_template("garden.html", goals=goals)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any previous user_id
    session.clear()

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["password_hash"], request.form.get("password")
        ):
            return apology("invalid username or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/login")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Register user"""
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check username
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Check password
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Confirm password
        elif not request.form.get("confirmation"):
            return apology("please confirm password", 400)

        # Confirmation wasn't the same
        elif not request.form.get("confirmation") == request.form.get("password"):
            return apology("does not match password", 400)

        # Ensure new username and password aren't taken
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        if len(rows) != 0:
            return apology("username or password taken", 400)

        # Hash user's password
        pw_hash = generate_password_hash(password)

        # Insert into database
        new_user_id = db.execute(
            "INSERT INTO users (username, password_hash) VALUES(?, ?)", username, pw_hash
        )

        # Remember which user has logged in
        session["user_id"] = new_user_id

        # Redirect to home page
        return redirect("/")

    # User reached route via GET
    else:
        return render_template("signup.html")

if __name__ == "__main__":
    app.run(debug=True)