project name: real time multi agent chat system

app name: chat

project description:

## backend

1. user can registration and login.

2. visitor and agent can chat with each other.

3. visitor and agent both can see chat history.

project features:

I have dockerize python(django) application for this project and installed the required packages, which i have shared in requirements.txt file.

I have used Django Rest Framework for creating the API's.

I have used Postgresql database for this project.

I have used Django ORM for database operations.

I have used Django Admin for creating the admin panel.

I have used Django Serializer for creating the serializers.

I have used JWT for creating the token based authentication.

I have used Postman for testing the API's.

installation and execution instructions:

1.Clone the project from the git repository. Even you can download the zip file from the git repository.

git clone https://github.com/sazzadhossain881/Real-Time-Multi-Agent-Chat-System.git

Run the following commands:

1. docker build .

2. docker-compose build

3. docker-compose run --rm app sh -c "python manage.py makemigrations"

4. docker-compose run --rm app sh -c "python manage.py migrate"

5. docker-compose run --rm app sh -c "python manage.py createsuperuser"

6. docker-compose up

API usage examples:

Now, you have to authenticate yourself before doing any operation. To do that hit the login endpoint and pass the username and password in the body. You will get a token in the response. Copy token and paste it in the Headers section in Postman (Authorization: Bearer <your_token>). Now, you can perform any operation.:

url: http://127.0.0.1:8000/api/users/register/

Request Body: 

{
    "username":"",
    "first_name":"",
    "last_name":"",
    "email":"",
    "role":"" (visitor/agent),
    "password":""
}

Response:

{
    "username": "",
    "first_name": "",
    "last_name": "",
    "email": "",
    "role": "",
    "token": ""
}

url: http://127.0.0.1:8000/api/users/login/

Request Body: 

{
    "username": "",
    "password": ""
}

Response:

{
    "username": "",
    "first_name": "",
    "last_name": "",
    "email": "",
    "role": "",
    "token": ""
}

To see visitor or agent own conversations:

url: http://127.0.0.1:8000/api/chat/my-message/

To see visitor or agent specific conversations:

http://127.0.0.1:8000/api/chat/my-message/<session_id>/

You can also see the admin dashboard using the following url:

url: http://127.0.0.1:8000/admin/

Websocket Configuration:

url: https://websocketking.com/

ws://localhost:8000/ws/chat/?token=<your_token>

Body:

{
"message":"Hello from visitor"
}

Database Schema:

This implementation has 3 main models: User, ChatSession, Message

User stores information username, first_name, last_name, email, role, password, is_available

ChatSession stores information agent, visitor, is_active

Message stores information session, sender, content


Future improvements:

1. File upload feature
2. Typing indicator


