# Travel Map - Backend API Documentation

## Overview

This is the backend API documentation for the Travel Map application. The backend is built with Django and SQLite, providing CRUD (Create, Read, Update, Delete) operations for locations and photos.

**Developer**: Member 2 (Backend & Database)
**Tech Stack**: Python + Django + SQLite

---

## Base Information

### Server URL
```
Development: http://127.0.0.1:8000
```

### Data Format
- All requests and responses use **JSON** format (except file uploads)
- File uploads use `multipart/form-data` format
- Character encoding: UTF-8

### HTTP Status Codes
| Status Code | Meaning |
|---|---|
| 200 | Success (GET, PUT, DELETE) |
| 201 | Created successfully (POST) |
| 404 | Resource not found |
| 400 | Bad request (invalid parameters) |

---

## Data Models

### Location (地点)
| Field | Type | Description | Required |
|---|---|---|---|
| id | Integer | Unique identifier (auto-generated) | Auto |
| name | String | Name of the place | Yes |
| country | String | Country | Yes |
| city | String | City | Yes |
| latitude | Float | Latitude coordinate | Yes |
| longitude | Float | Longitude coordinate | Yes |
| visit_date | Date | Date of visit (YYYY-MM-DD) | No |
| notes | String | Personal notes / description | No |
| created_at | DateTime | Creation timestamp (auto-generated) | Auto |
| updated_at | DateTime | Last update timestamp (auto-generated) | Auto |
| photos | Array | List of photos for this location | Auto |

### Photo (照片)
| Field | Type | Description | Required |
|---|---|---|---|
| id | Integer | Unique identifier (auto-generated) | Auto |
| location | Integer | ID of the location this photo belongs to | Yes |
| image | File | Image file | Yes |
| description | String | Photo description | No |
| uploaded_at | DateTime | Upload timestamp (auto-generated) | Auto |

---

## API Endpoints

---

### 1. Get All Locations (获取所有地点)

Retrieve a list of all saved locations.

**URL**: `/api/locations/`

**Method**: `GET`

**Parameters**: None

**Response Example**:
```json
{
  "locations": [
    {
      "id": 1,
      "name": "Eiffel Tower",
      "country": "France",
      "city": "Paris",
      "latitude": 48.8584,
      "longitude": 2.2945,
      "visit_date": "2024-06-15",
      "notes": "Beautiful tower with amazing view",
      "photos": [
        {
          "id": 1,
          "image": "/media/location_photos/photo.jpg",
          "description": "Sunset view"
        }
      ]
    },
    {
      "id": 2,
      "name": "Petronas Towers",
      "country": "Malaysia",
      "city": "Kuala Lumpur",
      "latitude": 3.1579,
      "longitude": 101.7116,
      "visit_date": "2025-01-01",
      "notes": "Iconic twin towers",
      "photos": []
    }
  ]
}
```

---

### 2. Create New Location (创建新地点)

Create a new visited location.

**URL**: `/api/locations/`

**Method**: `POST`

**Content-Type**: `application/json`

**Request Body**:
| Field | Type | Required | Description |
|---|---|---|---|
| name | String | Yes | Name of the place |
| country | String | Yes | Country |
| city | String | Yes | City |
| latitude | Float | Yes | Latitude coordinate |
| longitude | Float | Yes | Longitude coordinate |
| visit_date | String | No | Date of visit (YYYY-MM-DD) |
| notes | String | No | Personal notes |

**Request Example**:
```json
{
  "name": "Eiffel Tower",
  "country": "France",
  "city": "Paris",
  "latitude": 48.8584,
  "longitude": 2.2945,
  "visit_date": "2024-06-15",
  "notes": "Beautiful tower with amazing view"
}
```

**Response Example** (Status: 201 Created):
```json
{
  "message": "Created successfully",
  "location": {
    "id": 3,
    "name": "Eiffel Tower",
    "country": "France",
    "city": "Paris",
    "latitude": 48.8584,
    "longitude": 2.2945,
    "visit_date": "2024-06-15",
    "notes": "Beautiful tower with amazing view",
    "photos": []
  }
}
```

---

### 3. Get Single Location Detail (获取单个地点详情)

Retrieve detailed information for a specific location by ID.

**URL**: `/api/locations/{location_id}/`

**Method**: `GET`

**URL Parameters**:
| Parameter | Type | Description |
|---|---|---|
| location_id | Integer | ID of the location |

**Response Example** (Status: 200 OK):
```json
{
  "location": {
    "id": 1,
    "name": "Eiffel Tower",
    "country": "France",
    "city": "Paris",
    "latitude": 48.8584,
    "longitude": 2.2945,
    "visit_date": "2024-06-15",
    "notes": "Beautiful tower with amazing view",
    "photos": [
      {
        "id": 1,
        "image": "/media/location_photos/photo.jpg",
        "description": "Sunset view"
      }
    ]
  }
}
```

**Error Response** (Status: 404 Not Found):
```json
{
  "error": "Location not found"
}
```

---

### 4. Update Location (更新地点)

