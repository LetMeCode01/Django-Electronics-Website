from django import forms
from django.core.exceptions import ValidationError
from .validators import (
    validator_majorat,
    validator_numar_cuvinte,
    validator_lungime_cuvant,
    validator_fara_linkuri,
    validator_tip_mesaj_selectat,
    validator_cnp_cifre,
    validator_cnp_format,
    validator_email_temporar,
    validator_format_text,
    validator_majuscula_dupa_separator,
    validator_semnatura_in_mesaj, #ex 3
    validator_cnp_data_nasterii, 
    preproceseaza_varsta,  # ex 4
    preproceseaza_mesaj_spatii,  # 
    preproceseaza_majuscula_dupa_terminatori,  
    preproceseaza_urgent,  
    genereaza_cod_confirmare,   # lab 7, task 1b
)

# Lab 5, Task 2, Ex 1 - Formular contact cu validari
class ContactForm(forms.Form):
    # Lab 5, Task 2, Ex 1a - Nume (obligatoriu, max 10 caractere)
    # Lab 5, Task 2, Ex 2i + 2j - Validare format text + majuscula dupa separator
    nume = forms.CharField(
        max_length=10,
        required=True,
        label="Nume",
        validators=[validator_format_text, validator_majuscula_dupa_separator],
        widget=forms.TextInput(attrs={'placeholder': 'Introduceti numele'})
    )
    
    # Lab 5, Task 2, Ex 1b - Prenume (optional, max 10 caractere)
    # Lab 5, Task 2, Ex 2i + 2j - Validare format text + majuscula dupa separator (cu atentie la gol)
    prenume = forms.CharField(
        max_length=10,
        required=False,
        label="Prenume",
        validators=[validator_format_text, validator_majuscula_dupa_separator],
        widget=forms.TextInput(attrs={'placeholder': 'Introduceti prenumele (optional)'})
    )
    
    # Lab 5, Task 2, Ex 1c - CNP (optional, exact 13 caractere)
    # Lab 5, Task 2, Ex 2f + 2g - Validare CNP cifre + format valid
    cnp = forms.CharField(
        max_length=13,
        min_length=13,
        required=False,
        label="CNP",
        validators=[validator_cnp_cifre, validator_cnp_format],
        widget=forms.TextInput(attrs={'placeholder': 'Introduceti CNP (13 caractere, optional)'})
    )
    
    # Lab 5, Task 2, Ex 1d - Data nasterii (obligatoriu)
    # Lab 5, Task 2, Ex 2a - Validare majorat (peste 18 ani)
    data_nasterii = forms.DateField(
        required=True,
        label="Data nasterii",
        validators=[validator_majorat],
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    # Lab 5, Task 2, Ex 1e - Email (obligatoriu)
    # Lab 5, Task 2, Ex 2h - Validare email temporar
    email = forms.EmailField(
        required=True,
        label="E-mail",
        validators=[validator_email_temporar],
        widget=forms.EmailInput(attrs={'placeholder': 'Introduceti e-mail-ul'})
    )
    
    # Lab 5, Task 2, Ex 1f - Confirmare email (obligatoriu)
    confirmare_email = forms.EmailField(
        required=True,
        label="Confirmare e-mail",
        widget=forms.EmailInput(attrs={'placeholder': 'Confirmati e-mail-ul'})
    )
    
    # Lab 5, Task 2, Ex 1g - Tip mesaj (dropdown, implicit "neselectat")
    # Lab 5, Task 2, Ex 2e - Validare tip mesaj selectat
    TIP_MESAJ_CHOICES = [
        ('neselectat', 'Neselectat'),
        ('reclamatie', 'Reclamatie'),
        ('intrebare', 'Intrebare'),
        ('review', 'Review'),
        ('cerere', 'Cerere'),
        ('programare', 'Programare'),
    ]
    tip_mesaj = forms.ChoiceField(
        choices=TIP_MESAJ_CHOICES,
        required=True,
        initial='neselectat',
        label="Tip mesaj",
        validators=[validator_tip_mesaj_selectat],
        widget=forms.Select(attrs={'class': 'form-select'})
        #randam campul in html, generam tag <select>, adaugam atributul pe tagul html
    )
    
    # Lab 5, Task 2, Ex 1h - Subiect (obligatoriu, max 100 caractere)
    # Lab 5, Task 2, Ex 2i + 2d - Validare format text + fara linkuri
    subiect = forms.CharField(
        max_length=100,
        required=True,
        label="Subiect",
        validators=[validator_format_text, validator_fara_linkuri],
        widget=forms.TextInput(attrs={'placeholder': 'Introduceti subiectul (max 100 caractere)'})
    )
    
    # Lab 5, Task 2, Ex 1i - Minim zile asteptare (numar natural, obligatoriu)
    minim_zile_asteptare = forms.IntegerField(
        min_value=2,
        max_value=30,
        required=True,
        label="Minim zile asteptare",
        help_text="Pentru review-uri/cereri minimul de zile de asteptare trebuie setat de la 4 incolo iar pentru cereri/intrebari de la 2 incolo. Maximul este 30.",
        widget=forms.NumberInput(attrs={'min': '2', 'max': '30'})
    )
    
    # Lab 5, Task 2, Ex 1j - Mesaj (multiline, obligatoriu, cu semnatura)
    # Lab 5, Task 2, Ex 2b + 2c + 2d - Validare numar cuvinte + lungime cuvant + fara linkuri
    mesaj = forms.CharField(
        required=True,
        label="Mesaj (semnati-va in mesaj)",
        validators=[validator_numar_cuvinte, validator_lungime_cuvant, validator_fara_linkuri],
        widget=forms.Textarea(attrs={
            'rows': 6,
            'placeholder': 'Introduceti mesajul si semnati-va la final'
        })
    )
    
# Lab 5, Task 2, Ex 1f + 3 + 4 - Validari generale si preprocesari
    def clean(self):#metoda de validare generala pentru intregul formular; 
                    #se apeleaza dupa validarea campurilor individuale
        cleaned_data = super().clean()
        
        # Lab 5, Task 2, Ex 1f - Validare: emailurile trebuie sa coincida
        email = cleaned_data.get('email')
        confirmare_email = cleaned_data.get('confirmare_email')
        
        if email and confirmare_email and email != confirmare_email:
            raise ValidationError("E-mail-urile nu coincid. Va rugam sa reintroduceti.")
            #apare in from.non_field_errors in template
            
        # Lab 5, Task 2, Ex 3b - Validare: semnatura in mesaj (ultimul cuvant = numele)
        mesaj = cleaned_data.get('mesaj')
        nume = cleaned_data.get('nume')#obtinem valoarea procesata a campului
        
        if mesaj and nume:
            try:
                validator_semnatura_in_mesaj(mesaj, nume)
            except ValidationError as e:
                self.add_error('mesaj', e)#eroare specifica unui camp
        
        # Lab 5, Task 2, Ex 3c - Validare: zile asteptare in functie de tip mesaj
        tip_mesaj = cleaned_data.get('tip_mesaj')
        minim_zile = cleaned_data.get('minim_zile_asteptare')
        
        if tip_mesaj and minim_zile:
            if tip_mesaj in ['review', 'cerere'] and minim_zile < 4:
                self.add_error('minim_zile_asteptare', 
                    "Pentru review-uri si cereri, minimul de zile este 4.")
            if tip_mesaj in ['intrebare', 'reclamatie', 'programare'] and minim_zile < 2:
                self.add_error('minim_zile_asteptare',
                    "Pentru intrebari, reclamatii si programari, minimul de zile este 2.")
        
        # Lab 5, Task 2, Ex 3d - Validare: CNP corespunde cu data nasterii
        cnp = cleaned_data.get('cnp')
        data_nasterii = cleaned_data.get('data_nasterii')
        
        if cnp and data_nasterii:
            try:
                validator_cnp_data_nasterii(cnp, data_nasterii)
            except ValidationError as e:
                self.add_error('cnp', e)
        
        # Lab 5, Task 2, Ex 4a - Preproceseaza: inlocuieste data nasterii cu varsta
        if data_nasterii:
            cleaned_data['varsta'] = preproceseaza_varsta(data_nasterii)
            # Sterge data_nasterii din cleaned_data (nu o mai transmitem)
            cleaned_data.pop('data_nasterii', None)
        
        # Lab 5, Task 2, Ex 4b - Preproceseaza: elimina linii noi si compaseaza spatii
        if mesaj:
            mesaj = preproceseaza_mesaj_spatii(mesaj)
            cleaned_data['mesaj'] = mesaj
        
        # Lab 5, Task 2, Ex 4c - Preproceseaza: majuscula dupa terminatori de fraza
        if mesaj:
            mesaj = preproceseaza_majuscula_dupa_terminatori(mesaj)
            cleaned_data['mesaj'] = mesaj
        
        # Lab 5, Task 2, Ex 4d - Preproceseaza: seteaza urgent
        if tip_mesaj and minim_zile:
            urgent = preproceseaza_urgent(tip_mesaj, minim_zile)
            cleaned_data['urgent'] = urgent
        
        return cleaned_data
    



from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import DateClient
from .validators import validator_telefon, validator_cod_postal, validator_judet

# Lab 6, Task 2, Ex 3 - Formular inregistrare
class RegisterForm(UserCreationForm):#formular Django built-in pentru creare utilizator
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label="Prenume",
        widget=forms.TextInput(attrs={'placeholder': 'Prenume', 'class': 'form-control'})
    )
    
    last_name = forms.CharField(
        max_length=150,
        required=True,
        label="Nume",
        widget=forms.TextInput(attrs={'placeholder': 'Nume', 'class': 'form-control'})
    )
    
    email = forms.EmailField(
        required=True,
        label="E-mail",
        widget=forms.EmailInput(attrs={'placeholder': 'E-mail', 'class': 'form-control'})
    )
    
    # Lab 6, Task 2, Ex 3 - 5 campuri suplimentare cu validare pe 3
    # Validator 1: telefon
    telefon = forms.CharField(
        max_length=20,
        required=True,
        label="Telefon (10 cifre)",
        validators=[validator_telefon],
        widget=forms.TextInput(attrs={'placeholder': '0712345678', 'class': 'form-control'})
    )
    
    tara = forms.CharField(
        max_length=50,
        required=True,
        label="Tara",
        initial='Romania',
        widget=forms.TextInput(attrs={'placeholder': 'Romania', 'class': 'form-control'})
    )
    
    # Validator 2: judet
    judet = forms.CharField(
        max_length=50,
        required=True,
        label="Judet",
        validators=[validator_judet],
        widget=forms.TextInput(attrs={'placeholder': 'Bucuresti', 'class': 'form-control'})
    )
    
    strada = forms.CharField(
        max_length=100,
        required=True,
        label="Strada",
        widget=forms.TextInput(attrs={'placeholder': 'Str. Principala', 'class': 'form-control'})
    )
    
    # Validator 3: cod_postal
    cod_postal = forms.CharField(
        max_length=10,
        required=True,
        label="Cod Postal (5 cifre)",
        validators=[validator_cod_postal],
        widget=forms.TextInput(attrs={'placeholder': '10001', 'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'telefon', 'tara', 'judet', 'strada', 'cod_postal', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Parola'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirma parola'})
    
    def save(self, commit=True):
        # Lab 6, Task 2, Ex 3 - Salveaza user si creeaza DateClient
        user = super().save(commit=False)#creeaza obiectul User, dar nu il salveaza inca
        if commit:
            user.save()
            get_cod = genereaza_cod_confirmare()  # lab 7, task 1b
            DateClient.objects.create(#creeaza si salveaza inregistrarea in db
                user=user,
                telefon=self.cleaned_data['telefon'],
                tara=self.cleaned_data['tara'],
                judet=self.cleaned_data['judet'],
                strada=self.cleaned_data['strada'],
                cod_postal=self.cleaned_data['cod_postal'],
                cod=get_cod  # Lab 7, Task 1b 
            )
        return user
    


# Lab 6, Task 2, Ex 4 - Formular login personalizat
from django.contrib.auth.forms import AuthenticationForm
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
            'class': 'form-control'
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Parola',
            'class': 'form-control'
        })
    )
    
    # Lab 6, Task 2, Ex 4 - Checkbox "Tine-ma logat 1 zi"
    remember_me = forms.BooleanField(
        required=False,
        label="Tine-ma logat timp de o zi",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )


