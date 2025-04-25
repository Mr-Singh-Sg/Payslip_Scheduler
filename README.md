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
