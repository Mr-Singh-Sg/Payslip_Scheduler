import datetime
from rest_framework import serializers
from .models import User, Employee ,Payslip

MONTH_CHOICES = [
    ('January', 'January'), ('February', 'February'), ('March', 'March'),
    ('April', 'April'), ('May', 'May'), ('June', 'June'),
    ('July', 'July'), ('August', 'August'), ('September', 'September'),
    ('October', 'October'), ('November', 'November'), ('December', 'December'),
]

CURRENT_YEAR = datetime.datetime.now().year
YEAR_CHOICES = [(str(y), str(y)) for y in range(CURRENT_YEAR - 1, CURRENT_YEAR + 6)]
YEAR_CHOICES_INT = [(y, y) for y in range(CURRENT_YEAR - 1, CURRENT_YEAR + 6)]  # For Payslip model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    

class PayslipSerializer(serializers.ModelSerializer):
    # Replace ChoiceField with PrimaryKeyRelatedField (Django handles ID <-> object)
    employee = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.select_related('user').all(),
        label="Employee"
    )
    month = serializers.ChoiceField(choices=MONTH_CHOICES)
    year = serializers.ChoiceField(choices=YEAR_CHOICES_INT)
    pdf = serializers.FileField(use_url=True)

    class Meta:
        model = Payslip
        fields = ['id', 'employee', 'month', 'year', 'pdf']

    def validate(self, data):
        if Payslip.objects.filter(
            employee=data['employee'],
            month=data['month'],
            year=data['year']
        ).exists():
            raise serializers.ValidationError("Payslip already exists for this employee and month.")
        return data
    
class SendPayslipRequestSerializer(serializers.Serializer):
    month = serializers.ChoiceField(choices=MONTH_CHOICES)
    year = serializers.ChoiceField(choices=YEAR_CHOICES)

class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Employee
        fields = ['id', 'user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        return Employee.objects.create(user=user)