# Mine's Restaurant 🍽️

A restaurant menu and ordering web application built using Python and Django. Mine's Restaurant allows customers to explore dishes by category, select multiple plates, manage quantities, calculate order totals, place orders, and submit reviews through a simple, responsive web interface.

## ✨ Features

### 🍴 Menu Management
- Browse dishes across Breakfast, Vegetarian, Non-Vegetarian, Starters, and Ice Cream categories.
- View dish names, descriptions, prices, and images.
- Display available dishes by category.

### 🛒 Dish Selection
- Add dishes to the selection.
- Increase or decrease the quantity of each dish.
- Remove dishes and clear the entire selection.
- View the total number of plates and subtotal.
- Retain selected items using Django sessions.

### 🧾 Checkout and Orders
- Enter customer details and a contact number.
- Choose the order type: delivery or takeaway, according to the available options.
- Enter a delivery address when required.
- Review the order summary before placing an order.
- Generate an order confirmation with an order number, order status, and itemized summary.

**Note:** This project currently demonstrates order placement and confirmation. It does not process online payments.

### ⭐ Customer Reviews
- Submit reviews for selected dishes.
- Provide a rating between 1 and 5.
- Add comments and view validation messages for invalid input.

### 🎨 User Interface
- Restaurant branding and logo.
- Food-themed backgrounds and dish images.
- Responsive layouts for different screen sizes.
- Styled selection, checkout, confirmation, and review pages.

## 🧰 Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application programming |
| Django 5.2.x | Backend framework |
| SQLite | Database |
| HTML5 | Page structure |
| CSS3 | Styling and responsive layouts |
| Bootstrap 5 | UI components and layout |
| Pillow | Image handling, if required by the configured image fields |
| Git and GitHub | Version control and project hosting |

## 📁 Project Structure

```text
Restaurant/
├── app/
│   ├── migrations/
│   ├── static/
│   │   └── images/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── project30/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── templates/
│   ├── menu_view.html
│   ├── menu_category.html
│   ├── update_selection.html
│   ├── checkout.html
│   ├── order_confirmation.html
│   └── create_review.html
├── manage.py
└── README.md
```

*The structure above highlights the main project files. Additional templates, configuration files, and static assets may also be present.*

## ⚙️ Run the Project Locally

### Prerequisites

- Python installed on your system.
- pip, the Python package installer.
- Git, if cloning the repository.

### 1. Clone the repository

```bash
git clone https://github.com/rajasekharkuruva583-source/Restaurant.git
cd Restaurant
```

### 2. Create a virtual environment

Windows CMD:

```bat
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bat
python -m pip install --upgrade pip
python -m pip install "Django>=5.2,<5.3" Pillow
```

If a `requirements.txt` file is provided with the project, use the following command instead:

```bat
python -m pip install -r requirements.txt
```

### 4. Apply database migrations

```bat
python manage.py migrate
```

### 5. Check the project

```bat
python manage.py check
```

### 6. Run automated tests

```bat
python manage.py test app
```

### 7. Start the development server

```bat
python manage.py runserver
```

Open the application in your browser:

http://127.0.0.1:8000/menu_view/

If port 8000 is already in use, run:

```bat
python manage.py runserver 8001
```

Then open:

http://127.0.0.1:8001/menu_view/

## 🧪 Testing

The project has six automated Django tests, which passed in the development environment on October 28, 2026.

Run the tests again after making changes:

```bat
python manage.py test app
```

The test suite can be expanded to cover quantity updates, subtotal calculations, checkout validation, order creation, order confirmation, and review submission.

## 🔐 Security and Deployment Notes

- Keep Django's secret key and other credentials out of source control.
- Do not commit the virtual environment or Python cache files.
- Review whether the local SQLite database should be included before publishing.
- Configure `DEBUG`, `ALLOWED_HOSTS`, and environment variables before production deployment.
- Configure static and uploaded media files appropriately for deployment.
- Use a production-ready Django application server for hosting.
- Review access controls for administrative operations.
- Do not collect or store real payment details in this demonstration project.

## 🚀 Future Improvements

- Expand automated tests for the complete ordering workflow.
- Add order history and order status management.
- Improve accessibility and mobile responsiveness.
- Add email notifications for order confirmation.
- Integrate a secure payment gateway if online payments are required.
- Deploy the application to a suitable hosting platform.

## 👨‍💻 Author

**Kuruva Rajasekhar**

GitHub: [rajasekharkuruva583-source](https://github.com/rajasekharkuruva583-source)

LinkedIn: [Rajasekhar Kuruva](https://www.linkedin.com/in/rajasekhar-kuruva-ba94352aa)

