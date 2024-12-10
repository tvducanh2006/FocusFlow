# FocusFlow – Your All-in-One Study Planner

FocusFlow is a web application designed to help students and professionals manage their tasks, schedules, and study sessions efficiently. Built with Flask, SQLite, and Bootstrap, FocusFlow integrates task management, calendar views, and a Pomodoro timer for optimal productivity.

---

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Setup Instructions](#setup-instructions)
4. [How to Use](#how-to-use)
5. [Database Schema](#database-schema)
6. [Project Structure](#project-structure)
7. [Future Improvements](#future-improvements)

---

## Introduction
FocusFlow was developed as a CS50 Final Project to create a comprehensive platform for managing tasks and tracking study habits. Whether you’re juggling assignments, preparing for exams, or managing daily responsibilities, FocusFlow provides the tools you need to stay organized.

This project employs:
- Python and Flask for backend logic
- SQLite for database management
- HTML, CSS, and Bootstrap for responsive design
- JavaScript for interactivity

---

## Features
1. **User Authentication**: Secure login and registration system with hashed passwords.
2. **Task Management**: Add, edit, and delete tasks with details like priority, subject, deadlines, and complexity.
3. **Calendar Integration**: View tasks in monthly or agenda formats.
4. **Pomodoro Timer**: Track your study sessions and monitor progress.
5. **Progress Tracking**: View stats like total work time, break time, and completed tasks. *(coming soon)*

---

## Setup Instructions

To run FocusFlow, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/tvducanh2006/FocusFlow.git
   cd FocusFlow
   ```

2. **Set Up a Virtual Environment** (Optional but Recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Linux/MacOS
   venv\Scripts\activate     # For Windows
   ```

3. **Install Dependencies**:
   Use the `requirements.txt` file to install all necessary libraries.
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the Database**:
   The `planner.db` file is included in the repository, so no setup is required. If you want to recreate the database from scratch, run the following schema in an SQLite environment:
   ```sql
   CREATE TABLE users (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       username TEXT NOT NULL UNIQUE,
       first_name TEXT NOT NULL,
       last_name TEXT NOT NULL,
       password TEXT NOT NULL
   );

   CREATE TABLE tasks (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       name TEXT NOT NULL,
       priority TEXT NOT NULL,
       deadline_date TEXT NOT NULL,
       deadline_time TEXT NOT NULL,
       complexity TEXT NOT NULL,
       subject TEXT NOT NULL,
       estimated_time INTEGER NOT NULL,
       remaining_time INTEGER DEFAULT NULL,
       completed_at DATETIME DEFAULT NULL,
       user_id INTEGER NOT NULL,
       FOREIGN KEY (user_id) REFERENCES users (id)
   );

   CREATE TABLE focus_stats (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       user_id INTEGER NOT NULL,
       date DATE NOT NULL,
       work_time INTEGER DEFAULT 0,
       break_time INTEGER DEFAULT 0,
       completed_tasks INTEGER DEFAULT 0,
       task_id INTEGER,
       FOREIGN KEY (user_id) REFERENCES users (id)
   );

   CREATE INDEX idx_tasks_user_id ON tasks (user_id);
   CREATE INDEX idx_focus_stats_user_id ON focus_stats (user_id);
   ```

5. **Run the Application**:
   Start the Flask server by running:
   ```bash
   flask run
   ```
   **Note**: After running the server, Flask will provide a URL where your application is accessible. This URL may vary depending on your development environment.

   Open your web browser and navigate to the URL provided in your terminal to access the application.

---

## How to Use

1. **Registration**:
   - Go to the registration page.
   - Enter your first name, last name, username, password, and password confirmation.
   - Click "Register" to create your account.

2. **Log In**:
   - Use your registered username and password to log in.

3. **Dashboard**:
   - View your tasks and Pomodoro timer.
   - Select your task & start, pause, or reset your timer to track work sessions.
   - Remaining time for each task will be updated simultaneously

4. **Tasks Manager**:
   - Add new tasks with details like priority, deadline, and estimated time. The new tasks will appear in **Task List** table
   - Edit or delete tasks as needed.

5. **Calendar**:
   - View tasks in a calendar format (monthly or agenda view).
   - Navigate between months or weeks.

---

## Database Schema

FocusFlow uses a relational SQLite database with the following schema:

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    priority TEXT NOT NULL,
    deadline_date TEXT NOT NULL,
    deadline_time TEXT NOT NULL,
    complexity TEXT NOT NULL,
    subject TEXT NOT NULL,
    estimated_time INTEGER NOT NULL,
    remaining_time INTEGER DEFAULT NULL,
    completed_at DATETIME DEFAULT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE focus_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    date DATE NOT NULL,
    work_time INTEGER DEFAULT 0,
    break_time INTEGER DEFAULT 0,
    completed_tasks INTEGER DEFAULT 0,
    task_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE INDEX idx_tasks_user_id ON tasks (user_id);
CREATE INDEX idx_focus_stats_user_id ON focus_stats (user_id);
```

---

## Project Structure

Here is the folder structure of FocusFlow:

```
FocusFlow/
│
├── flask_session/ # Flask session data storage
├── static/ # Static files like CSS and JavaScript
├── templates/ # HTML templates for Flask
├── venv/ # Virtual environment (optional)
├── app.py # Main application logic
├── DESIGN.md # Technical design document
├── helpers.py # Helper functions and decorators
├── planner.db # SQLite database
├── README.md # User documentation (this file)
└── requirements.txt # Python dependencies
```

---

## Future Improvements

- **Two-Factor Authentication**: Add an extra layer of security during login.
- **Notifications**: Implement email or in-app notifications for upcoming tasks or deadlines.
- **Data Visualization**: Provide graphical insights into productivity stats (e.g., work vs. break time).
- **Mobile-Friendly Design**: Optimize layout for smaller screens and mobile devices.

---

## Sources

- [CS50](https://cs50.yale.edu/2024/fall/) course materials
- [Flask documentation](https://flask.palletsprojects.com/en/2.3.x/) – for routing and session management
- [Jinja documentation](https://jinja.palletsprojects.com/en/3.1.x/) – for rendering HTML templates dynamically
- [Python documentation](https://docs.python.org/3/) – for general-purpose programming and modules like `datetime`
- [SQLite documentation](https://sqlite.org/docs.html) – for database integration
- [Bootstrap documentation](https://getbootstrap.com/docs/5.3/getting-started/introduction/) – for responsive web design and layout

### Timer Functionality
- [HTML CSS JavaScript Project - Pomodoro Timer](https://www.youtube.com/watch?v=_9QQf-RpPlM) by Code With Sahand – inspiration for implementing the Pomodoro timer
- [JavaScript Timers Guide](https://developer.mozilla.org/en-US/docs/Web/API/setTimeout) by MDN Web Docs – for understanding `setInterval` and `setTimeout` used in `timer.js`
- [Async Flask Functions with JavaScript](https://flask.palletsprojects.com/en/2.3.x/patterns/javascript/) – for integrating timers with backend routes (e.g., `/update_remaining_time`)
- [MDN Web Docs on `setInterval`](https://developer.mozilla.org/en-US/docs/Web/API/setInterval) - Used to implement the timer functionality in `timer.js`.
- [MDN Web Docs on `addEventListener`](https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener) - Used extensively in `timer.js` to manage user interactions.
- [MDN Web Docs on Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API) - Used to implement dynamic communication between the frontend and backend in `timer.js`.
- [Learn Fetch API in 6 Minutes](https://www.youtube.com/watch?v=cuEtnrL9-H0) by Web Dev Simplified – for handling navigation events and AJAX calls in `timer.js`

### Calendar Views
- [Date and Time Manipulation](https://docs.python.org/3/library/datetime.html) by Python Docs – for using `datetime` and `timedelta` to calculate dates for calendar logic
- [HTML Table Calendar](https://css-tricks.com/building-a-table-calendar-with-html-css/) by CSS-Tricks – for the frontend design of the calendar
- [MDN Web Docs: Tables](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/table) – For table-based calendar rendering
- [MDN Web Docs on `Date` Object](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date) - Referenced for date and time manipulations in both the calendar and timer functionalities.
