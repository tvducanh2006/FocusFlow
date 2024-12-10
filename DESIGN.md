# FocusFlow – Your All-in-One Study Planner

[`Link to my project on GitHub`](https://github.com/tvducanh2006/FocusFlow)
[`Youtube Video Here`](https://youtu.be/IruZrABx_EM)

## Table of Contents
1. [Introduction](#introduction)
2. [Backend Design](#backend-design)
   - [Overview](#overview)
   - [Routing Details](#routing-details)
   - [Database Design](#database-design)
   - [Security Considerations](#security-considerations)
3. [Frontend Design](#frontend-design)
   - [HTML Templates](#html-templates)
   - [CSS Styling](#css-styling-&-javacsript-functionality)
4. [Design Decisions](#design-decisions)

---

## Introduction

FocusFlow is a task management and productivity application designed to help users organize their tasks, manage deadlines, and improve productivity with features like a Pomodoro timer and task prioritization. The project uses **Flask** for the backend, **SQLite** as the database, and **HTML/CSS** for the frontend, with additional support from JavaScript for interactivity.

---

## Backend Design

### Overview

The backend is implemented using Flask and SQLite. It consists of:
1. **`app.py`:** Manages routing and business logic.
2. **`helpers.py`:** Contains utility functions like the `login_required` decorator.

### Routing Details

- [`index`](https://github.com/tvducanh2006/FocusFlow/blob/main/app.py#L20)
- [`about`](https://github.com/tvducanh2006/FocusFlow/blob/main/app.py#L25)
- [`register`](https://github.com/tvducanh2006/FocusFlow/blob/main/app.py#L30)
- [`login`](https://github.com/tvducanh2006/FocusFlow/blob/main/app.py#L72)
- [`logout`](https://github.com/tvducanh2006/FocusFlow/blob/main/app.py#L108)
- [`tasks`](https://github.com/tvducanh2006/FocusFlow/blob/main/app.py#L117)
- [`calendar`](https://github.com/tvducanh2006/FocusFlow/blob/main/app.py#L155)
- [`dashboard`](https://github.com/tvducanh2006/FocusFlow/blob/main/app.py#L233)
- [`update_remaining_time`](https://github.com/tvducanh2006/FocusFlow/blob/main/app.py#L280)

> Click each route to jump directly to its corresponding code in `app.py`.

### Database Design

#### Schema Overview
The SQLite database consists of three tables: `users`, `tasks`, and `focus_stats`. The schema ensures data integrity through relationships and constraints, and uses indexes for efficient queries.

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

### Security Considerations
- **Password Hashing:** Securely stores passwords using `generate_password_hash`.
- **Input Validation:** Prevents SQL injection with parameterized queries.
- **Session Security:** Sessions are securely managed to prevent unauthorized access.

---

## Frontend Design

### HTML Templates

Templates in `/templates` directory render dynamic content using Flask's Jinja2. Each file corresponds to a specific route or functionality:

| Template           | Purpose                                                                |
|--------------------|------------------------------------------------------------------------|
| `layout.html`      | Provides a consistent navigation bar and layout across all pages.      |
| `index.html`       | Displays the homepage with an overview of the application.             |
| `about.html`       | Details the application's features and design.                         |
| `register.html`    | Form for user registration.                                            |
| `login.html`       | Form for user login.                                                   |
| `tasks.html`       | Displays a list of tasks and provides a form for creating new tasks.   |
| `calendar.html`    | Visualizes tasks in a calendar format.                                 |
| `agenda.html`      | Presents tasks in an agenda-style list.                                |
| `dashboard.html`   | Includes the Pomodoro timer and task selection interface.              |

### CSS Styling & JavaScript Functionality

1. **`style.css`:** Adds styles, animations and hover effects for a polished user experience.
2. **`navigation.js`:** Handles navigation between calendar views with loading indicators.
3. **`timer.js`:** Implements the Pomodoro timer, including mode switching and task integration.

---

## Design Decisions

1. **Scalability:**
   - The database schema and code structure were designed to handle additional features (e.g., notifications, recurring tasks) with minimal rework.
   - Modular frontend and backend components allow for easier future updates.
   - Clear separation of concerns between backend and frontend for maintainability.

2. **Security:**
   - Password hashing ensures user data is securely stored.
   - Form validation and query parameter handling prevent common attacks (e.g., SQL injection).

3. **Usability:**
   - Features like flash messages, responsive design, and intuitive navigation were prioritized to enhance the user experience.
   - The use of a calendar and agenda view aligns with common productivity tools, making the platform intuitive for users.

4. **Consistency:**
   - Adherence to Flask's recommended structure ensures maintainability and readability.
   - CSS and Jinja templates promote a uniform look and feel across the application.

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
