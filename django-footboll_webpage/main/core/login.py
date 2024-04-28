from django import forms

class Login(forms.Form):
    email = forms.EmailField( required=True, max_length=100, widget=forms.TextInput(attrs={'style': '; padding-right: 60px; color: black;'}))
    password = forms.CharField( label = 'password', max_length=100, widget=forms.TextInput(attrs={'style': '; padding-right: 60px; color: black;'}))
    
 