# Little Lemon Restaurant API

## Project Overview

This project implements a fully functioning API for the Little Lemon restaurant using Django Rest Framework (DRF). The API allows client application developers to create web and mobile applications with various functionalities for different user roles.

### Key Features

- User authentication and authorization
- Menu item management
- Order placement and tracking
- Cart management
- User group management (Manager, Delivery Crew, Customer)
- Pagination, filtering, and sorting capabilities

## Tech Stack

- Python
- Django
- Django Rest Framework
- Djoser (for authentication endpoints)
- pipenv (for dependency management)

## Project Structure

The project consists of a single Django app called `LittleLemonAPI` that implements all the required API endpoints.

## User Roles

1. **Manager**: Can perform all operations, including user management
2. **Delivery Crew**: Can view and update assigned orders
3. **Customer**: Can browse menu, place orders, and view their own orders

## API Endpoints

### User Registration and Token Generation

| Endpoint                | Method | Purpose                                          |
|-------------------------|--------|--------------------------------------------------|
| `/api/users`            | POST   | Create a new user                                |
| `/api/users/users/me/`  | GET    | Display current user information                 |
| `/token/login/`         | POST   | Generate access token                            |

### Menu Items

| Endpoint                   | Method             | Role                  | Purpose                       |
|----------------------------|---------------------|----------------------|-------------------------------|
| `/api/menu-items`          | GET                 | All                  | List all menu items           |
| `/api/menu-items`          | POST                | Manager              | Create a new menu item        |
| `/api/menu-items/{id}`     | GET                 | All                  | Retrieve a specific menu item |
| `/api/menu-items/{id}`     | PUT, PATCH, DELETE  | Manager              | Update or delete a menu item  |

### User Group Management

| Endpoint                                  | Method | Role    | Purpose                                 |
|-------------------------------------------|--------|---------|------------------------------------------|
| `/api/groups/manager/users`               | GET    | Manager | List all managers                        |
| `/api/groups/manager/users`               | POST   | Manager | Assign user to manager group             |
| `/api/groups/manager/users/{userId}`      | DELETE | Manager | Remove user from manager group           |
| `/api/groups/delivery-crew/users`         | GET    | Manager | List all delivery crew                   |
| `/api/groups/delivery-crew/users`         | POST   | Manager | Assign user to delivery crew group       |
| `/api/groups/delivery-crew/users/{userId}`| DELETE | Manager | Remove user from delivery crew group     |

### Cart Management

| Endpoint              | Method | Role     | Purpose                               |
|-----------------------|--------|----------|---------------------------------------|
| `/api/cart/menu-items`| GET    | Customer | View current cart items               |
| `/api/cart/menu-items`| POST   | Customer | Add item to cart                      |
| `/api/cart/menu-items`| DELETE | Customer | Clear cart                            |

### Order Management

| Endpoint           | Method        | Role          | Purpose                               |
|--------------------|---------------|---------------|---------------------------------------|
| `/api/orders`      | GET           | All           | List orders (scope depends on role)   |
| `/api/orders`      | POST          | Customer      | Create a new order                    |
| `/api/orders/{id}` | GET           | Customer      | Retrieve a specific order             |
| `/api/orders/{id}` | PUT, PATCH    | Manager       | Update order status or assign crew    |
| `/api/orders/{id}` | DELETE        | Manager       | Delete an order                       |
| `/api/orders/{id}` | PATCH         | Delivery Crew | Update order status                   |

## Additional Features

### Pagination

The API implements pagination for endpoints that return multiple items, such as `/api/menu-items` and `/api/orders`. This improves performance and reduces bandwidth usage for large datasets.

### Filtering and Sorting

Users can filter and sort results for the `/api/menu-items` and `/api/orders` endpoints based on various parameters, enhancing the API's flexibility and usability.

### Throttling

API throttling is implemented to limit the number of requests a user can make within a given time frame. This helps prevent abuse and ensures fair usage of the API resources.

## Authentication and Authorization

The project uses token-based authentication. Users must include their token in the header of their requests to access protected endpoints. Different endpoints have different permission levels based on the user's role.

## Error Handling

The API returns appropriate HTTP status codes and error messages for various scenarios:

- 200 OK: Successful GET, PUT, PATCH, and DELETE calls
- 201 Created: Successful POST requests
- 400 Bad Request: Validation failures
- 401 Unauthorized: Authentication failures
- 403 Forbidden: Permission denied
- 404 Not Found: Resource not found

## Getting Started

1. Clone the repository
2. Install dependencies using pipenv: `pipenv install`
3. Activate the virtual environment: `pipenv shell`
4. Run migrations: `python manage.py migrate`
5. Create a superuser: `python manage.py createsuperuser`
6. Run the development server: `python manage.py runserver`

## Testing

Comprehensive unit tests and integration tests are included to ensure the reliability and correctness of the API endpoints.

## Documentation

Detailed API documentation is available, describing each endpoint, its parameters, and expected responses. This documentation can be accessed through the Django Rest Framework's built-in API browser or a dedicated documentation page.

## Contributing

Contributions to the project are welcome. Please follow the standard fork-and-pull request workflow. Make sure to adhere to the project's coding standards and include appropriate tests for new features or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

