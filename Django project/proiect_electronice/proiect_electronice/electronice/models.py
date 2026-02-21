from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Produs(models.Model):
    STATUS_CHOICES = [
        ('disponibil', 'Disponibil'),
        ('indisponibil', 'Indisponibil'),
        ('precomanda', 'Precomanda'),
    ]#lista de tupluri: valoare stocata in db, valoare afisata in interfata
    
    id = models.AutoField(primary_key=True)
    nume = models.CharField(max_length=100)
    cod_produs = models.CharField(max_length=50, unique=True)
    #sir de caractere cu lungime fixa;index unique
    descriere = models.TextField(blank=True, null=True) 
    #tip de date pt text lung, fara limita car; validare pe server
    pret = models.DecimalField(max_digits=10, decimal_places=2)
    stoc = models.PositiveIntegerField(default=0)
    #daca nu se specifica, default 0
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='disponibil')
    data_adaugare = models.DateTimeField(auto_now_add=True)
    #automat data si ora doar la creare
    brand = models.ForeignKey('Brand', blank=True, null=True, on_delete=models.SET_NULL)
    #null controleaza db, blank formularele
    taguri = models.ManyToManyField('Tag', blank=True, related_name='produse')
    categorie = models.ForeignKey('Categorie', blank=True, null=True, related_name='produse', on_delete=models.SET_NULL)

    def __str__(self):
        return self.nume


class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    nume = models.CharField(max_length=60, unique=True)
    tara_origine = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    an_infiintare = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.nume


class Discount(models.Model):
    id = models.AutoField(primary_key=True)
    nume = models.CharField(max_length=50, default='Reducere')
    procent = models.PositiveIntegerField()
    data_start = models.DateField(blank=True, null=True)
    data_sfarsit = models.DateField(blank=True, null=True)
    activ = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nume} - {self.procent}%"


class Categorie(models.Model):
    id = models.AutoField(primary_key=True)
    nume = models.CharField(max_length=40, unique=True)
    descriere = models.TextField(blank=True, null=True)
    # Lab 4, Task QuerySets, Ex 5 - Culoare si icon pentru categorie
    culoare = models.CharField(max_length=7, default='#007bff')
    icon = models.CharField(max_length=50, default='●')
    discount = models.ForeignKey('Discount', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.nume


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    nume = models.CharField(max_length=50, unique=True)
    culoare_hex = models.CharField(max_length=7, default='#000000')

    def __str__(self):
        return self.nume


class Specificatie(models.Model):
    id = models.AutoField(primary_key=True)
    produs = models.ForeignKey(Produs, on_delete=models.CASCADE, related_name='specificatii')
    nume_atribut = models.CharField(max_length=100)
    valoare = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.produs.nume} - {self.nume_atribut}"



#extindere entitati si atribute
class DateClient(models.Model):
    # Lab 6, Task 1 - User Profile cu informatii despre utilizator
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_user = models.CharField(max_length=30, blank=True, null=True)
    vip = models.BooleanField(default=False)
    a_cumparat = models.BooleanField(default=False)
    data_inregistrarii = models.DateField(default=timezone.now)
    
    # Lab 6, Task 2 - 5 atribute aditionale pentru utilizator
    telefon = models.CharField(max_length=20, blank=True, null=True)
    tara = models.CharField(max_length=50, default='Romania')
    judet = models.CharField(max_length=50, blank=True, null=True)
    strada = models.CharField(max_length=100, blank=True, null=True)
    numar = models.CharField(max_length=10, blank=True, null=True)
    cod_postal = models.CharField(max_length=10, blank=True, null=True)
    
    # Lab 7, Task 1a - Cod confirmare email si status
    cod = models.CharField(max_length=100, blank=True, null=True)
    email_confirmat = models.BooleanField(default=False)
    
    #lab 8, task 4 - utilizator
    blocat = models.BooleanField(default=False)

    def __str__(self):
        return f"({self.user.id}) {self.user.username}"

    class Meta:
        permissions = [
            # Lab 8, Task 3.1 - Permisiune pentru vizualizare oferta speciala
            ("vizualizeaza_oferta", "Poate vizualiza oferta speciala cu reducere 50%"),
        ]


