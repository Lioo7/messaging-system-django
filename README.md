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
- **Update Message**: Authenticated users who are the senders can modify existing messages.
- **Partial Update Message**: Authenticated users who are the senders can partially update existing messages.
- **Delete Message**: Authenticated users who are the senders or the receivers can remove messages they've sent or received.
- **User Registration**: Unauthenticated users can register new accounts via the "/api/v1/users/register/" endpoint.


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
   - Additional users can be created via the "/api/v1/accounts/register/" endpoint.

4. **Logging**:
   - This project includes a logging system to track important events and messages during runtime. Logging configurations are defined in the   `settings.py` file, allowing developers to customize logging levels and output formats as needed. By default, logs are stored in the `logs/` directory.


## Postman Collection

Explore the Postman collections provided in the project repository to test the API. They encompass examples for all API endpoints, differentiated for development and production environments.

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

## Entity-Relationship Diagram (ERD)
This ERD illustrates the relationship between the "Message" and "User" models within the Messaging System API.

![ERD Diagram](https://i.ibb.co/gSBJFNh/messaging-app-erd.png)
