from rest_framework import viewsets,status
from .models import Employee,Payslip
from .serializers import EmployeeSerializer, SendPayslipRequestSerializer , PayslipSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .send_email import send_monthly_payslips
from drf_yasg.utils import swagger_auto_schema
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json
from rest_framework.parsers import MultiPartParser, FormParser


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

class PayslipViewSet(viewsets.ModelViewSet):
    queryset = Payslip.objects.all()
    serializer_class = PayslipSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # Enables file uploads

    @swagger_auto_schema(
        operation_description="Create a payslip with file upload and dropdowns for employee/month/year.",
        request_body=PayslipSerializer
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
class SendPayslipsView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(request_body=SendPayslipRequestSerializer)
    def post(self, request):
        serializer = SendPayslipRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            month = serializer.validated_data.get("month")
            year = serializer.validated_data.get("year")

            # Schedule email sending to run in the next minute (or use crontab for monthly)
            schedule, created = IntervalSchedule.objects.get_or_create(every=1, period=IntervalSchedule.MONTHS)
            PeriodicTask.objects.create(
                interval=schedule,
                name=f"SendPayslips6-{month}-{year}",
                task='payslips.send_email.send_monthly_payslips',
                args=json.dumps([month, year])
            )
            
            return Response({"status": f"Payslip sending scheduled for {month} {year}."}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

