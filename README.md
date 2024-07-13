### Database Schema Documentation

#### **Users Table**

- **Table Name**: users
- **Description**: Stores user information.
- **Fields**:
  - `id`: `int` (Primary Key, Auto Increment)
  - `unique_id`: `varchar`
  - `first_name`: `varchar`
  - `last_name`: `varchar`
  - `phone`: `varchar`
  - `email`: `varchar` (Unique)
  - `password`: `varchar`
  - `role`: `boolean`
  - `created_at`: `datetime`
  - `updated_at`: `datetime`

#### **Organisations Table**

- **Table Name**: organisations
- **Description**: Stores organisation details.
- **Fields**:
  - `id`: `int` (Primary Key, Auto Increment)
  - `name`: `varchar`
  - `description`: `varchar`
  - `created_at`: `datetime`
  - `updated_at`: `datetime`

#### **User_Organisation Table**

- **Table Name**: user_organisation
- **Description**: Maps users to organisations.
- **Fields**:
  - `id`: `int` (Primary Key, Auto Increment)
  - `user_id`: `varchar` (Foreign Key referencing `users.unique_id`)
  - `organisation_id`: `int` (Foreign Key referencing `organisations.id`)

#### **Notifications Table**

- **Table Name**: notifications
- **Description**: Stores user notifications.
- **Fields**:
  - `id`: `int` (Primary Key, Auto Increment)
  - `user_id`: `varchar` (Foreign Key referencing `users.unique_id`)
  - `message_data`: `json`
  - `read_status`: `varchar`
  - `created_at`: `datetime`

#### **Posts Table**

- **Table Name**: posts
- **Description**: Stores user posts.
- **Fields**:
  - `id`: `int` (Primary Key, Auto Increment)
  - `title`: `varchar`
  - `body`: `text`
  - `image`: `varchar`
  - `status`: `varchar`
  - `author_id`: `varchar` (Foreign Key referencing `users.unique_id`)
  - `created_at`: `datetime`
  - `updated_at`: `datetime`

#### **Messages Table**

- **Table Name**: messages
- **Description**: Stores user messages.
- **Fields**:
  - `id`: `int` (Primary Key, Auto Increment)
  - `sender_id`: `varchar` (Foreign Key referencing `users.unique_id`)
  - `receiver_id`: `varchar` (Foreign Key referencing `users.unique_id`)
  - `subject`: `varchar`
  - `body`: `text`
  - `sent_at`: `datetime`

#### **Payments Table**

- **Table Name**: payments
- **Description**: Stores payment details.
- **Fields**:
  - `id`: `int` (Primary Key, Auto Increment)
  - `user_id`: `varchar` (Foreign Key referencing `users.unique_id`)
  - `user_data`: `json`
  - `amount`: `decimal`
  - `payment_method`: `varchar`
  - `status`: `varchar`
  - `created_at`: `datetime`

#### **Transactions Table**

- **Table Name**: transactions
- **Description**: Stores transaction details.
- **Fields**:
  - `id`: `int` (Primary Key, Auto Increment)
  - `user_id`: `varchar` (Foreign Key referencing `users.unique_id`)
  - `payment_data`: `json`
  - `created_at`: `datetime`

### **API Design Documentation with JWT Authentication**

---

#### **Auth API**

- **Endpoint**: `/auth`
- **Description**: Manage authentication and authorization.
- **Methods**:

  ##### `POST /auth/register`
  - **Description**: Register a new user.
  - **Request Body**:
    ```json
    {
      "first_name": "string",
      "last_name": "string",
      "phone": "int",
      "email": "string",
      "password": "string",
      "role": "bool"
    }
    ```
  - **Response**:
    - **201 Created**:
      ```json
      {
        "message": "User registered successfully"
      }
      ```
    - **400 Bad Request**:
      ```json
      {
        "error": "Invalid input data"
      }
      ```
    - **409 Conflict**:
      ```json
      {
        "error": "User already exists"
      }
      ```

  ##### `POST /auth/login`
  - **Description**: Log in a user and return a JWT token.
  - **Request Body**:
    ```json
    {
      "email": "string",
      "password": "string"
    }
    ```
  - **Response**:
    - **200 OK**:
      ```json
      {
        "token": "string"
      }
      ```
    - **400 Bad Request**:
      ```json
      {
        "error": "Invalid email or password"
      }
      ```
    - **401 Unauthorized**:
      ```json
      {
        "error": "Unauthorized"
      }
      ```

  ##### `POST /auth/logout`
  - **Description**: Log out a user by invalidating the JWT token.
  - **Response**:
    - **200 OK**:
      ```json
      {
        "message": "User logged out successfully"
      }
      ```

