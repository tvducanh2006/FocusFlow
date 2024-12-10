import os
from cs50 import SQL
from flask import Flask, render_template, request, redirect, session, flash
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required
from datetime import datetime, timedelta

# Configure application
app = Flask(__name__)

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure SQLite database
db = SQL("sqlite:///planner.db")

# Index Route
@app.route("/")
def index():
    return render_template("index.html")

# About Route
@app.route("/about")
def about():
    return render_template("about.html")

# Register Route
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register a new user"""
    if request.method == "POST":
        # Get form inputs
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Validation
        if not first_name or not last_name or not username or not password:
            flash("All fields are required!", "error")
            return redirect("/register")
        if password != confirmation:
            flash("Passwords do not match!", "error")
            return redirect("/register")

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Insert user into the database
        try:
            db.execute(
                """
                INSERT INTO users (first_name, last_name, username, password)
                VALUES (?, ?, ?, ?)
                """,
                first_name, last_name, username, hashed_password,
            )
            flash("Account created successfully! Please log in.", "success")
            return redirect("/login")
        except Exception as e:
            flash("Username already exists or an error occurred. Try again.", "error")
            print(e)
            return redirect("/register")

    # GET request: Render the registration form
    return render_template("register.html")

# Log In Route
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log in a user"""
    if request.method == "POST":
        # Debugging to ensure form fields are received
        print("Form Data:", request.form)

        # Get form inputs
        username = request.form.get("username")
        password = request.form.get("password")

        # Validation for missing fields
        if not username or not password:
            flash("Username and password are required!", "error")
            return redirect("/login")

        # Check if the user exists in the database
        user = db.execute("SELECT * FROM users WHERE username = ?", username)
        print("User Data:", user)  # Debug to ensure query works

        # Validate user and password
        if len(user) != 1 or not check_password_hash(user[0]["password"], password):
            flash("Invalid username or password!", "error")
            return redirect("/login")

        # Log the user in (set session variables)
        session["user_id"] = user[0]["id"]
        session["first_name"] = user[0]["first_name"]
        session["last_name"] = user[0]["last_name"]
        flash(f"Welcome back, {user[0]['first_name']}!", "success")
        return redirect("/dashboard")

    # GET request: Render the login form
    return render_template("login.html")

# Log Out Route
@app.route("/logout")
@login_required
def logout():
    """Log the user out and clear the session"""
    session.clear()  # Clear all session data
    flash("You have been logged out successfully.", "info")
    return redirect("/")  # Redirect to the homepage

