# Task Management API

## Overview
This is a Django REST framework-based Task Management API that allows user registration, authentication, task management, and user retrieval. It includes token-based authentication, rate limiting, and an AWS Lambda simulation for task completion notifications.

## Setup Instructions

### Prerequisites
- Python 3.x
- Django 3.x or later
- Django REST Framework
- PostgreSQL or SQLite (default)

### Installation

1. Clone the repository:
   ```sh
   git clone git@github.com:rahulg0/task-management.git
   cd task-management
   ```

2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```sh
   python manage.py migrate
   ```

5. Create a superuser:
   ```sh
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```sh
   python manage.py runserver
   ```

## API Endpoints

### Authentication

#### Register a new user
```http
POST /api/register/
```
**Request Body:**
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "securepassword"
}
```
**Response:**
```json
{
  "message": "Successfully created user.",
  "token": "<authentication_token>"
}
```

#### Login
```http
POST /api/login/
```
**Request Body:**
```json
{
  "email": "test@example.com",
  "password": "securepassword"
}
```
**Response:**
```json
{
  "token": "<authentication_token>",
  "id": 1
}
```

### Users

#### Get All Users (Admin Only)
```http
GET /api/get-users/
```
**Headers:**
```sh
Authorization: Token <authentication_token>
```
**Response:**
```json
{
  "users": [
    {
      "id": 1,
      "username": "testuser",
      "email": "test@example.com"
    }
  ]
}
```

### Tasks

#### Get Tasks
```http
GET /api/tasks/?status=
```
**Headers:**
```sh
Authorization: Token <authentication_token>
```
**Response:**
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Task 1",
      "status": "pending",
      "assigned_to": 1
    }
  ]
}
```

#### Create Task (Admin Only)
```http
POST /api/tasks/
```
**Headers:**
```sh
Authorization: Token <authentication_token>
```
**Request Body:**
```json
{
  "title": "New Task",
  "description": "Task description",
  "assigned_to": 2
}
```
**Response:**
```json
{
  "message": "Successfully created task: New Task"
}
```

#### Update Task
```http
PUT /api/tasks/{task_id}/
```
**Headers:**
```sh
Authorization: Token <authentication_token>
```
**Request Body:**
```json
{
  "status": "completed"
}
```
**Response:**
```json
{
  "message": "Successfully updated task: New Task"
}
```

#### Delete Task (Admin Only)
```http
DELETE /api/tasks/{task_id}/
```
**Headers:**
```sh
Authorization: Token <authentication_token>
```
**Response:**
```json
{
  "message": "Task deleted successfully"
}
```

## Design Choices


### 1. Django Rest Framework (DRF) with Token Authentication
- Provides a structured and scalable approach for API development.
- Token-based authentication ensures secure access.

### 2. Class-Based Views (CBVs) with APIView
- Enhances maintainability and code reuse.
- Simplifies handling different HTTP methods.

### 3. Permissions & Authentication
- `permissions.IsAuthenticated` ensures only authorized users can access certain endpoints.
- `permissions.AllowAny` allows open access for login and registration.
- `TokenAuthentication` secures API requests.

### 4. Task Management Logic
- Superusers can create, assign, and delete tasks.
- Regular users can only update the status of their assigned tasks.
- Query parameters allow task filtering by status.

### 5. Rate Limiting (Throttling)
- `UserRateThrottle` prevents API abuse.
- Unit tests validate throttling behavior.

### 6. Database Indexing for Performance
- `status` and `assigned_to` fields in `Task` model have `db_index=True`.
- Improves filtering and lookup speed.

### 7. AWS Lambda Simulation for Task Completion
- Optional feature to simulate a Lambda function call when a task is completed.
- Useful for event-driven processing.

### 8. User Management & Superuser Privileges
- Users are uniquely identified via email.
- Only superusers can manage tasks and user data.


## Running Unit Tests

To run tests for tasks throttling, execute:
```sh
python manage.py test
```

## Conclusion
This API balances **security, scalability, and maintainability**, making it efficient for managing tasks with proper access control.