# Lab 6, Task 1 - Order (Comanda)
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'In asteptare'),
        ('processing', 'In procesare'),
        ('shipped', 'Expediat'),
        ('delivered', 'Livrat'),
        ('cancelled', 'Anulat'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    data_comanda = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_pret = models.DecimalField(max_digits=10, decimal_places=2)
    adresa_livrare = models.TextField()
    
    def __str__(self):
        return f"Comanda #{self.id} - {self.user.username}"
    
    class Meta:
        ordering = ['-data_comanda']


# Lab 6, Task 1 - OrderItem (Produse in comanda)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    produs = models.ForeignKey(Produs, on_delete=models.CASCADE)
    cantitate = models.IntegerField(default=1)
    pret_unitar = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.produs.nume} x{self.cantitate}"


# Lab 6, Task 1 - Rating (Evaluare produs)
class Rating(models.Model):
    RATING_CHOICES = [
        (1, '1 Stea'),
        (2, '2 Stele'),
        (3, '3 Stele'),
        (4, '4 Stele'),
        (5, '5 Stele'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    produs = models.ForeignKey(Produs, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField(choices=RATING_CHOICES)
    data_rating = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.produs.nume} ({self.rating}*)"
    
    class Meta:
        unique_together = ('user', 'produs')
        ordering = ['-data_rating']


# Lab 6, Task 1 - Review (Recenzie produs)
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    produs = models.ForeignKey(Produs, on_delete=models.CASCADE, related_name='reviews')
    titlu = models.CharField(max_length=100)
    text = models.TextField(max_length=1000)
    data_review = models.DateTimeField(auto_now_add=True)
    helpful_count = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username} - {self.produs.nume}"
    
    class Meta:
        ordering = ['-data_review']


# Lab 6, Task 1 - Favorite (Produse favorite)
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    produs = models.ForeignKey(Produs, on_delete=models.CASCADE, related_name='favorite_users')
    data_adaugare = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.produs.nume}"
    
    class Meta:
        unique_together = ('user', 'produs')
        ordering = ['-data_adaugare']


# Lab 7, Task 2.1 - Vizualizari (ultimele N produse vizualizate de utilizator)
class Vizualizare(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vizualizari')
    produs = models.ForeignKey(Produs, on_delete=models.CASCADE, related_name='vizualizari')
    data_vizualizare = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.produs.nume} ({self.data_vizualizare})"
    
    class Meta:
        ordering = ['-data_vizualizare']
    
    # Lab 7, Task 2.2 - Limita maxima de vizualizari per utilizator
    MAX_VIZUALIZARI = 5
    
    @classmethod
    def adauga_vizualizare(cls, user, produs):
        # Verifica daca exista deja vizualizare pentru acest produs
        vizualizare_existenta = cls.objects.filter(user=user, produs=produs).first()
        if vizualizare_existenta:
            # Actualizeaza data vizualizarii
            vizualizare_existenta.data_vizualizare = timezone.now()
            vizualizare_existenta.save()
            return vizualizare_existenta
        
        # Verifica daca s-a atins limita
        vizualizari_user = cls.objects.filter(user=user).order_by('-data_vizualizare')
        if vizualizari_user.count() >= cls.MAX_VIZUALIZARI:
            # Sterge cea mai veche vizualizare
            vizualizari_user.last().delete()
        
        # Adauga noua vizualizare
        return cls.objects.create(user=user, produs=produs)


# Lab 7, Task 2.3 - Promotii/Oferte
class Promotie(models.Model):
    nume = models.CharField(max_length=100)
    data_creare = models.DateTimeField(auto_now_add=True)
    data_expirare = models.DateTimeField()
    # Campuri aditionale
    descriere = models.TextField(blank=True, null=True)
    procent_reducere = models.PositiveIntegerField(default=10)
    categorii = models.ManyToManyField(Categorie, related_name='promotii')
    activa = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.nume} ({self.procent_reducere}%)"
    
    class Meta:
        ordering = ['-data_creare']
