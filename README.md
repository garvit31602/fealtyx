# Flask CRUD App

This project is a simple Flask-based CRUD (Create, Read, Update, Delete) application that stores data about students. It’s designed to be deployed on [Vercel](https://vercel.com/) with the WSGI server `waitress`.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Running Locally](#running-locally)
6. [Deploying to Vercel](#deploying-to-vercel)
7. [API Endpoints](#api-endpoints)
8. [Troubleshooting](#troubleshooting)
9. [Contributing](#contributing)
10. [License](#license)

---

### Project Overview

This Flask app provides CRUD functionalities for managing student data, including creating new records, retrieving existing records, updating, and deleting entries.

---

### Features

- **List Students**: Retrieve a list of all students.
- **View Student Details**: Get detailed information for a specific student.
- **Add a Student**: Add new student records.
- **Update Student Information**: Modify existing student details.
- **Delete a Student**: Remove student records.

---

### Installation

To get started, ensure you have Python and pip installed on your system. Clone the repository and install the dependencies:

git clone https://github.com/garvit31602/fealtyx.git
cd fealtyx
pip install -r requirements.txt
If waitress is missing, install it separately with:

bash
Copy code
pip install waitress
Configuration
Create a vercel.json file in the root directory. This file configures Vercel for deployment and specifies the main Python file.

json
Copy code
{
    "version": 2,
    "builds": [
      {
        "src": "app.py",
        "use": "@vercel/python"
      }
    ],
    "routes": [
      {
        "src": "/(.*)",
        "dest": "/app.py"
      }
    ]
}
Note: Replace "app.py" with the filename of your Flask app if different.

Running Locally
To run the application locally:

Run the server with waitress:

bash
Copy code
waitress-serve --port=8000 app:app
Replace app:app with the filename and instance of your Flask application if different.

Open your browser and go to http://localhost:8000 to view the app.

Deploying to Vercel
To deploy the app to Vercel:

Install Vercel CLI (if not installed):

bash
Copy code
npm install -g vercel
Initialize the project on Vercel:

bash
Copy code
vercel init
Deploy:

bash
Copy code
vercel --prod
If successful, Vercel will provide a URL where your app is hosted.

### API Endpoints

| Endpoint               | Method | Description                           |
|------------------------|--------|---------------------------------------|
| `/students`            | GET    | Retrieve a list of all students       |
| `/students/<int:id>`   | GET    | Get details for a specific student    |
| `/students`            | POST   | Add a new student                     |
| `/students/<int:id>`   | PUT    | Update a specific student             |
| `/students/<int:id>`   | DELETE | Delete a specific student             |
| `/students/summary`    | POST   | Generate a summary for a student      |

Troubleshooting
404 Not Found on Vercel: Ensure that your vercel.json file correctly points to your main app file.
Invalid API Version: Ensure the version in vercel.json is set to "2".
Module Not Found Errors: Double-check requirements.txt for missing dependencies.
