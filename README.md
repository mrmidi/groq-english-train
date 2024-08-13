# English Grammar Practice Web Application

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Development](#development)
- [Deployment](#deployment)
- [Acknowledgments](#acknowledgments)

## Project Overview

This project is an educational web application designed to help users practice English grammar. It focuses on exercises like converting direct speech to indirect speech and practicing various verb tenses. The application provides automated task generation, answer validation, and explanations, all accessible through a user-friendly web interface.

**Expandability**: The project is designed to be easily expandable with other types of tasks. The use of a `TaskFactory` pattern allows for the seamless addition of new task types, making it a flexible foundation for a comprehensive grammar practice tool.

## Features

- **Task Generation**: Automatically generate grammar tasks related to direct-to-indirect speech conversion and verb tense usage.
- **Answer Validation**: Validate user-submitted answers with detailed feedback.
- **Explanations**: Provide comprehensive explanations for each task, formatted for easy reading.
- **Interactive Web Interface**: User-friendly interface built with Flask and Jinja2 templating.
- **Dockerized for Deployment**: Easily deploy the application using Docker for a consistent environment.

## Technologies Used

- **Python**: Core programming language used for the backend.
- **Flask**: Web framework used to build the server and handle HTTP requests.
- **Jinja2**: Templating engine used to render HTML pages dynamically.
- **Markdown & BeautifulSoup**: Used for formatting explanations and converting them to HTML.
- **Pydantic**: Used for data validation and ensuring correct data structure.
- **Groq API**: Integration with an LLM (Large Language Model) to generate tasks, validate answers, and provide explanations.
- **Docker**: Containerization tool used for deployment.

## Project Structure

```
├── app.py                      # Main Flask application file
├── llm_interaction.py          # Handles interactions with the LLM via Groq API
├── models.py                   # Pydantic models for data validation
├── task_handler.py             # Logic for task handling and validation
├── templates/                  # HTML templates for rendering pages
│   ├── index.html              # Template for the main index page
│   ├── verb_tense.html         # Template for verb tense exercises
├── Dockerfile                  # Docker configuration file
├── docker-compose.yaml         # Docker Compose configuration
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

## Installation

### Prerequisites

- **Docker**: Ensure you have Docker installed on your machine.
- **Python 3.12+**: If you prefer running locally without Docker.

### Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/mrmidi/groq-english-train.git
   cd groq-english-train
   ```

2. **Set Up Environment Variables**
   Create a `.env` file in the root directory and add your `GROQ_API_KEY`.
   ```bash
   echo "GROQ_API_KEY=your_api_key_here" > .env
   ```

3. **Install Dependencies**
   If running locally:
   ```bash
   pip install -r requirements.txt
   ```

4. **Build and Run the Docker Container**
   ```bash
   docker-compose up --build
   ```
   This will build the Docker image and start the application on port `8001`.

## Usage

1. **Access the Application**
   Once the Docker container is running, open your web browser and go to:
   ```
   http://localhost:8001
   ```

2. **Explore the Features**
   - View and complete grammar tasks.
   - Submit your answers to see if they are correct.
   - Request explanations to understand the concepts better.

## API Endpoints

- **`GET /`**: Load the main page with direct-to-indirect speech tasks.
- **`POST /check/<task_type>`**: Submit a task answer for validation.
- **`GET /explain/<task_type>/<question_text>`**: Get an explanation for a specific task.
- **`GET /fetch_task/<task_type>`**: Fetch a new task of the specified type.
- **`GET /verb_tense`**: Load verb tense tasks.

## Development

### Running Locally

1. **Activate Virtual Environment (Optional)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Run the Flask Application**
   ```bash
   export FLASK_APP=app.py
   flask run --port=8001
   ```

### Running with Docker

1. **Build and Run**
   ```bash
   docker-compose up --build
   ```

2. **Stop the Application**
   ```bash
   docker-compose down
   ```

## Deployment

### Docker Deployment

- The application is set up for deployment using Docker. Ensure that the `GROQ_API_KEY` environment variable is correctly set in the `.env` file before building the Docker image.

### Manual Deployment

1. **Set up a Python environment on the server.**
2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application with a production server like Gunicorn:**
   ```bash
   gunicorn --bind 0.0.0.0:8001 app:app
   ```

## Acknowledgments

- **Flask**: For providing a simple and powerful web framework.
- **Groq**: For the LLM API used to generate, validate, and explain tasks.
- **Markdown & BeautifulSoup**: For easy HTML formatting and manipulation.
- **Pydantic**: For ensuring data consistency and validation.
