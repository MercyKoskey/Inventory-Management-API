# Inventory Management API

A RESTful API built with Django and Django REST Framework (DRF) for **authentication, user management, inventory categories, items, and reports**.  

## Project Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/MercyKoskey/Inventory-Management-API.git
   cd Inventory-Management-API
   ```

2. **Create and Activate Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create Superuser (for Admin access)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the Server**
   ```bash
   python manage.py runserver
   ```

Server runs at:  
 `http://127.0.0.1:8000/`  



## Authentication

### 1. Signup  
**Endpoint:**  
`POST /api/signup/`

**Headers:**
```json
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "john@example.com",
  "username": "johnny",
  "password": "Password123!"
}
```

**Response (201 Created):**
```json
{ "message": "User created successfully" }
```



### 2. Login  
**Endpoint:**  
`POST /api/login/`

**Headers:**
```json
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "Password123!"
}
```

**Response (200 OK):**
```json
{
  "refresh": "jwt-refresh-token",
  "access": "jwt-access-token"
}
```

Use this header for all authenticated requests:  
```
Authorization: Bearer <access>
```



## Users CRUD

- **Admin:**
  - `GET /api/users/` → List users
  - `POST /api/users/` → Create user
  - `PUT/PATCH/DELETE /api/users/{id}/` → Manage users  

- **Regular User:**
  - `GET /api/users/{id}/` → Get own profile
  - `PUT/PATCH/DELETE /api/users/{id}/` → Update/Delete own profile  

**Request Body Example (Create User):**
```json
{
  "email": "mary@example.com",
  "username": "mary",
  "password": "StrongPass99"
}
```



## Categories

**Create Category**  
`POST /api/inventory/categories/`

**Headers:**
```
Authorization: Bearer <access>
```

**Body:**
```json
{ "name": "Electronics" }
```
**Get Categories**  
`GET /api/inventory/categories/`

**Headers:**
```
Authorization: Bearer <access>
```


## Items CRUD + Filters

### Create Item
`POST /api/inventory/items/`

**Body:**
```json
{
  "name": "Laptop",
  "description": "Dell XPS 15",
  "quantity": 10,
  "price": 1500.00,
  "category": 1
}
```

### Get Items (with filters, search, ordering, pagination)
`GET /api/inventory/items/?category=1&min_price=100&max_price=2000&low_stock=true&threshold=5&search=laptop&ordering=-price&page=1`

### Update Item
`PATCH /api/inventory/items/1/`

**Body:**
```json
{ "quantity": 15 }
```



## Inventory Levels

`GET /api/inventory/items/levels/`

**Response Example:**
```json
[
  { "id": 1, "name": "Laptop", "quantity": 15 },
  { "id": 2, "name": "Rice", "quantity": 50 }
]
```



## Inventory Changes

### Item History
`GET /api/inventory/items/1/changes/`

**Response Example:**
```json
[
  {
    "id": 1,
    "item": "Laptop",
    "change_type": "restock",
    "quantity_changed": 5,
    "changed_by": "johnny",
    "timestamp": "2025-08-29T12:34:56Z"
  }
]
```

### All Changes
`GET /api/inventory/changes/`



## Reports

`GET /api/inventory/reports/`



**Note:**:  
- Authentication is handled via **JWT**.  
- Admins have **full user management** privileges.  
- Regular users can only manage their **own account and view/update their own data**.  
- Pagination available for items endpoint via `?page={pageNumber}`.  
