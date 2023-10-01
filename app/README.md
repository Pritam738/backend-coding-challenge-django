# Django REST Framework Project

This is a Django REST framework project that allows users to manage notes.

## Project Description

The project provides a RESTful API for managing notes. Users can create, read, update, and delete their own notes. Additionally, notes can be tagged and marked as public or private.

## Features

- User registration and authentication
- user can Create, read, update, and delete notes
- Search notes by keywords
    - user can search their notes as well as all public notes
- Filter notes by tags
- Mark notes as public or private

## Installation and How to run the code

1. Clone this repository to your local machine:

   ```bash
   git clone <repository-url>
   ```
2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```
3. Install project dependencies:

```bash
pip install -r requirements.txt
```

4. Apply database migrations:

```bash
python manage.py migrate
```

5. Run the development server:
```bash
python manage.py runserver
Access the API at http://localhost:8000/api/.
```
or 

1. Use docker compose 
 
    1. docker-compose build
 
    2. docker-compose run app python manage.py migrate
 
    3. docker-compose up

# API USAGE

## User Registration
To register a new user, make a POST request to the following endpoint:

```
http

POST /api/register/
```
Request Body:

```json
{
    "username": "your_username",
    "password": "your_password"
}
```

## User Login
To log in as a registered user, make a POST request to the following endpoint:

```
http

POST /api/login/
```
Request Body:

```json
{
    "username": "your_username",
    "password": "your_password"
}
```

## Create a Note
To create a new note, make a POST request to the following endpoint:

```
http

POST /api/notes/create/
```

Request Headers:

```
http

Content-Type: application/json
Authorization: Token your_token_here
```
Request Body:

```json
{
    "title": "Your Note Title",
    "body": "This is the content of your note.",
    "tags": "tag1,tag2",
    "is_public": false
}
```

## Get a List of Notes
To retrieve a list of notes, make a GET request to the following endpoint:

```
http

GET /api/notes/
```

Request Headers:

```
http

Authorization: Token your_token_here
```

## Search Notes by Keywords
To search for notes by keywords, make a GET request to the following endpoint:

```
http

GET /api/notes/search/?keywords=your_keywords
```

Request Headers:

```
http

Authorization: Token your_token_here
```

## Filter Notes by Tags
To filter notes by tags, make a GET request to the following endpoint:

```
http

GET /api/notes/?tags=your_tags
```

Request Headers:

```
http

Authorization: Token your_token_here
```

## Get all Notes of a user
To fetch all notes of a user, make a GET request to the following endpoint:

```
http

GET /api/notes/
```

Request Headers:

```
http

Authorization: Token your_token_here
```


## Update a Note
To update an existing note, make a PUT request to the following endpoint:

```
http
PUT /api/notes/detail/<note_id>/
```

Request Headers:

```
http

Content-Type: application/json
Authorization: Token your_token_here
```

Request Body:

```json
{
    "title": "Updated Note Title",
    "body": "This is the updated content of your note.",
    "tags": "tag3,tag4",
    "is_public": true
}
```
## Delete a Note
To delete an existing note, make a DELETE request to the following endpoint:

```
http

DELETE /api/notes/detail/<note_id>/
```
Request Headers:

```
http

Authorization: Token your_token_here
```
# Logging

The project uses logging to capture important events. Logs are available in the server logs and can be configured according to your needs.

# Test cases

To run the test cases ypu can use django test cmd 

```
    python manage.py test 
```

or if you are useing docker-compose 

```
    docker-compose run app python manage.py test
```