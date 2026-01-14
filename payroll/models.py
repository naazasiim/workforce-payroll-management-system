from django.db import models
from employees.models import Employee


class Payroll(models.Model):

    class Status(models.TextChoices):
        GENERATED = "GENERATED", "Generated"
        APPROVED = "APPROVED", "Approved"
        PAID = "PAID", "Paid"

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="payrolls")
    month = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()

    # Salary snapshot (VERY IMPORTANT)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    hra = models.DecimalField(max_digits=10, decimal_places=2)
    allowances = models.DecimalField(max_digits=10, decimal_places=2)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    total_working_days = models.PositiveSmallIntegerField()
    payable_days = models.PositiveSmallIntegerField()

    net_salary = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.GENERATED
    )

    generated_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("employee", "month", "year")
        indexes = [
            models.Index(fields=["employee", "month", "year"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.employee.employee_code} - {self.month}/{self.year}"