---

#### **Securing Endpoints with JWT**

**General Security Rules:**
- **Authentication**: Include a JWT token in the `Authorization` header of the request with the format `Bearer <token>`.
- **Authorization**: Check user roles and permissions based on the information in the JWT token.

---

#### **Protected Endpoints**

- **Endpoint**: `/users`
- **Description**: Manage users. Requires authentication.
- **Methods**:

  ##### `GET /users`
  - **Description**: Get a list of users.
  - **Authentication**: Required
  - **Request Header**:
    - `Authorization`: `Bearer <token>`
  - **Response**:
    - **200 OK**:
      ```json
      [
        {
          "unique_id": "string",
          "first_name": "string",
          "last_name": "string",
          "phone": "int",
          "email": "string",
          "password": "string",
          "role": "bool",
          "created_at": "datetime",
          "updated_at": "datetime"
        }
      ]
      ```

  ##### `GET /users/{unique_id}`
  - **Description**: Get a user by ID.
  - **Authentication**: Required
  - **Parameters**:
    - `unique+_id`: `string` (Path Parameter)
  - **Request Header**:
    - `Authorization`: `Bearer <token>`
  - **Response**:
    - **200 OK**:
      ```json
      {
        "unique_id": "string",
        "first_name": "string",
        "last_name": "string",
        "phone": "int",
        "email": "string",
        "password": "string",
        "role": "bool",
        "created_at": "datetime",
        "updated_at": "datetime"
      }
      ```
    - **404 Not Found**:
      ```json
      {
        "error": "User not found"
      }
      ```

- **Endpoint**: `/organisations`
- **Description**: Manage organizations. Requires authentication.
- **Methods**:

  ##### `GET /organisations`
  - **Description**: Get a list of organizations.
  - **Authentication**: Required
  - **Request Header**:
    - `Authorization`: `Bearer <token>`
  - **Response**:
    - **200 OK**:
      ```json
      [
        {
          "id": "int",
          "name": "string",
          "description": "string",
          "created_at": "datetime",
          "updated_at": "datetime"
        }
      ]
      ```
    - **401 Unauthorized**:
      ```json
      {
        "error": "Unauthorized"
      }
      ```

  ##### `GET /organisations/{id}`
  - **Description**: Get an organization by ID.
  - **Authentication**: Required
  - **Parameters**:
    - `id`: `int` (Path Parameter)
  - **Request Header**:
    - `Authorization`: `Bearer <token>`
  - **Response**:
    - **200 OK**:
      ```json
      {
        "id": "int",
        "name": "string",
        "description": "string",
        "created_at": "datetime",
        "updated_at": "datetime"
      }
      ```
    - **404 Not Found**:
      ```json
      {
        "error": "Organization not found"
      }
      ```
    - **401 Unauthorized**:
      ```json
      {
        "error": "Unauthorized"
      }
      ```

  ##### `POST /organisations`
  - **Description**: Create a new organization.
  - **Authentication**: Required
  - **Request Header**:
    - `Authorization`: `Bearer <token>`
  - **Request Body**:
    ```json
    {
      "name": "string",
      "description": "string"
    }
    ```
  - **Response**:
    - **201 Created**:
      ```json
      {
        "message": "Organization created successfully"
      }
      ```
    - **400 Bad Request**:
      ```json
      {
        "error": "Invalid input data"
      }
      ```
    - **401 Unauthorized**:
      ```json
      {
        "error": "Unauthorized"
      }
      ```

  ##### `PUT /organisations/{id}`
  - **Description**: Update an existing organization.
  - **Authentication**: Required
  - **Parameters**:
    - `id`: `int` (Path Parameter)
  - **Request Header**:
    - `Authorization`: `Bearer <token>`
  - **Request Body**:
    ```json
    {
      "name": "string",
      "description": "string"
    }
    ```
  - **Response**:
    - **200 OK**:
      ```json
      {
        "message": "Organization updated successfully"
      }
      ```
    - **400 Bad Request**:
      ```json
      {
        "error": "Invalid input data"
      }
      ```
    - **404 Not Found**:
      ```json
      {
        "error": "Organization not found"
      }
      ```
    - **401 Unauthorized**:
      ```json
      {
        "error": "Unauthorized"
      }
      ```

  ##### `DELETE /organisations/{id}`
  - **Description**: Delete an organization by ID.
  - **Authentication**: Required
  - **Parameters**:
    - `id`: `int` (Path Parameter)
  - **Request Header**:
    - `Authorization`: `Bearer <token>`
  - **Response**:
    - **200 OK**:
      ```json
      {
        "message": "Organization deleted successfully"
      }
      ```
    - **404 Not Found**:
      ```json
      {
        "error": "Organization not found"
      }
      ```
    - **401 Unauthorized**:
      ```json
      {
        "error": "Unauthorized"
      }
      ```

