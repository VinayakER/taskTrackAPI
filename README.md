# FastAPI Project

## Overview

This is a FastAPI application for managing projects and tasks. It includes endpoints for handling users, projects, and tasks with a relational database setup using SQLAlchemy.

## Features

- User management (create, update, deactivate)
- Project creation and management
- Task creation and management
- Relational database with SQLite

## Requirements

- Python 3.8+
- pip
- virtualenv (optional but recommended)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/VinayakER/taskTrackAPI.git
   cd taskTrackAPI
    ```
2. **Create and activate a virtual environment (optional but recommended):**

   ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
3. **Install the dependencies:**

   ```bash
    pip install -r requirements.txt
    ```
4. **Run the FastAPI application:**

   ```bash
    uvicorn app.main:app --reload
    ```