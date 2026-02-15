# SCHOOL_ATTENDANCE 🎓

A simple Django-based web application for managing school attendance.  
Teachers/Admins can manage students, classes, and mark daily attendance through a browser-friendly interface.

---

## ✨ Features

- Add and manage students and their details.
- Create and manage classes/sections.
- Mark daily attendance for each class.
- View attendance records by date and student.
- Django admin panel for full control of data.

> Note: Update this section if you add more features (reports, exports, etc.).

---

## 🧰 Tech Stack

- **Language:** Python
- **Framework:** Django (tested with Django 6.x)
- **Database:** SQLite (default Django DB)
- **Frontend:** Django templates, HTML, CSS

---

## 📁 Project Structure

At a high level, the project looks like this:

```bash
SCHOOL_ATTENDANCE/
└── school_attendance/
    ├── manage.py
    ├── school_attendance/      # Django project settings, URLs, WSGI, ASGI, etc.
    ├── <your_apps_here>/       # Apps for students, attendance, etc.
    └── ...