- **Endpoint**: `/user_organisation`
- **Description**: Manage user-organisation relationships. Requires authentication.
- **Methods**:

  ##### `GET /user_organisation`
  - **Description**: Get a list of user-organisation relationships.
  - **Authentication**: Required
  - **Request Header**:
    - `Authorization`: `Bearer <token>`
  - **Response**:
    - **200 OK**:
      ```json
      [
        {
          "id": "int",
          "user_id": {
            "id": "int",
            "unique_id": "string",
            "first_name": "string",
            "last_name": "string",
            "phone": "int",
            "email": "string",
            "password": "string",
            "role": "bool",
            "created_at": "datetime",
            "updated_at": "datetime"
          },
          "organisation_id": {
            "id": "int",
            "name": "string",
            "description": "string",
            "created_at": "datetime",
            "updated_at": "datetime"
          }
        }
      ]
      ```

  ##### `GET /user_organisation/{id}`
  - **Description**: Get a user-organisation relationship by ID.
  - **Authentication**: Required
  - **Parameters**:
    - `id`: `int` (Path Parameter)
  - **Request Header**:
    - `Authorization`: `Bearer <token>`
  - **Response**:
    - **200 OK**:
      ```json
      {
        "id": "int",
        "user_id": {
          "id": "int",
          "unique_id": "string",
          "first_name": "string",
          "last_name": "string",
          "phone": "int",
          "email": "string",
          "password": "string",
          "role": "bool",
          "created_at": "datetime",
          "updated_at": "datetime"
        },
        "organisation_id": {
          "id": "int",
          "name": "string",
          "description": "string",
          "created_at": "datetime",
          "updated_at": "datetime"
        }
      }
      ```
    - **404 Not Found**:
      ```json
      {
        "error": "User-organisation relationship not found"
      }
      ```
    - **401 Unauthorized**:
      ```json
      {
        "error": "Unauthorized"
      }
      ```

  ##### `POST /user_organisation`
  - **Description**: Create a new user-organisation relationship.
  - **Authentication**: Required
  - **Request Header**:
    - `Authorization`: `Bearer <token>`
  - **Request Body**:
    ```json
    {
      "user_id": "int",
      "organisation_id": "int"
    }
    ```
  - **Response**:
    - **201 Created**:
      ```json
      {
        "message": "User-organisation relationship created successfully"
      }
      ```
    - **400 Bad Request**:
      ```json
      {
        "error": "Invalid input data"
      }
      ```
    - **401 Unauthorized**:
      ```json
      {
        "error": "Unauthorized"
      }
      ```

  ##### `PUT /user_organisation/{id}`
  - **Description**: Update an existing user-organisation relationship.
  - **Authentication**: Required
  - **Parameters**:
    - `id`: `int` (Path Parameter)
  - **Request Header**:
    - `Authorization`: `Bearer <token>`
  - **Request Body**:
    ```json
    {
      "user_id": "int",
      "organisation_id": "int"
    }
    ```
  - **Response**:
    - **200 OK**:
      ```json
      {
        "message": "User-organisation relationship updated successfully"
      }
      ```
    - **400 Bad Request**:
      ```json
      {
        "error": "Invalid input data"
      }
      ```
    - **404 Not Found**:
      ```json
      {
        "error": "User-organisation relationship not found"
      }
      ```
    - **401 Unauthorized**:
      ```json
      {
        "error": "Unauthorized"
      }
      ```

  ##### `DELETE /user_organisation/{id}`
  - **Description**: Delete a user-organisation relationship by ID.
  - **Authentication**: Required
  - **Parameters**:
    - `id`: `int` (Path Parameter)
  - **Request Header**:
    - `Authorization`: `Bearer <token>`
  - **Response**:
    - **200 OK**:
      ```json
      {
        "message": "User-organisation relationship deleted successfully"
      }
      ```
    - **404 Not Found**:
      ```json
      {
        "error": "User-organisation relationship not found"
      }
      ```
    - **401 Unauthorized**:
      ```json
      {
        "error": "Unauthorized"
      }
      ```

