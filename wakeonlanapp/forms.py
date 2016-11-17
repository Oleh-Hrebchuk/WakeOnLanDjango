from django import forms


class WakeOnLan(forms.Form):
    computer_name = forms.CharField(max_length=30, required=False, help_text='Enter your ip or hostname')