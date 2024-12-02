from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Recensione

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cognome'}))

    class Meta:  # Corretto il nome della classe Meta
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')
        widgets = {
            'username': forms.HiddenInput(),  # Nascondi il campo username
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Conferma Password'}),
        }

    
class RegistrazioneForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Password'
        })
    )

class RecensioneForm(forms.ModelForm):
    class Meta:
        model = Recensione
        fields = ['nome', 'commento', 'voto']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Il tuo nome', 'required': 'required',}),
            'commento': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Scrivi il tuo commento'}),
            'voto': forms.Select(attrs={'class': 'form-control'}, choices=[(i, f"{i} - {descr}") for i, descr in enumerate(
                ["Pessimo", "Scarso", "Sufficiente", "Buono", "Eccellente"], 1)]),
        }