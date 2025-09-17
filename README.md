# Smart Parking Backend API System

## Project Overview
This project is a robust backend API system for a smart parking solution, built to manage parking slots, user reservations, and authentication. It is a scaled-down, functional prototype of a real-world system, demonstrating key skills in backend development, database management, and API security.

This project was built with a focus on core features relevant to the urban mobility and car ownership domain, with a particular emphasis on addressing real-world challenges like concurrency in reservations and secure user authentication.

---

## 🚀 Key Features
- **User Authentication:** Secure user registration and login using JWT (JSON Web Tokens) with Supabase's authentication service.  
- **Parking Slot Management:** A RESTful API to retrieve a list of all available parking slots.  
- **Secure Reservation System:** A protected endpoint that allows an authenticated user to reserve a parking slot. The logic handles availability checks to prevent double-booking.  
- **User-Specific Reservations:** A protected API to retrieve all reservations made by the authenticated user.  
- **Cloud-Based Database:** Uses Supabase for a scalable and reliable PostgreSQL backend.  

---

## 🛠️ Technologies Used
- Backend: Python 3.11+  
- Web Framework: FastAPI  
- Database: Supabase (PostgreSQL)  
- Authentication: JWT (JSON Web Tokens)  
- Dependency Management: pip  
- Environment Variables: python-dotenv  

---

## 🧱 System Architecture
The system follows a standard client-server architecture. The FastAPI backend acts as a microservice, handling all business logic and API routing. It communicates with the Supabase backend, which serves as a centralized database and authentication provider.

---

## ⚙️ Setup and Installation

1. Clone the repository:  
`git clone https://github.com/<your-username>/<your-repository-name>.git`  
`cd <your-repository-name>`

2. Create a virtual environment and activate it:  
`python -m venv env`  
On Windows: `.\env\Scripts\activate`  
On macOS/Linux: `source env/bin/activate`

3. Install the required packages:  
`pip install fastapi uvicorn supabase python-dotenv pyjwt`  

Alternatively, create a `requirements.txt` with:  
fastapi
uvicorn
supabase
python-dotenv
pyjwt
and install via: `pip install -r requirements.txt`

4. Configure environment variables by creating a `.env` file in the root of the project:  SUPABASE_URL=YOUR_SUPABASE_URL
 SUPABASE_ANON_KEY=YOUR_SUPABASE_ANON_KEY
 SECRET_KEY=a_strong_secret_key_for_jwt_signing

5. Run the server:  
`uvicorn app.main:app --reload`  
The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## 📌 API Endpoints
The API is fully documented using Swagger UI at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

| Method | Endpoint | Description | Authentication Required |
|--------|----------|------------|------------------------|
| POST   | /register | Registers a new user. | No |
| POST   | /login | Authenticates a user and returns a JWT token. | No |
| GET    | /parking/slots | Retrieves all available parking slots. | No |
| POST   | /parking/reserve | Reserves an available parking slot. | Yes |
| GET    | /parking/my-reservations | Retrieves all reservations for the authenticated user. | Yes |
| POST   | /parking/slots | Creates a new parking slot (for admin use). | Yes |

---

## 🚀 Future Enhancements
- Check-out and Payments: Implement a `/check-out` endpoint to calculate final fees and free up the parking slot.  
- Email Notifications: Integrate a service to send email notifications for reservation confirmations.  
- Admin Dashboard: Create endpoints for an admin to manage all parking slots and user reservations.  
- Containerization: Use Docker to containerize the application for easier deployment.  
- Cloud Deployment: Deploy the API to a cloud platform like Render, Heroku, or AWS.


