from django.core.management.base import BaseCommand
from payslips.models import User

class Command(BaseCommand):
    help = 'Create a default admin user'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(username='admin', email='admin@acme.com', password='admin123', role='admin')
            self.stdout.write(self.style.SUCCESS('Successfully created default admin user'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists'))