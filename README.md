# To-Do List API

A To-Do List app built with FastAPI and SQLite, with a React frontend.

## Prerequisites

- Python 3.10+
- Node.js 18+

## Running the Application

### Clone the repository and navigate to the project folder:

git clone https://github.com/yourusername/To-Do-List-API.git
cd To-Do-List-API

### Create and activate a virtual environment:

python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

### Install backend dependencies:

pip install -r requirements.txt

### Create a .env file in the project root with the following:

SECRET_KEY=anyrandomstringyouwant

### Start the backend server:

uvicorn main:app --reload

### Navigate to the frontend folder, install dependencies and start the app:

cd frontend
npm install
npm run dev

The app will be running at http://localhost:5173
## Using the API Standalone

The API can also be used standalone without the frontend. Navigate to http://localhost:8000/docs to access the Swagger UI and interact with the endpoints directly:

<img width="1919" height="1030" alt="image" src="https://github.com/user-attachments/assets/8e00bc9f-500a-4b62-b4ee-b8d8f6ef38b9" />

### Before making any requests to protected endpoints, you need to register a user and get a token.

1. Register a new user by posting to `/register`:

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "yourpassword"
}

2. Login with the same credentials at `/login` to get your token:

{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}

3. Click the Authorize button in Swagger UI and enter your token to make authenticated requests to the todo endpoints.

## Features

- User registration and login with JWT authentication
- Password hashing
- Full CRUD for to-do items
- Paginated item listing
- Protected routes