### Endpoint: `/payments`

**Description**: Manage payments. Requires authentication.

### Methods:

#### `GET /payments`

- **Description**: Get a list of payments.
- **Authentication**: Required
- **Request Header**:
  - `Authorization`: `Bearer <token>`
- **Response**:
  - **200 OK**:
    ```json
    [
      {
        "id": "int",
        "user_id": "string",
        "user_data": "json",
        "amount": "decimal",
        "payment_method": "string",
        "status": "string",
        "created_at": "datetime"
      }
    ]
    ```
  - **401 Unauthorized**:
    ```json
    {
      "error": "Unauthorized"
    }
    ```

#### `GET /payments/{id}`

- **Description**: Get a payment by ID.
- **Authentication**: Required
- **Parameters**:
  - `id`: `int` (Path Parameter)
- **Request Header**:
  - `Authorization`: `Bearer <token>`
- **Response**:
  - **200 OK**:
    ```json
    {
      "id": "int",
      "user_id": "string",
      "user_data": "json",
      "amount": "decimal",
      "payment_method": "string",
      "status": "string",
      "created_at": "datetime"
    }
    ```
  - **404 Not Found**:
    ```json
    {
      "error": "Payment not found"
    }
    ```
  - **401 Unauthorized**:
    ```json
    {
      "error": "Unauthorized"
    }
    ```

#### `POST /payments`

- **Description**: Create a new payment.
- **Authentication**: Required
- **Request Header**:
  - `Authorization`: `Bearer <token>`
- **Request Body**:
  ```json
  {
    "user_id": "string",
    "amount": "decimal",
    "payment_method": "string",
    "status": "string"
  }
  ```
- **Response**:
  - **201 Created**:
    ```json
    {
      "message": "Payment created successfully"
    }
    ```
  - **400 Bad Request**:
    ```json
    {
      "error": "Invalid input data"
    }
    ```
  - **401 Unauthorized**:
    ```json
    {
      "error": "Unauthorized"
    }
    ```

