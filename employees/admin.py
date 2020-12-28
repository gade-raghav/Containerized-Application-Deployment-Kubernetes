from django.contrib import admin

# Register your models here.

from .models import Employee

class EmployeeAdmin(admin.ModelAdmin):
    fields = [
        'employee_id',
        'employee_name',
        'date_created',
    ]

    readonly_fields= [
        'date_created',
    ]


admin.site.register(Employee,EmployeeAdmin)
