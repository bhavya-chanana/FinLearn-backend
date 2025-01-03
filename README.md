# FinLearn Backend

Welcome to the FinLearn backend repository! This project serves as the backend for the FinLearn platform, a financial learning application designed to help users enhance their financial literacy.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

## Features

- User authentication and management
- Financial learning resources and materials
- Interactive quizzes and assessments
- Progress tracking for users
- RESTful API for frontend integration

## Technologies Used

- **Python**: The primary programming language for the backend.
- **Flask**: A lightweight WSGI web application framework.
- **SQLAlchemy**: For database management and ORM.
- **pytest**: For testing the application.

## Installation

To set up the FinLearn backend on your local machine, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/mittal-shreya/FinLearn-backend.git
   cd FinLearn-backend

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install the required packages:**

   ```bash 
   pip install -r requirements.txt
  
4. **Set up the configuration:**

Modify the config.py file to include your database and application settings.

5. **Run the application:**

    ```bash
    python app.py
