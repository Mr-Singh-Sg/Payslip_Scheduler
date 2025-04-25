# 🧾 Acme Payslip Email Scheduler

This Django project mimics Acme Inc.'s monthly payslip dispatch process by sending PDF attachments to employees via email. It uses:

- **Django** for the backend
- **Celery** for asynchronous job processing
- **Redis** as the message broker
- **SMTP** for sending emails with attached PDFs

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/email_schedule.git
cd email_schedule

### 2. Activate the virtual environment
python -m venv venv
## On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

## Install required packages
pip install -r requirements.txt

## change credentail for email in Setting.py

EMAIL_HOST=smtp.yourprovider.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-password
EMAIL_USE_TLS=True

### 4. run schedular by 
celery -A email_schedule worker --loglevel=info
celery -A email_schedule beat --loglevel=info

### 3. run server by 
python manage.py runserver

## Below are the neccessary command to run application

Install requirements	pip install -r requirements.txt
Run migrations	python manage.py migrate
Start server	python manage.py runserver
Start Celery worker	celery -A email_schedule worker --loglevel=info
Start Redis (Windows)	Run redis-server.exe
Start Celery Beat	celery -A email_schedule beat --loglevel=info
Test email task	Run task in shell as shown above



