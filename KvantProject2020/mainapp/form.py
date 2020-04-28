from django import forms

class Filters(forms.Form):
     CHOICES = [('AMD', 'AMD'),
                ('Intel', 'Intel')]
     manufacturer = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)