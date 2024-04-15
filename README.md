# Messaging System API

<p align="center">
  <img src="https://img.shields.io/badge/Django-092E20?style=flat&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/Django%20REST%20Framework-092E20?style=flat&logo=django&logoColor=white" alt="Django REST Framework">
  <img src="https://img.shields.io/badge/AWS%20EC2-232F3E?style=flat&logo=amazonaws&logoColor=white" alt="AWS EC2">
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white" alt="Python">
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
- **JWT (JSON Web Tokens)**: An authentication standard used to secure the API.
- **AWS EC2**: The API is hosted on an Amazon EC2 instance.
- **Python**: The programming language used for development.

## Getting Started

1. **Setting up the Development Environment**:
   - Install Python.
   - Create and activate a virtual environment.
   - Install the required dependencies: `pip install -r requirements.txt`.

2. **Running the Development Server**:
   - Apply database migrations: `python manage.py migrate`.
   - Start the development server: `python manage.py runserver`.

3. **Creating Super User and Other Users**:
   - To create a superuser (admin) for accessing the Django admin interface and performing administrative tasks:
     ```
     python manage.py createsuperuser
     ```
   - To create additional users, you can either use the Django admin interface or create users programmatically through Django's shell or management commands.

## Postman Collection

Explore the Postman collection provided in the project repository to test the API. It encompasses examples for all API endpoints.

The API relies on JWT (JSON Web Tokens) for authentication. Upon logging in, users receive an access token and a refresh token. The access token authenticates requests. Include the access token in the `Authorization` header of your requests as follows:
```
Authorization: Bearer <access_token>
```
