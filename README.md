# Messaging System API

<p align="center">
  <img src="https://img.shields.io/badge/Django-092E20?style=flat&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/Django%20REST%20Framework-092E20?style=flat&logo=django&logoColor=white" alt="Django REST Framework">
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/JSON%20Web%20Tokens-000000?style=flat&logo=jsonwebtokens&logoColor=white" alt="JSON Web Tokens">
</p>

This Django REST API facilitates a messaging system, enabling users to send, receive, read, and delete messages.

## Website Link

Visit the website to explore the Messaging System API: [Messaging System API](http://54.235.55.114:8000/)

## Features

- **Write Message**: Authenticated users can compose and send messages to other users.
- **Get All Messages**: Authenticated users can retrieve a comprehensive list of all messages they've sent or received.
- **Get Unread Messages**: Authenticated users can obtain a list of unread messages they've received.
- **Read Message**: Authenticated users can mark a message as read and access its details.
- **Delete Message**: Authenticated users can remove messages they've sent or received.
- **Authentication**: The API leverages JWT (JSON Web Tokens) for authentication, ensuring that only authenticated users can execute actions.

## Technologies Used

- **Django**: A high-level Python web framework for developing web applications.
- **Django REST Framework**: A versatile toolkit for building Web APIs.
- **Docker**: A platform for developing, shipping, and running applications in containers.
- **JWT (JSON Web Tokens)**: An authentication standard used to secure the API.
- **Python**: The programming language used for development.

## Getting Started (Development Environment)

1. **Setting up the Development Environment**:
   - Install Docker on your machine.
   - Clone this repository.
   - Navigate to the project directory.
   - Create a `.env` file in the project root directory and add the following lines to it:
     ```
     SECRET_KEY="your_secret_key"
     DJANGO_SUPERUSER_USERNAME="your_django_superuser_username"
     DJANGO_SUPERUSER_EMAIL="your_django_superuser_email"
     DJANGO_SUPERUSER_PASSWORD="your_django_superuser_password"
     ```
   
2. **Running the Application with Docker**:
   - Build the Docker image: `docker-compose build`.
   - Start the Docker containers: `docker-compose up -d`.
   - Access the API at `http://localhost:8000/`.

3. **Creating Super User and Other Users**:
   - A superuser (admin) will be created automatically during Docker container startup using the credentials provided in the `.env` file.
   - Additional users can be created programmatically through Django's shell or management commands.


## Postman Collection

Explore the Postman collection provided in the project repository to test the API. It encompasses examples for all API endpoints.

The API relies on JWT (JSON Web Tokens) for authentication. Upon logging in, users receive an access token and a refresh token. The access token authenticates requests. Include the access token in the `Authorization` header of your requests as follows:
```
Authorization: Bearer <access_token>
```

## Tests
The test suite includes comprehensive coverage of the API endpoints and scenarios to ensure robustness and reliability.

Run the following command to execute the tests:
```
python manage.py test
```
