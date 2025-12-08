# FastAPI User Calculation App

This project is a small full-stack web application built with **FastAPI**, **SQLAlchemy**, and **SQLite**.  
Users can register, log in, perform calculations, view a report/summary, and manage their profile information (including changing their password).

The project is containerized with **Docker** and uses **GitHub Actions** for CI/CD to run tests and automatically build & push a Docker image to Docker Hub.

--- 

## Features

### Authentication & Security
- User registration with unique email.
- Login with JWT-based authentication.
- Passwords hashed using **passlib[bcrypt]** (no plain-text storage).
- Protected routes that require a valid JWT.

### Calculations (BREAD)
- Perform basic operations: `add`, `sub`, `mul`, `div`, `pow`.
- **B**rowse all calculations for the logged-in user.
- **R**ead individual calculation records (via API).
- **E**dit existing calculations.
- **A**dd new calculations.
- **D**elete calculations.
- Simple HTML page (`/calculations-page`) that calls the API and shows the user’s calculations.

### Reports / History
- `/reports/summary` API returns:
  - Total number of calculations.
  - Average values of operands `a` and `b`.
  - Count of each operation type.
- `/report-page` shows a simple HTML summary page for the logged-in user.

### User Profile & Password Change (Final Project Feature)
- `/profile-page` front-end to:
  - View current username and email.
  - Update username and/or email.
  - Change password by providing old password and new password.
- Backend routes:
  - `GET /users/me` – get current profile.
  - `PUT /users/me` – update profile fields.
  - `POST /users/me/change-password` – secure password change.

### CI/CD & Docker
- GitHub Actions workflow:
  - Installs dependencies.
  - Runs unit and integration tests.
  - Builds and pushes Docker image to Docker Hub on push / pull request.
- Docker image is available publicly on Docker Hub.

---

## Tech Stack

- **Backend:** FastAPI, Uvicorn
- **Database:** SQLite + SQLAlchemy
- **Auth:** JWT (python-jose), passlib[bcrypt]
- **Frontend:** Simple HTML + JavaScript (no framework)
- **Testing:** pytest (unit & integration), Playwright (E2E – optional locally)
- **CI/CD:** GitHub Actions
- **Containerization:** Docker

---

## Getting Started (Run Locally)

### 1. Clone the repository

```bash
git clone https://github.com/gt-codes04/fastapi-user-calculation-app.git
cd fastapi-user-calculation-app
2. Create and activate a virtual environment
Windows (PowerShell):

bash
Copy code
python -m venv .venv
.venv\Scripts\activate
macOS / Linux:

bash
Copy code
python -m venv .venv
source .venv/bin/activate
3. Install dependencies
bash
Copy code
pip install --upgrade pip
pip install -r requirements.txt
4. Run the application
bash
Copy code
uvicorn app.main:app --reload
By default, the app runs at: http://localhost:8000

5. Front-end pages
After starting the server, you can access:

Register page:
http://localhost:8000/register-page

Login page:
http://localhost:8000/login-page

Calculations page:
http://localhost:8000/calculations-page

Report page:
http://localhost:8000/report-page

Profile page (final feature):
http://localhost:8000/profile-page

Interactive API docs:
http://localhost:8000/docs

Running Tests Locally
1. Unit + Integration tests (used in CI)
From the project root, with the virtual environment activated:

bash
Copy code
pytest tests/unit tests/integration -vv
This runs:

Unit tests for the calculation logic.

Integration tests for:

Users (register/login)

Calculations (BREAD)

Reports summary

2. End-to-End (E2E) tests with Playwright (optional, local only)
If you want to run the Playwright browser-based tests locally:

Install Playwright browsers once:

bash
Copy code
playwright install
Run all tests including E2E:

bash
Copy code
pytest tests/e2e -vv
Note: In CI (GitHub Actions), only unit + integration tests are executed.
E2E tests are intended to be run locally where Playwright browsers are installed.

Docker
Docker Hub Repository
Public Docker image:

https://hub.docker.com/r/gunateja04/fastapi-user-calculation-app

Pull the image
bash
Copy code
docker pull gunateja04/fastapi-user-calculation-app:latest
Run the container
bash
Copy code
docker run -p 8000:8000 gunateja04/fastapi-user-calculation-app:latest
Then open:

http://localhost:8000/register-page

http://localhost:8000/login-page

etc., as described above.

CI/CD (GitHub Actions)
The workflow file is located at: .github/workflows/ci.yml

On each push or pull request:

Set up Python.

Install dependencies.

Run unit + integration tests:

bash
Copy code
pytest tests/unit tests/integration -vv
Log in to Docker Hub using repository secrets:

DOCKERHUB_USERNAME

DOCKERHUB_TOKEN

Build and push the Docker image:

text
Copy code
gunateja04/fastapi-user-calculation-app:latest
A successful run means:

All tests passed.

New Docker image was pushed to Docker Hub.

Project Structure (High-Level)
text
Copy code
app/
  main.py                # FastAPI app, page routes, router includes
  db.py                  # Database session & engine
  models.py              # SQLAlchemy models (User, Calculation)
  schemas.py             # Pydantic schemas
  security.py            # Password hashing / verify helpers
  auth.py                # JWT creation & utilities
  crud.py                # CRUD helpers for users & calculations
  routers/
    auth_routes.py       # Login route
    users.py             # Register, profile, change password
    calculations.py      # BREAD endpoints for calculations
    reports.py           # Reports/summary endpoints
    ui.py                # (if used) simple UI helpers

frontend/
  register.html
  login.html
  calculations.html
  reports.html
  profile.html           # Final feature front-end

tests/
  unit/
  integration/
  e2e/
Notes
This project was developed as a course assignment to practice:

Creating and testing FastAPI applications.

Integrating authentication and database models.

Using CI/CD with GitHub Actions and Docker Hub.

The final feature implemented is the User Profile & Password Change flow with full backend + front-end integration and tests.

yaml
Copy code

---

## ✅ Git commands to push the updated README to your branch

1. Make sure you’re on your **project root** and the correct branch (sounds like `final-feature`):

```bash
cd C:\Users\Guna Teja\OneDrive\Desktop\fastapi-user-calculation-app
git checkout final-feature
Open README.md in VS Code and replace its contents with the README above. Save the file.

Stage and commit:

bash
Copy code
git status          # just to see changes
git add README.md
git commit -m "Add final README with run instructions, tests, and Docker Hub link"
Push to GitHub:

bash
Copy code
git push origin final-feature
If you already have a PR from final-feature to main, GitHub will automatically show the updated README in that PR.
If not, create a new Pull Request from final-feature → main.