Update information for an existing location. Only fields provided in the request will be updated.

**URL**: `/api/locations/{location_id}/`

**Method**: `PUT`

**Content-Type**: `application/json`

**URL Parameters**:
| Parameter | Type | Description |
|---|---|---|
| location_id | Integer | ID of the location |

**Request Body** (all fields optional):
| Field | Type | Description |
|---|---|---|
| name | String | Name of the place |
| country | String | Country |
| city | String | City |
| latitude | Float | Latitude coordinate |
| longitude | Float | Longitude coordinate |
| visit_date | String | Date of visit (YYYY-MM-DD) |
| notes | String | Personal notes |

**Request Example**:
```json
{
  "notes": "Updated notes: amazing view at night"
}
```

**Response Example** (Status: 200 OK):
```json
{
  "message": "Updated successfully",
  "location": {
    "id": 1,
    "name": "Eiffel Tower",
    "country": "France",
    "city": "Paris",
    "latitude": 48.8584,
    "longitude": 2.2945,
    "visit_date": "2024-06-15",
    "notes": "Updated notes: amazing view at night",
    "photos": []
  }
}
```

---

### 5. Delete Location (删除地点)

Delete a location and all its associated photos.

**URL**: `/api/locations/{location_id}/`

**Method**: `DELETE`

**URL Parameters**:
| Parameter | Type | Description |
|---|---|---|
| location_id | Integer | ID of the location |

**Response Example** (Status: 200 OK):
```json
{
  "message": "Deleted successfully"
}
```

**Note**: When a location is deleted, all photos belonging to that location are also automatically deleted (cascade delete).

---

### 6. Get All Photos for a Location (获取地点的所有照片)

Retrieve all photos associated with a specific location.

**URL**: `/api/locations/{location_id}/photos/`

**Method**: `GET`

**URL Parameters**:
| Parameter | Type | Description |
|---|---|---|
| location_id | Integer | ID of the location |

**Response Example** (Status: 200 OK):
```json
{
  "photos": [
    {
      "id": 1,
      "image": "/media/location_photos/photo1.jpg",
      "description": "Sunset view"
    },
    {
      "id": 2,
      "image": "/media/location_photos/photo2.jpg",
      "description": "Night view with lights"
    }
  ]
}
```

---

### 7. Upload Photo (上传照片)

Upload a new photo for a specific location.

**URL**: `/api/locations/{location_id}/photos/`

**Method**: `POST`

**Content-Type**: `multipart/form-data` (NOT JSON)

**URL Parameters**:
| Parameter | Type | Description |
|---|---|---|
| location_id | Integer | ID of the location |

**Form Data**:
| Field | Type | Required | Description |
|---|---|---|---|
| image | File | Yes | Image file (JPG, PNG, etc.) |
| description | String | No | Photo description |

**Request Example** (using JavaScript fetch):
```javascript
const formData = new FormData();
formData.append('image', fileInput.files[0]);
formData.append('description', 'Sunset view');

fetch('http://127.0.0.1:8000/api/locations/1/photos/', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

**Response Example** (Status: 201 Created):
```json
{
  "message": "Photo uploaded successfully",
  "photo": {
    "id": 3,
    "image": "/media/location_photos/uploaded_photo.jpg",
    "description": "Sunset view"
  }
}
```

---

### 8. Delete Photo (删除照片)

Delete a specific photo from a location.

**URL**: `/api/locations/{location_id}/photos/{photo_id}/`

**Method**: `DELETE`

**URL Parameters**:
| Parameter | Type | Description |
|---|---|---|
| location_id | Integer | ID of the location |
| photo_id | Integer | ID of the photo |

**Response Example** (Status: 200 OK):
```json
{
  "message": "Photo deleted successfully"
}
```

---

## Error Handling

### Common Error Responses

**404 Not Found** - Resource does not exist:
```json
{
  "error": "Location not found"
}
```

**400 Bad Request** - Invalid request parameters:
```json
{
  "error": "Invalid data provided"
}
```

---

## Quick Reference Summary

| # | Operation | Method | URL |
|---|---|---|---|
| 1 | Get all locations | GET | `/api/locations/` |
| 2 | Create location | POST | `/api/locations/` |
| 3 | Get location detail | GET | `/api/locations/{id}/` |
| 4 | Update location | PUT | `/api/locations/{id}/` |
| 5 | Delete location | DELETE | `/api/locations/{id}/` |
| 6 | Get location photos | GET | `/api/locations/{id}/photos/` |
| 7 | Upload photo | POST | `/api/locations/{id}/photos/` |
| 8 | Delete photo | DELETE | `/api/locations/{id}/photos/{photo_id}/` |

---

## Setup Instructions

### How to Run the Backend Server

```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install django pillow

# Run database migrations
python manage.py migrate

# Create admin user (optional)
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### Access Points
- API Base URL: http://127.0.0.1:8000/api/
- Admin Panel: http://127.0.0.1:8000/admin/
- Media Files: http://127.0.0.1:8000/media/

---

*Documentation generated for Travel Map Project - Member 2 (Backend & Database)*
