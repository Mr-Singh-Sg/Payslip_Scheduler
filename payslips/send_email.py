from celery import shared_task
from django.core.mail import EmailMessage
from .models import Payslip
from django.template.loader import render_to_string
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True)
def send_monthly_payslips(self,month, year):
    payslips = Payslip.objects.filter(month=month, year=year)
    for payslip in payslips:
        subject = f"Payslip for {month} {year}"
        body = render_to_string("email_template.html", {"name": payslip.employee.user.get_full_name()})
        email = EmailMessage(subject, body, to=[payslip.employee.user.email])
        email.attach_file(payslip.pdf.path)
        email.send()
    print("run sucess schedule")  

