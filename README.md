# LivePoll

## Description
A full-stack web application designed for creating and participating in real-time polls. The project features live score updates using WebSockets, allowing connected users to see voting results update instantly without refreshing the page.

## Tech Stack
- Python / FastAPI: Backend API and server framework

- SQLAlchemy: ORM for database interaction and object mapping

- MySQL / MariaDB: Relational database management

- WebSockets: Real-time bidirectional communication and broadcasting

- JavaScript / HTML / CSS: Frontend user interface and interactive components

- Pytest: Unit testing framework


## Key Features
- Real-Time Updates: WebSockets automatically broadcast voting changes to all users currently viewing the poll results.

- Comprehensive REST API: Full CRUD endpoints exposed via FastAPI's automatically generated Interactive API Documentation (`/docs`).

- Duplicate Vote Prevention: LocalStorage checks determine if a browser session has already voted, enabling quick side-by-side testing across multiple browsers.

- Input Validation & Error Handling: Client-side and server-side form validation, complemented by a custom error page.

- Type Annotations & Docstrings: Complete code documentation with Python type hinting and structured docstrings across all modules.

- Automated Unit Testing: Includes a suite of unit tests powered by Pytest that validate core logic directly against the database.


## How to Run the Project

1. Install and open the **XAMPP Control Panel**, then start the **MySQL** and **Apache** modules.

2. Open `localhost/phpmyadmin` in your browser and import the `livepoll.sql` file located in the root directory (this generates the database along with 20 sample polls). You can stop Apache afterwards.

3. Execute the automated setup and launcher script from the root directory:

```bash
.\run
```

4. Open the local address provided in the terminal output to view the application

## How to run tests

Run the unit test suite using the virtual environment interpreter:

```bash
.\venv\Scripts\python.exe -m pytest
```
