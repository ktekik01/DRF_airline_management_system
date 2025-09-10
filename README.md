
# Airline Management System API

This project is a Django REST Framework (Django DRF) backend for managing airplanes, flights, and passenger reservations.


## Design and Implementation Decisions
I organized the codebase into a standard Django project package (airline_management_system/) and a separate apps/ package that contains three domain‑focused apps: airplane, flight, and reservation. Each app encapsulates its own models, serializers, views, URLs, and migrations to keep concerns isolated and make the code easy to navigate, test, and evolve. Endpoints follow REST conventions with plural resource names and clear nested list endpoints (e.g., /airplanes/{id}/flights/, /flights/{id}/reservations/). I chose DRF generic views with explicit URL patterns (instead of routers/ViewSets) to keep the routing fully transparent and interview‑friendly while still leveraging DRF’s request/response pipeline.

Persistence is handled by Django ORM on PostgreSQL. Configuration is 12‑factor: secrets and environment‑specific settings (database, email) are read from .env via django‑environ; we ship a .env.example for reviewers. Database schema is driven by the apps’ migrations (included in the repo); reviewers only need to run python manage.py migrate once to create tables before runserver. Foreign keys use on_delete=CASCADE so deleting an airplane removes its flights (and their reservations via cascading relationships). Separately, when an airplane is deactivated (PATCH status=false), I perform a logical cascade in the view to mark related reservations inactive without deleting data.

Validation is layered appropriately. Model/field constraints (types, max_length, EmailField, uniqueness) provide basic validation, while business rules live in serializers. The Flight serializer enforces arrival_time > departure_time and prevents scheduling conflicts by scanning the airplane’s other flights with a ±1‑hour buffer; it supports partial updates (PATCH) by falling back to the instance’s existing values when fields aren’t provided. The Reservation serializer checks capacity against flight.airplane.capacity before saving; unique, alphanumeric reservation codes are auto‑generated in the model’s save(). Optional filtering on flights (by departure, destination, and date) is exposed via query parameters and reflected in the Postman Collection; I implemented it using django-filter.

Finally, I send confirmation emails on successful reservation creation via Django’s send_mail. Email settings are environment‑driven so development can use the console backend while production can use SMTP (e.g., Gmail with App Passwords). I include a Postman Collection that covers CRUD, nested endpoints, filtering queries, and sample payloads, plus a README with setup and run instructions. This balance of modular structure, explicit endpoints, environment‑based configuration, and serializer‑level business logic keeps the service simple to understand yet robust enough for real‑world usage.



## Features

- **Airplanes**  
  - `GET /api/airplanes/` - List all airplanes  
  - `GET /api/airplanes/{id}/` - Retrieve one airplane  
  - `POST /api/airplanes/` - Create a new airplane  
  - `PATCH /api/airplanes/{id}/` - Update an airplane  
  - `DELETE /api/airplanes/{id}/` - Delete an airplane  
  - `GET /api/airplanes/{id}/flights/` - List flights for an airplane  

- **Flights**  
  - `GET /api/flights/` - List all flights (supports filtering)  
  - `GET /api/flights/{id}/` - Retrieve one flight  
  - `POST /api/flights/` - Create a new flight  
  - `PATCH /api/flights/{id}/` - Update a flight  
  - `DELETE /api/flights/{id}/` - Delete a flight  
  - `GET /api/flights/{id}/reservations/` - List reservations for a flight  

- **Reservations**  
  - `GET /api/reservations/` - List all reservations  
  - `GET /api/reservations/{id}/` - Retrieve one reservation  
  - `POST /api/reservations/` - Create a new reservation (sends confirmation email)  
  - `PATCH /api/reservations/{id}/` - Update a reservation  

## Setup Instructions

1. **Clone the repository** and navigate to the project root (where `manage.py` is).

2. **Create & activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate      # Linux/macOS
   venv\Scripts\activate       # Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:  
   Create a `.env` file in the project root with the following variables:
   ```dotenv
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   EMAIL_USE_TLS=True
   DEFAULT_FROM_EMAIL=your-email@gmail.com
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   DATABASE_URL=postgres://user:password@localhost:5432/mydatabase
   ```
   
   **Important**: Replace the placeholder values with your actual credentials:
   - `EMAIL_HOST_USER`: Your Gmail address
   - `EMAIL_HOST_PASSWORD`: Your Gmail App Password (not regular password)
   - `SECRET_KEY`: Generate a new Django secret key
   - `DATABASE_URL`: Your actual database connection string

5. **Database migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

7. **Test API via Postman Collection**:  
   - Open Postman  
   - **File** → **Import** → Choose `airline_management_system_postman_collection.json`  

## Filtering Flights

You can filter flights by query parameters:

```
GET /api/flights/?departure=Heathrow&destination=Istanbul&departure_date=2025-08-01
GET /api/flights/?departure_date=2025-08-01&arrival_date=2025-08-02
```
