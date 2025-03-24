# TFA Clothing Website

A minimal Django website displaying men's and women's clothing.

## Setup and Run

1. Make sure you have Python installed on your system

2. Set up a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```
   python manage.py migrate
   ```

5. Load initial data:
   ```
   python manage.py loaddata clothes/fixtures/initial_data.json
   ```

6. Create a superuser (for admin access):
   ```
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```
   python manage.py runserver
   ```

8. Open your browser and navigate to:
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Features

- Minimal design
- Men's and women's clothing sections
- Admin panel for managing products 