- **Endpoint**: `/transactions`
- **Description**: Manage transactions. Requires authentication.
- **Methods**:

  ##### `GET /transactions`
  - **Description**: Get a list of transactions.
  - **Authentication**: Required
  - **Request Header**:
    - `Authorization`: `Bearer <token>`
  - **Response**:
    - **200 OK**:
      ```json
      [
        {
          "id": "int",
          "user_id": {
            "id": "int",
            "unique_id": "string",
            "first_name": "string",
            "last_name": "string",
            "phone": "int",
            "email": "string",
            "password": "string",
            "role": "bool",
            "created_at": "datetime",
            "updated_at": "datetime"
          },
          "payment_data": {
            "id": "int",
            "user_id": "int",
            "user_data": {
              "id": "int",
              "unique_id": "string",
              "first_name": "string",
              "last_name": "string",
              "phone": "int",
              "email": "string",
              "password": "string",
              "role": "bool",
              "created_at": "datetime",
              "updated_at": "datetime"
            },
            "amount": "decimal",
            "payment_method": "string",
            "status": "string",
            "created_at": "datetime"
          },
          "created_at": "datetime"
        }
      ]
      ```

  ##### `GET /transactions/{id}`
  - **Description**: Get a transaction by ID.
  - **Authentication**: Required
  - **Parameters**:
    - `id`: `int` (Path Parameter)
  - **Request Header**:
    - `Authorization`: `Bearer <token>`
  - **Response**:
    - **200 OK**:
      ```json
      {
        "id": "int",
        "user_id": {
          "id": "int",
          "unique_id": "string",
          "first_name": "string",
          "last_name": "string",
          "phone": "int",
          "email": "string",
          "password": "string",
          "role": "bool",
          "created_at": "datetime",
          "updated_at": "datetime"
        },
        "payment_data": {
          "id": "int",
          "user_id": "int",
          "user_data": {
            "id": "int",
            "unique_id": "string",
            "first_name": "string",
            "last_name": "string",
            "phone": "int",
            "email": "string",
            "password": "string",
            "role": "bool",
            "created_at": "datetime",
            "updated_at": "datetime"
          },
          "amount": "decimal",
          "payment_method": "string",
          "status": "string",
          "created_at": "datetime"
        },
        "created_at": "datetime"
      }
      ```
    - **404 Not Found**:
      ```json
      {
        "error": "Transaction not found"
      }
      ```

- **Endpoint**: `/notifications`
- **Description**: Manage notifications. Requires authentication.
- **Methods**:

  ##### `GET /notifications`
  - **Description**: Get a list of notifications.
  - **Authentication**: Required
  - **Request Header**:
    - `Authorization`: `Bearer <token>`
  - **Response**:
    - **200 OK**:
      ```json
      [
        {
          "id": "int",
          "user_id": "string",
          "message_data": {
            "id": "int",
            "sender_id": {
              "id": "int",
              "unique_id": "string",
              "first_name": "string",
              "last_name": "string",
              "phone": "int",
              "email": "string",
              "password": "string",
              "role": "bool",
              "created_at": "datetime",
              "updated_at": "datetime"
            },
            "receiver_id": {
              "id": "int",
              "unique_id": "string",
              "first_name": "string",
              "last_name": "string",
              "phone": "int",
              "email": "string",
              "password": "string",
              "role": "bool",
              "created_at": "datetime",
              "updated_at": "datetime"
            },
            "subject": "string",
            "body": "text",
            "sent_at": "datetime"
          },
          "status": "string",
          "created_at": "datetime"
        }
      ]
      ```

  ##### `GET /notifications/{id}`
  - **Description**: Get a notification by ID.
  - **Authentication**: Required
  - **Parameters**:
    - `id`: `int` (Path Parameter)
  - **Request Header**:
   

 - `Authorization`: `Bearer <token>`
  - **Response**:
    - **200 OK**:
      ```json
      {
        "id": "int",
        "user_id": "string",
        "message_data": {
          "id": "int",
          "sender_id": {
            "id": "int",
            "unique_id": "string",
            "first_name": "string",
            "last_name": "string",
            "phone": "int",
            "email": "string",
            "password": "string",
            "role": "bool",
            "created_at": "datetime",
            "updated_at": "datetime"
          },
          "receiver_id": {
            "id": "int",
            "unique_id": "string",
            "first_name": "string",
            "last_name": "string",
            "phone": "int",
            "email": "string",
            "password": "string",
            "role": "bool",
            "created_at": "datetime",
            "updated_at": "datetime"
          },
          "subject": "string",
          "body": "text",
          "sent_at": "datetime"
        },
        "read_status": "string",
        "created_at": "datetime"
      }
      ```
    - **404 Not Found**:
      ```json
      {
        "error": "Notification not found"
      }
      ```

