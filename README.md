FastAPI User & Calculation App

This project implements a FastAPI backend that supports user registration, secure login, and CRUD operations for calculations. It includes automated integration testing and a full CI/CD pipeline using GitHub Actions and Docker Hub.

Project Features
User Functionality

Register new users

Secure password hashing (Passlib bcrypt)

Login endpoint with password verification

Calculation Functionality

Create a calculation

Browse all calculations

Read a specific calculation

Update an existing calculation

Delete a calculation

Input validation and schema enforcement

Development and Deployment

Pydantic for data validation

SQLAlchemy ORM

SQLite for local testing

PostgreSQL in GitHub Actions

Full integration tests for users and calculations

CI/CD pipeline that:

Installs dependencies

Starts PostgreSQL

Runs tests

Builds Docker image

Pushes image to Docker Hub

How to Run Locally
1. Install Dependencies
pip install -r requirements.txt

2. Start the FastAPI Server
uvicorn app.main:app --reload


Open in browser:

http://localhost:8000/docs


This page allows testing the API interactively.

Running Tests

Run all integration tests:

pytest -vv


All tests must pass to confirm correct behavior.

Running Using Docker (Local Machine)
1. Pull the Docker Image
docker pull gunateja04/fastapi-user-calculation-app:latest

2. Run the Container
docker run -d -p 8000:8000 --name calcapp gunateja04/fastapi-user-calculation-app:latest


Access the live API:

http://localhost:8000/docs

GitHub Actions CI/CD

This repository includes a GitHub Actions workflow located in:

.github/workflows/ci.yml


The workflow performs:

Python setup

Dependency installation

PostgreSQL service startup

Integration testing

Docker image build

Docker Hub push (only after tests pass)

This ensures continuous integration and deployment reliability.

Docker Hub Repository

The application image is published at:

https://hub.docker.com/r/gunateja04/fastapi-user-calculation-app