# Tasks Route
@app.route("/tasks", methods=["GET", "POST"])
@login_required
def tasks():
    if request.method == "POST":
        name = request.form.get("name")
        deadline_date = request.form.get("deadline_date")
        deadline_time = request.form.get("deadline_time")
        priority = request.form.get("priority")
        complexity = request.form.get("complexity")
        subject = request.form.get("subject")
        estimated_time = request.form.get("estimated_time")

        if not all([name, deadline_date, deadline_time, priority, complexity, subject, estimated_time]):
            flash("All fields are required!", "error")
            return redirect("/tasks")

        try:
            # Set remaining_time equal to estimated_time initially
            db.execute(
                """
                INSERT INTO tasks (
                    name, priority, deadline_date, deadline_time, complexity, subject, estimated_time, user_id, remaining_time
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                name, priority, deadline_date, deadline_time, complexity, subject, estimated_time, session["user_id"],
                int(estimated_time) * 3600  # Convert hours to seconds
            )
            flash("Task added successfully!", "success")
        except Exception as e:
            flash("Error adding task. Please try again.", "error")
            print(e)

        return redirect("/tasks")
    else:
        tasks = db.execute("SELECT * FROM tasks WHERE user_id = ?", session["user_id"])
        return render_template("tasks.html", tasks=tasks)

# Calendar Route
@app.route("/calendar")
@login_required
def calendar():
    # Get query parameters for view and navigation
    view = request.args.get("view", "month")
    direction = request.args.get("direction", None)

    # Default date to today
    today = datetime.today()
    current_date = session.get("current_date", today)

    if direction == "prev":
        current_date -= timedelta(days=30 if view == "month" else 7)
    elif direction == "next":
        current_date += timedelta(days=30 if view == "month" else 7)

    # Save the updated date in the session
    session["current_date"] = current_date

    print("Current Date in Session:", session.get("current_date"))  # Debugging

    # Calculate first day of the month and weekday
    first_day_of_month = current_date.replace(day=1)

    # Generate data for month or agenda view
    if view == "month":
        days = []
        first_weekday = first_day_of_month.weekday()
        blank_cells = (first_weekday + 1) % 7

        for _ in range(blank_cells):
            days.append({"date": None, "tasks": []})

        for i in range(1, 32):  # Assuming max 31 days
            date = first_day_of_month + timedelta(days=i - 1)
            if date.month != first_day_of_month.month:
                break
            tasks = db.execute(
                "SELECT name, deadline_time FROM tasks WHERE user_id = ? AND deadline_date = ?",
                session["user_id"], date.strftime("%Y-%m-%d")
            )
            days.append({"date": date.day, "tasks": tasks})

        return render_template(
            "calendar.html",
            days=days,
            view=view,
            month_name=current_date.strftime("%B"),
            current_year=current_date.year,
        )

    elif view == "agenda":
        agenda = []
        first_day_of_month = current_date.replace(day=1)
        days_in_month = (first_day_of_month.replace(month=(current_date.month % 12) + 1, day=1) - timedelta(days=1)).day

        for i in range(days_in_month):
            date = first_day_of_month + timedelta(days=i)
            tasks = db.execute(
                """
                SELECT name, deadline_time, estimated_time
                FROM tasks
                WHERE user_id = ? AND deadline_date = ?
                """,
                session["user_id"], date.strftime("%Y-%m-%d")
            )
            if tasks:
                agenda.append({"date": date, "tasks": tasks})

        return render_template(
            "agenda.html",
            agenda=agenda,
            view=view,
            month_name=current_date.strftime("%B"),
            current_year=current_date.year,
        )

# Dashboard Route
@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    """Dashboard for Pomodoro timer and task management"""
    if request.method == "POST":
        task_id = request.form.get("task_id")
        time_spent = int(request.form.get("time_spent", 0))  # Time spent in seconds

        # Add the time spent to focus_stats for the selected task
        db.execute(
            """
            INSERT INTO focus_stats (user_id, task_id, date, work_time)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id, task_id, date)
            DO UPDATE SET work_time = work_time + ?
            """,
            session["user_id"], task_id, datetime.now().date(), time_spent, time_spent
        )

        # Update the remaining time in the tasks table
        db.execute(
            """
            UPDATE tasks
            SET remaining_time = remaining_time - ?
            WHERE id = ? AND user_id = ? AND remaining_time IS NOT NULL
            """,
            time_spent, task_id, session["user_id"]
        )

        return redirect("/dashboard")

    # Fetch tasks with remaining time calculation
    tasks = db.execute(
        """
        SELECT tasks.id, tasks.name, tasks.deadline_date, tasks.deadline_time,
               tasks.estimated_time * 3600 AS estimated_time, -- Convert to seconds for comparison
               tasks.remaining_time
        FROM tasks
        WHERE tasks.user_id = ? AND tasks.completed_at IS NULL
        ORDER BY tasks.deadline_date ASC
        """,
        session["user_id"]
    )

    return render_template("dashboard.html", tasks=tasks)

# Updates the remaining time for tasks asynchronously via AJAX
@app.route("/update_remaining_time", methods=["POST"])
@login_required
def update_remaining_time():
    data = request.get_json()
    task_id = data.get("task_id")
    remaining_time = data.get("remaining_time")

    db.execute(
        "UPDATE tasks SET remaining_time = ? WHERE id = ? AND user_id = ?",
        remaining_time, task_id, session["user_id"]
    )
    return jsonify({"status": "success"})
