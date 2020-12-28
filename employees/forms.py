from django.forms import ModelForm,TextInput
from .models import *

#Employee-FORM

class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = ['employee_name','employee_id']
        labels = {
            'employee_name': ('Name'),
            'employee_id': ('Employee-ID')
        }

        def clean(self):
            email = self.cleaned_data.get('email')
            user  = self.cleaned_data.get('username')
            if Employee.employee_id < 1000000 or Employee.employee_id > 99999999:
                self.add_error("employee_id","Employee ID should be 8 digits!")
            return self.cleaned_data

        widgets ={

            'employee_name' : TextInput(
                attrs={'placeholder': 'Enter employee name'}
            ),

            'employee_id' : TextInput(
                attrs={'placeholder': 'Enter employee ID'}
            )
    
            }

