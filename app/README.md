# Django REST Framework Project

This is a Django REST framework project that allows users to manage notes.

## Project Description

The project provides a RESTful API for managing notes. Users can create, read, update, and delete their own notes. Additionally, notes can be tagged and marked as public or private.

## Features

- User registration and authentication.
- User can Create, update, and delete their own notes.
- Notes can be public or private.
- users can read their own and all public notes.
- Search notes by keywords.
    - User can search their notes as well as all public notes.
- Filter notes by tags.
    - User can access all their notes as well as public notes.

## Installation and How to run the code

1. Clone this repository to your local machine:

   ```bash
   git clone <repository-url>
   ```
2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
cd app
```

3. Use docker compose 
 
```bash
    docker-compose build
    docker-compose run app python manage.py migrate
    docker-compose up
```

# API USAGE

## User Registration
To register a new user, make a POST request to the following endpoint:

```
POST /api/register/
```
Request Body:

```json
{
    "username": "your_username",
    "password": "your_password"
}
```

```
curl --location --request POST 'http://localhost:8000/api/register/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "test",
    "password": "password"
}'
```

Response Body
```
{
    "message": "User created successfully.",
    "token": "ccadf65f8a64f2722a1d84581c7e219459856734"
}
```

## User Login
To log in as a registered user, make a POST request to the following endpoint:

```
POST /api/login/
```
Request Body:

```json
{
    "username": "your_username",
    "password": "your_password"
}
```

```
curl --location --request POST 'http://localhost:8000/api/login/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "test", //"test_user1",
    "password": "password"
}'
```

Response Body

```
{
    "token": "ccadf65f8a64f2722a1d84581c7e219459856734"
}
```
Note: this token is used for authorization in below apis

## Create a Note
To create a new note, make a POST request to the following endpoint:

```
POST /api/notes/create/
```

Request Headers:

```
Content-Type: application/json
Authorization: Token < your_token_here >
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

```
curl --location --request POST 'http://localhost:8000/api/notes/create/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Token edbc23c6ed8399c8e2e5410b34498fdc9e66607a' \
--data-raw '{
    "title": "Your Note Title",
    "body": "This is the content of your note.",
    "tags": "tag1,tag2",
    "is_public": false
}'
```

Response Body

```
{
    "id": 1,
    "title": "Your Note Title",
    "body": "This is the content of your note.",
    "tags": "tag1,tag2",
    "is_public": false
}
```

## List Notes by id
To retrieve a note by id, make a GET request to the following endpoint:

```
GET /api/notes/< id >/
```

Request Headers:

```
Authorization: Token < your_token_here >
```
Note:  Authorization token is optional here; if you dont pass the token, you will only be able to access public     notes. With a valid user token you will be able to access all users notes and all public notes.

```
curl --location --request GET 'http://localhost:8000/api/notes/1/' \
--header 'Authorization: Token edbc23c6ed8399c8e2e5410b34498fdc9e66607a' \
```

Response Body

```
{
    "id": 1,
    "title": "Your Note Title",
    "body": "This is the content of your note.",
    "tags": "tag1,tag2",
    "is_public": false
}
```  
## Search Notes by Keywords
To search for notes by keywords, make a GET request to the following endpoint:

```
GET /api/notes/search/?keywords=your_keywords
```

Request Headers:

```
Authorization: Token < your_token_here >
```

```
curl --location --request GET 'http://localhost:8000/api/notes/search/?keywords=note' \
--header 'Authorization: Token edbc23c6ed8399c8e2e5410b34498fdc9e66607a' \
```

Response Body

```
[{
    "id": 1,
    "title": "Your Note Title",
    "body": "This is the content of your note.",
    "tags": "tag1,tag2",
    "is_public": false
},
...
]
```  

## Filter Notes by Tags
To filter notes by tags, make a GET request to the following endpoint:

```
GET /api/notes/?tags=your_tags
```

Request Headers:

```
Authorization: Token < your_token_here >
```

```
curl --location --request GET 'http://localhost:8000/api/notes/list/?tags=tag3,tag4' \
--header 'Authorization: Token edbc23c6ed8399c8e2e5410b34498fdc9e66607a' \
```

Response Body

```
{
    "id": 1,
    "title": "Your Note Title",
    "body": "This is the content of your note.",
    "tags": "tag3,tag4",
    "is_public": false
}
```  

## Get all Notes of a user
To fetch all notes of a user, make a GET request to the following endpoint:

```
GET /api/notes/
```

Request Headers:

```
Authorization: Token < your_token_here >
```

```
curl --location --request GET 'http://localhost:8000/api/notes/list/' \
--header 'Authorization: Token edbc23c6ed8399c8e2e5410b34498fdc9e66607a' \
```

Response Body

```
[
    {
        "id": 1,
        "title": "Updated Note Title",
        "body": "This is the updated content of your note.",
        "tags": "tag3,tag4",
        "is_public": false
    },
    {
        "id": 3,
        "title": "Updated Note Title",
        "body": "This is the updated content of your note.",
        "tags": "tag3,tag4",
        "is_public": true
    },
    {
        "id": 4,
        "title": "Updated Note Title",
        "body": "This is the updated content of your note.",
        "tags": "tag3,tag4",
        "is_public": true
    },
    {
        "id": 5,
        "title": "Updated Note Title",
        "body": "This is the updated content of your note.",
        "tags": "tag3,tag4",
        "is_public": true
    },
    {
        "id": 6,
        "title": "Updated Note Title",
        "body": "This is the updated content of your note.",
        "tags": "tag3,tag4",
        "is_public": true
    },
    {
        "id": 7,
        "title": "Updated Note Title",
        "body": "This is the updated content of your note.",
        "tags": "tag3,tag4",
        "is_public": true
    }
]
```

## Update a Note
To update an existing note, make a PUT request to the following endpoint:

```
PUT /api/notes/detail/<note_id>/
```

Request Headers:

```
Content-Type: application/json
Authorization: Token < your_token_here >
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

```
curl --location --request PUT 'http://localhost:8000/api/notes/detail/1/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Token edbc23c6ed8399c8e2e5410b34498fdc9e66607a' \
--data-raw '{
    "title": "Updated Note Title",
    "body": "This is the updated content of your note.",
    "tags": "tag3,tag4",
    "is_public": false
}'
```
Response Body

```
{
    "id": 1,
    "title": "Updated Note Title",
    "body": "This is the updated content of your note.",
    "tags": "tag3,tag4",
    "is_public": false
}
```  

## Delete a Note
To delete an existing note, make a DELETE request to the following endpoint:

```
DELETE /api/notes/detail/<note_id>/
```
Request Headers:

```
Authorization: Token < your_token_here >
```

```
curl --location --request DELETE 'http://localhost:8000/api/notes/detail/3/' \
--header 'Authorization: Token ccadf65f8a64f2722a1d84581c7e219459856734' \
```
# Http Response Code

200: success
204: resource deleted
400: bad request (issue with input params)
401: unauthorized access (issue with access token)
403: you dont have permission for the operation
404: endpoint not available 
500: internal server error

# Logging

The project uses logging to capture important events. Logs are available in the server logs and can be configured according to your needs.

# Test cases

To run the test cases using docker-compose 

```
    docker-compose run app python manage.py test
```
# Scope for improvement 

1. Use pagination in the search, filter and get all notes api's to increasing handle load.
2. Implement api caching, so for the same api request we dont query the DB again and again; help in load management.