- **Endpoint**: `/posts`
- **Description**: Manage posts. Requires authentication.
- **Methods**:

  ##### `GET /posts`
  - **Description**: Get a list of posts.
  - **Authentication**: Required
  - **Request Header**:
    - `Authorization`: `Bearer <token>`
  - **Response**:
    - **200 OK**:
      ```json
      [
        {
          "id": "int",
          "title": "string",
          "body": "text",
          "image": "string",
          "status": "string",
          "author_id": {
            "id": "int",
            "unique_id": "string",
            "first_name": "string",
            "last_name": "string",
            "phone": "int",
            "email": "string",
            "password": "string",
            "role": "bool",
            "created_at": "datetime",
            "updated_at": "datetime"
          },
          "created_at": "datetime",
          "updated_at": "datetime"
        }
      ]
      ```

  ##### `GET /posts/{id}`
  - **Description**: Get a post by ID.
  - **Authentication**: Required
  - **Parameters**:
    - `id`: `int` (Path Parameter)
  - **Request Header**:
    - `Authorization`: `Bearer <token>`
  - **Response**:
    - **200 OK**:
      ```json
      {
        "id": "int",
        "title": "string",
        "body": "text",
        "image": "string",
        "status": "string",
        "author_id": {
          "id": "int",
          "unique_id": "string",
          "first_name": "string",
          "last_name": "string",
          "phone": "int",
          "email": "string",
          "password": "string",
          "role": "bool",
          "created_at": "datetime",
          "updated_at": "datetime"
        },
        "created_at": "datetime",
        "updated_at": "datetime"
      }
      ```
    - **404 Not Found**:
      ```json
      {
        "error": "Post not found"
      }
      ```

    ##### `PUT /posts/{id}`
  - **Description**: Update a post by ID.
  - **Authentication**: Required
  - **Parameters**:
    - `id`: `int` (Path Parameter)
  - **Request Header**:
    - `Authorization`: `Bearer <token>`
  - **Response**:
    - **200 OK**:
      ```json
      {
        "response": "Post updated",
      }
      ```
    - **404 Not Found**:
      ```json
      {
        "error": "Post not found"
      }
      ```

    ##### `DELETE /posts/{id}`
  - **Description**: Update a post by ID.
  - **Authentication**: Required
  - **Parameters**:
    - `id`: `int` (Path Parameter)
  - **Request Header**:
    - `Authorization`: `Bearer <token>`
  - **Response**:
    - **200 OK**:
      ```json
      {
        "response": "Post deleted",
      }
      ```
    - **404 Not Found**:
      ```json
      {
        "error": "Post not found"
      }
      ```

- **Endpoint**: `/messages`
- **Description**: Manage messages. Requires authentication.
- **Methods**:

  ##### `GET /messages`
  - **Description**: Get a list of messages.
  - **Authentication**: Required
  - **Request Header**:
    - `Authorization`: `Bearer <token>`
  - **Response**:
    - **200 OK**:
      ```json
      [
        {
          "id": "int",
          "sender_id": {
            "id": "int",
            "unique_id": "string",
            "first_name": "string",
            "last_name": "string",
            "phone": "int",
            "email": "string",
            "password": "string",
            "role": "bool",
            "created_at": "datetime",
            "updated_at": "datetime"
          },
          "receiver_id": {
            "id": "int",
            "unique_id": "string",
            "first_name": "string",
            "last_name": "string",
            "phone": "int",
            "email": "string",
            "password": "string",
            "role": "bool",
            "created_at": "datetime",
            "updated_at": "datetime"
          },
          "subject": "string",
          "body": "text",
          "sent_at": "datetime"
        }
      ]
      ```

  ##### `GET /messages/{id}`
  - **Description**: Get a message by ID.
  - **Authentication**: Required
  - **Parameters**:
    - `id`: `int` (Path Parameter)
  - **Request Header**:
    - `Authorization`: `Bearer <token>`
  - **Response**:
    - **200 OK**:
      ```json
      {
        "id": "int",
        "sender_id": {
          "id": "int",
          "unique_id": "string",
          "first_name": "string",
          "last_name": "string",
          "phone": "int",
          "email": "string",
          "password": "string",
          "role": "bool",
          "created_at": "datetime",
          "updated_at": "datetime"
        },
        "receiver_id": {
          "id": "int",
          "unique_id": "string",
          "first_name": "string",
          "last_name": "string",
          "phone": "int",
          "email": "string",
          "password": "string",
          "role": "bool",
          "created_at": "datetime",
          "updated_at": "datetime"
        },
        "subject": "string",
        "body": "text",
        "sent_at": "datetime"
      }
      ```
    - **404 Not Found**:
      ```json
      {
        "error": "Message not found"
      }
      ```
---