# Lab 6, Task 2, Ex 5 - Formular schimba parola
class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label="Parola veche",
        widget=forms.PasswordInput(attrs={'placeholder': 'Parola veche', 'class': 'form-control'})
    )
    
    new_password = forms.CharField(
        label="Parola noua",
        widget=forms.PasswordInput(attrs={'placeholder': 'Parola noua', 'class': 'form-control'})
    )
    
    confirm_password = forms.CharField(
        label="Confirma parola noua",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirma parola', 'class': 'form-control'})
    )
    
    def clean(self):
        # Lab 6, Task 2, Ex 5 - Validare: parole noi trebuie sa coincida
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if new_password and confirm_password and new_password != confirm_password:
            raise ValidationError("Parolele noi nu se potrivesc.")
        
        return cleaned_data


# Lab 7, Task 2.5 - Formular promotii
from .models import Categorie

class PromotieForm(forms.Form):
    subiect = forms.CharField(
        max_length=200,
        required=True,
        label="Subiect email",
        widget=forms.TextInput(attrs={'placeholder': 'Subiect email', 'class': 'form-control'})
    )
    
    mesaj = forms.CharField(
        required=True,
        label="Mesaj",
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Mesajul promotiei', 'class': 'form-control'})
    )
    
    nume_promotie = forms.CharField(
        max_length=100,
        required=True,
        label="Nume promotie",
        widget=forms.TextInput(attrs={'placeholder': 'Nume promotie', 'class': 'form-control'})
    )
    
    data_expirare = forms.DateTimeField(
        required=True,
        label="Data expirare",
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
    )
    
    procent_reducere = forms.IntegerField(
        min_value=1,
        max_value=90,
        required=True,
        label="Procent reducere (%)",
        widget=forms.NumberInput(attrs={'placeholder': '10', 'class': 'form-control'})
    )
    
    # Lab 7, Task 2.5 - Choice field multiplu cu categoriile (implicit toate selectate)
    categorii = forms.ModelMultipleChoiceField(
        queryset=Categorie.objects.all(),
        required=True,
        label="Categorii (selecteaza pentru care categorii se aplica promotia)",
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )
    
    # Lab 7, Task 2.6 - K minim vizualizari (K < N=5)
    minim_vizualizari = forms.IntegerField(
        min_value=1,
        max_value=4,
        required=True,
        initial=2,
        label="Minim vizualizari pentru a primi email (K < 5)",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )


# Lab 8, Task 2.3 - Formular pentru adaugare produs
from .models import Produs, Brand, Tag

class ProdusForm(forms.ModelForm): #ModelForm-form generat automat din model
    class Meta:
        model = Produs
        fields = ['nume', 'cod_produs', 'descriere', 'pret', 'stoc', 'status', 'brand', 'categorie', 'taguri']
        widgets = {
            'nume': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nume produs'}),
            'cod_produs': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cod produs'}),
            'descriere': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'pret': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stoc': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'brand': forms.Select(attrs={'class': 'form-control'}),
            'categorie': forms.Select(attrs={'class': 'form-control'}),
            'taguri': forms.CheckboxSelectMultiple(),
        }