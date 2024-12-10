from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Recensione

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = False  # Imposta il flag staff
        user.is_superuser = False  # Imposta il flag admin
        if commit:
            user.save()
        return user

    
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
class WaitlistForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Inserisci la tua email'}))