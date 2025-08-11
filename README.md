# Restaurant-Management-System

Restaurant Management System - A Django-Based Web Application
This is a comprehensive restaurant management system built with the Django framework. The application is designed to streamline various restaurant operations, including online ordering, table reservations, inventory tracking, and order management, all through a clean and intuitive web interface.

Screenshots
Here’s a glimpse into the different modules of the application:

Customer Dashboard: Menu & Ordering
![](https://i.postimg.cc/7ZkNp3hT/Screenshot-2025-08-11-154850.png)

Your Order (Shopping Cart)
![](https://i.postimg.cc/C1zCjJP9/Screenshot-2025-08-11-155720.png)


Table Reservation System
![](https://i.postimg.cc/rs4SHsLJ/Screenshot-2025-08-11-155752.png)


Admin Panel: Inventory & Table Management
![](https://i.postimg.cc/XNBcqHyC/Screenshot-2025-08-11-155910.png)



Admin Panel: Order Management
![](https://i.postimg.cc/dtMRy28S/Screenshot-2025-08-11-155929.png)




Features:


This application is divided into two main parts: a customer-facing dashboard and an admin panel.



Customer Features:


Browse Menu: View all available food items with their prices and stock status.


Shopping Cart: Add items to a cart, adjust quantities, and view the total cost.


Place Orders: Finalize and place orders directly from the cart.


Table Reservations: Book a table by providing customer name, time, and number of guests. View current reservations.




Admin Features:

Inventory Management: View and update the stock levels for all menu items.


Table Availability: Manage the status of restaurant tables (Available/Occupied).


Order Management: View all incoming orders with details and update their status (e.g., Pending, Completed).


User Authentication: Secure login/logout functionality for both customers and admins.


Technologies Used:


Backend: Python, Django

Frontend: HTML, CSS, JavaScript

Database: SQLite 3 (for development)



Setup and Installation
To run this project on your local machine, follow these steps:


Clone the repository:

git clone [https://github.com/Amangupta87410/Restaurant-Management-System.git](https://github.com/Amangupta87410/Restaurant-Management-System.git)
cd Restaurant-Management-System/restaurant_management_project



Create and activate a virtual environment:

# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

Install the dependencies:
(Note: A requirements.txt file should be created for a production-ready project.)

pip install Django

Apply database migrations:

python manage.py migrate

Create a superuser to access the admin panel:

python manage.py createsuperuser

Run the development server:

python manage.py runserver

The application will be available at http://127.0.0.1:8000/.



Project Structure:


Restaurant-Management-System/
└── restaurant_management_project/
    ├── media/menu_images/
    ├── restaurant_app/
    ├── restaurant_management_project/
    ├── templates/
    ├── db.sqlite3
    ├── manage.py
    └── README.md
