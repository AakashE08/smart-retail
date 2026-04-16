# Retail Shop Management System

A comprehensive retail shop management system built with Django and MySQL.

## Features

- 🔐 Role-based access control (Admin, Employee, Customer)
- 🧾 Billing and invoice generation
- 📦 Inventory management with alerts
- 🛒 Online order portal
- 📊 Sales and inventory reports
- 🎁 Promotions and discounts
- 🔄 Product returns and refunds
- 📱 Responsive web interface

## Tech Stack

- Backend: Django (Python)
- Database: MySQL
- Frontend: Django Templates with Bootstrap
- Additional: ReportLab (PDF generation)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/retail-management.git
cd retail-management
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure MySQL:
- Create a new MySQL database
- Update database settings in `retail_management/settings.py`

5. Run migrations:
```bash
python manage.py migrate
```

6. Initialize MySQL operations:
```bash
python manage.py initialize_mysql
```

7. Create a superuser:
```bash
python manage.py createsuperuser
```

8. Run the development server:
```bash
python manage.py runserver
```

## Project Structure

```
retail_management/
├── accounts/           # User authentication and profiles
├── inventory/          # Product and stock management
├── orders/            # Order processing
├── billing/           # Billing and invoicing
├── returns/           # Returns and refunds
├── promotions/        # Discounts and promotions
├── reports/           # Sales and inventory reports
└── retail_management/ # Project settings
```

## Key Features Implementation

### Database Operations
- MySQL Views for inventory summary
- Triggers for automatic inventory updates
- Cursors for batch processing
- Complex joins for reports

### Security
- Role-based access control
- Secure password hashing
- Session management
- CSRF protection

### Automation
- Low stock alerts
- Expiry date notifications
- Automatic inventory updates
- Sales reports generation

## Usage

1. **Admin Access**
   - Manage users and roles
   - Configure system settings
   - View all reports and analytics

2. **Employee Access**
   - Process bills and orders
   - Manage inventory
   - Handle returns and refunds

3. **Customer Access**
   - Browse products
   - Place orders
   - View order history
   - Request returns

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, email support@example.com or create an issue in the repository. 