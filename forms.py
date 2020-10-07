from django import forms


class AcronymSearchForm(forms.Form):
    search_term = forms.CharField(label='Search string', max_length=100)
