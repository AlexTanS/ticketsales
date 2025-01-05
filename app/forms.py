from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Ticket, Client, Route


class RegisterUserForm(UserCreationForm):
    """Форма регистрации"""

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class BuyTicketClient(forms.ModelForm):
    """Форма покупки билета"""

    class Meta:
        model = Client
        fields = ["fio_f", "fio_i", "fio_o", "passport", "money"]
