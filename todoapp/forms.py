from django import forms

class TaskEditForm(forms.Form):
    updated_task_name = forms.CharField(max_length=1000)