from django.urls import path
from . import views

app_name = 'electronice'#format permisiune, pentru Lab 8, Task 2.3 - Verifica daca userul are permisiunea de a adauga produse

urlpatterns = [
    # Lab 4, Task QuerySets, Ex 1 - Ruta pagina produse cu paginare
    path('produse/', views.produs_list, name='produs_list'),
    
    # Lab 4, Task QuerySets, Ex 2 - Ruta pagina detalii produs
    path('produse/<int:pk>/', views.produs_detail, name='produs_detail'),#<path converter>
    #capteaza un numar intreg din URL si il trimite ca argument
    
    # Lab 4, Task QuerySets, Ex 4 - Ruta pagina categorie
    path('categorii/<slug:slug>/', views.categorie_detail, name='categorie_detail'),
    #slug: capteaza un string format din litere, cifre, cratime si underscore
    
    # Lab 5, Task 2, Ex 1 - Ruta pagina contact
    path('contact/', views.contact, name='contact'),
    
    # Lab 6, Task 2, Ex 3 - Register
    path('register/', views.register, name='register'),
    
    # Lab 6, Task 2, Ex 4 - Login/Logout
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Lab 6, Task 2, Ex 5 - Profil si schimba parola
    path('profil/', views.profil, name='profil'),
    path('change-password/', views.change_password, name='change_password'),
    
    # Lab 7, Task 1e - Confirmare email
    path('confirma_mail/<str:cod>/', views.confirma_mail, name='confirma_mail'),
    
    # Lab 7, Task 2.5 - Pagina promotii
    path('promotii/', views.promotii, name='promotii'),
    
    # Lab 8, Task 1 - Ruta de test pentru pagina 403
    path('interzis/', views.pagina_interzisa, name='interzis'),
    
    # Lab 8, Task 2.3 - Ruta pentru adaugare produs (protejata)
    path('adauga-produs/', views.adauga_produs, name='adauga_produs'),
    
    # Lab 8, Task 2.4 - Rute pentru log si info (doar Administratori_site)
    path('log/', views.pagina_log, name='log'),
    path('info/', views.pagina_info, name='info'),
    
    # Lab 8, Task 3 - Rute pentru oferta speciala
    path('activeaza-oferta/', views.activeaza_oferta, name='activeaza_oferta'),
    path('oferta/', views.pagina_oferta, name='oferta'),
]