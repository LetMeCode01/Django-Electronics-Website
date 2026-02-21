from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Produs, Categorie, Vizualizare, Promotie
from .forms import ContactForm
from django.contrib.auth.models import User  # Lab 8, Task 2
from django.contrib.auth.decorators import login_required  # Lab 8, Task 2

from django.core.mail import send_mail, mail_admins  # Lab 7, Task 1c + Task 3
from django.template.loader import render_to_string

import os #ex 5
import json
import time
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta
import logging  # Lab 7, Task 4

from decimal import Decimal #Lab 8 task 3

# Lab 7, Task 4 - Logger pentru aplicatie
logger = logging.getLogger('django')

# Lab 7, Task 3a - Dictionar pentru tracking incercari de login esuate
# Format: {ip: [(timestamp1, username1), (timestamp2, username2), ...]}
incercari_login_esuate = {}


# Lab 8, Task 1 - View pentru pagina de eroare 403
def eroare_403_view(request, exception=None, titlu='', mesaj_personalizat=''):
    # Lab 8, Task 1e - Contorizeaza accesarile 403 in sesiune
    if 'numar_accesari_403' not in request.session:
        request.session['numar_accesari_403'] = 0
    request.session['numar_accesari_403'] += 1
    
    context = {
        'titlu': titlu,
        'mesaj_personalizat': mesaj_personalizat,
        'numar_accesari_403': request.session['numar_accesari_403'],
        'n_max_403': settings.N_MAX_403,
    }
    
    return render(request, 'eroare403.html', context, status=403)


# Lab 8, Task 1 - Ruta de test /interzis pentru a ajunge la pagina 403
def pagina_interzisa(request):
    return eroare_403_view(
        request, 
        titlu='Acces Interzis', 
        mesaj_personalizat='Aceasta pagina este interzisa pentru testare.'
    )


# Lab 8, Task 2.3 - View pentru adaugare produse (protejat cu permisiuni)
from .forms import ProdusForm

@login_required(login_url='electronice:login')
def adauga_produs(request):
    # Lab 8, Task 2.3 - Verifica daca userul are permisiunea de a adauga produse
    if not request.user.has_perm('electronice.add_produs'):#daca are permisiunea userul, returneaza un bool
        # Obtine categoriile pentru mesajul personalizat
        categorii = Categorie.objects.all()
        tip_produse = ', '.join([c.nume for c in categorii]) if categorii else 'produse electronice'
        
        return eroare_403_view(
            request,
            titlu='Eroare adaugare produse',
            mesaj_personalizat=f'Nu ai voie sa adaugi {tip_produse}.'
        )
    
    if request.method == 'POST':
        form = ProdusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('electronice:produs_list')
    else:
        form = ProdusForm()
    
    return render(request, 'adauga_produs.html', {'form': form})


# Lab 8, Task 2.4/2.5 - Pagina /log (doar pentru Administratori_site)
@login_required(login_url='electronice:login')
def pagina_log(request):
    # Verifica daca userul e in grupul Administratori_site
    if not request.user.groups.filter(name='Administratori_site').exists() and not request.user.is_superuser:
        return eroare_403_view(
            request,
            titlu='Acces Interzis',
            mesaj_personalizat='Nu ai permisiunea de a accesa paginile de log.'
        )
    
    # Citeste fisierele de log
    logs = {}
    log_files = ['debug.log', 'info.log', 'warning.log', 'error.log', 'critical.log']
    logs_dir = os.path.join(settings.BASE_DIR, 'logs')
    
    for log_file in log_files:
        log_path = os.path.join(logs_dir, log_file)
        if os.path.exists(log_path):
            with open(log_path, 'r', encoding='utf-8') as f:
                # Citeste ultimele 50 linii
                lines = f.readlines()[-50:]
                logs[log_file] = ''.join(lines)
        else:
            logs[log_file] = 'Fisierul nu exista.'
    
    return render(request, 'log.html', {'logs': logs})


# Lab 8, Task 2.4/2.5 - Pagina /info (doar pentru Administratori_site)
@login_required(login_url='electronice:login')
def pagina_info(request):
    # Verifica daca userul e in grupul Administratori_site
    if not request.user.groups.filter(name='Administratori_site').exists() and not request.user.is_superuser:
        return eroare_403_view(
            request,
            titlu='Acces Interzis',
            mesaj_personalizat='Nu ai permisiunea de a accesa paginile de informatii.'
        )
    
    # Informatii despre sistem
    import django
    import sys
    
    info = {
        'django_version': django.get_version(),
        'python_version': sys.version,
        'debug_mode': settings.DEBUG,
        'database': settings.DATABASES['default']['ENGINE'],
        'installed_apps': settings.INSTALLED_APPS,
        'numar_produse': Produs.objects.count(),
        'numar_categorii': Categorie.objects.count(),
        'numar_utilizatori': User.objects.count(),
    }
    
    return render(request, 'info.html', {'info': info})


# Lab 5, Task 2, Ex 1 + 4 + 5 - Pagina contact cu formular, preproceseari si salvare JSON
def contact(request):
    if request.method == 'POST':#verifica cerere submit formular
        form = ContactForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data#dictionar cu datele valide si preprocesate
            
            # Lab 5, Task 2, Ex 5 - Calculeaza timestamp
            timestamp = int(time.time())
            
            # Lab 5, Task 2, Ex 4d - Genereaza nume fisier cu "urgent" daca e cazul
            urgent_text = "_urgent" if cleaned_data.get('urgent') else ""
            nume_fisier = f"mesaj_{timestamp}{urgent_text}.json"
            
            # Lab 5, Task 2, Ex 5 - creeare directorul Mesaje daca nu exista
            cale_mesaje = os.path.join(settings.BASE_DIR, 'Mesaje')
            os.makedirs(cale_mesaje, exist_ok=True)
            
            # Lab 5, Task 2, Ex 5 - pregatim datele pentru JSON
            data_curenta = timezone.now()
            ip_utilizator = get_client_ip(request)
            
            mesaj_data = {
                'timestamp': timestamp,
                'data_ora': data_curenta.strftime('%d.%m.%Y %H:%M:%S'),
                'ip_utilizator': ip_utilizator,
                'nume': cleaned_data['nume'],
                'prenume': cleaned_data.get('prenume', ''),
                'cnp': cleaned_data.get('cnp', ''),
                'varsta': cleaned_data.get('varsta', ''),
                'email': cleaned_data['email'],
                'tip_mesaj': cleaned_data['tip_mesaj'],
                'subiect': cleaned_data['subiect'],
                'minim_zile_asteptare': cleaned_data['minim_zile_asteptare'],
                'mesaj': cleaned_data['mesaj'],
                'urgent': cleaned_data.get('urgent', False),
            }
            
            # Lab 5, Task 2, Ex 5 - salvam fisierul JSON
            cale_fisier = os.path.join(cale_mesaje, nume_fisier)
            with open(cale_fisier, 'w', encoding='utf-8') as f:
                json.dump(mesaj_data, f, indent=4, ensure_ascii=False)
                #serializeaza obiect python in fisier JSON
            
            # Lab 7, Task 4 - INFO: Mesaj contact salvat
            logger.info(f'Mesaj contact salvat: {nume_fisier} de la {cleaned_data["email"]}')
            
            return render(request, 'contact_success.html', {
                'nume': cleaned_data['nume'],
                'email': cleaned_data['email'],
                'tip_mesaj': cleaned_data['tip_mesaj'],
                'varsta': cleaned_data.get('varsta'),
                'urgent': cleaned_data.get('urgent'),
                'nume_fisier': nume_fisier,
            })
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})

# Lab 5, Task 2, Ex 5 -extragem IP-ul utilizatorului
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# Lab 4, Task QuerySets, Ex 1 - Pagina cu toate produsele + paginare
def produs_list(request):
    # Lab 7, Task 4 - DEBUG: Acces pagina produse
    logger.debug(f'Acces pagina produse - IP: {get_client_ip(request)}, User: {request.user}')
    
    #returneaza QuerySet cu toate obiectele din Produs
    produse = Produs.objects.all()
    
    # Lab 4, Task QuerySets, Ex 3 - Sortare ascendenta/descendenta
    sort = request.GET.get('sort', 'd')
    if sort == 'a':
        produse = produse.order_by('pret')
    else:
        produse = produse.order_by('-pret')
    
    # Lab 4, Task QuerySets, Ex 1 - Paginare 5 produse pe pagina
    paginator = Paginator(produse, 5)
    #imparte queryset in pagini de cate 5 produse
    page_number = request.GET.get('page')
    #extrage parametru page din URL (ex: ?page=2)
    page_obj = paginator.get_page(page_number)
    #returneaza valoarea
    
    context = {
        'page_obj': page_obj,
        'produse': page_obj.object_list,
        'sort': sort,
    }
    return render(request, 'produs_list.html', context)

# Lab 4, Task QuerySets, Ex 2 - Pagina detalii produs + eroare 404
# Lab 7, Task 2.1/2.2 - Inregistrare vizualizare produs
# Lab 7, Task 3c - Try-except cu mail_admins pentru erori
def produs_detail(request, pk):
    try:
        produs = get_object_or_404(Produs, pk=pk)
        #cauta obiectul cu Model=Produs si pk=pk; daca nu exista, returneaza eroare 404
        
        # Lab 7, Task 2.1/2.2 - Adauga vizualizare daca utilizatorul e autentificat
        if request.user.is_authenticated:
            Vizualizare.adauga_vizualizare(request.user, produs)
        
        context = {
            'produs': produs,
        }
        return render(request, 'produs_detail.html', context)
    
    except Exception as e:
        # Lab 7, Task 3c - Trimite mail catre admini in caz de eroare
        import traceback
        ip_utilizator = get_client_ip(request)
        # Lab 7, Task 4 - CRITICAL: Eroare in view produs_detail
        logger.critical(f'Eroare critica in produs_detail pentru ID {pk}: {str(e)}')
        mail_admins(
            subject=f'EROARE in produs_detail - Produs ID: {pk}',
            message=f'A aparut o eroare in view-ul produs_detail.\n\n'
                    f'Produs ID solicitat: {pk}\n'
                    f'IP utilizator: {ip_utilizator}\n'
                    f'Utilizator: {request.user}\n'
                    f'Data/ora: {timezone.now().strftime("%d.%m.%Y %H:%M:%S")}\n\n'
                    f'Eroare: {str(e)}\n\n'
                    f'Traceback:\n{traceback.format_exc()}',
            fail_silently=True
        )
        # Arunca eroarea mai departe pentru a afisa pagina 404/500
        raise

# Lab 4, Task QuerySets, Ex 4 - Pagina categorie + filtrare produse
def categorie_detail(request, slug):
    # Lab 7, Task 4 - DEBUG: Acces pagina categorie
    logger.debug(f'Acces categorie: {slug} - IP: {get_client_ip(request)}')
    
    categorie = get_object_or_404(Categorie, nume__iexact=slug)#comparatoe case-insensitive
    produse = Produs.objects.filter(categorie=categorie)
    #paginare si sortare
    
    # Lab 4, Task QuerySets, Ex 3 - Sortare pentru categorie
    sort = request.GET.get('sort', 'd')#default descrescator
    if sort == 'a':
        produse = produse.order_by('pret')
    else:
        produse = produse.order_by('-pret')
    
    # Lab 4, Task QuerySets, Ex 1 - Paginare
    paginator = Paginator(produse, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'categorie': categorie,
        'page_obj': page_obj,
        'produse': page_obj.object_list,
        'sort': sort,
    }
    return render(request, 'categorie_detail.html', context)

# Lab 4, Task QuerySets, Ex 4 - Functie pentru meniu dinamic cu categorii
def get_categorii(request):
    categorii = Categorie.objects.all()
    return {'categorii': categorii}




from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm, ChangePasswordForm
from .models import DateClient

'''
# Lab 6, Task 2, Ex 3 - Register
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('electronice:profil')
    else:
        form = RegisterForm()
    
    return render(request, 'register.html', {'form': form})
'''

# Lab 7, Task 1c - Register cu trimitere mail de confirmare
# Lab 7, Task 3b - Blocare username "admin"
def register(request):
    eroare_admin = None  # Lab 7, Task 3b - Eroare pentru username admin
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        
        # Lab 7, Task 3b - Verifica daca username-ul e "admin"
        username = request.POST.get('username', '').lower()
        if username == 'admin':
            # Lab 7, Task 3b - Trimite alerta catre admini
            ip_utilizator = get_client_ip(request)
            # Lab 7, Task 4 - ERROR: Incercare inregistrare cu username admin
            logger.error(f'Incercare inregistrare cu username "admin" de la IP {ip_utilizator}')
            mail_admins(
                subject='ALERTA SECURITATE: Incercare inregistrare cu username "admin"',
                message=f'S-a incercat inregistrarea cu username-ul "admin".\n'
                        f'IP: {ip_utilizator}\n'
                        f'Data/ora: {timezone.now().strftime("%d.%m.%Y %H:%M:%S")}\n'
                        f'Email furnizat: {request.POST.get("email", "N/A")}',
                fail_silently=True
            )
            eroare_admin = 'Username-ul "admin" nu este permis.'
            return render(request, 'register.html', {'form': form, 'eroare_admin': eroare_admin})
        
        if form.is_valid():
            user = form.save()
            date_client = DateClient.objects.get(user=user)
            
            # Lab 7, Task 1c - Trimite mail de confirmare
            subject = 'Confirma adresa de e-mail - Electronice'
            context = {
                'nume': user.last_name,
                'prenume': user.first_name,
                'username': user.username,
                'cod': date_client.cod,
                'link_confirmare': f"http://127.0.0.1:8000/electronice/confirma_mail/{date_client.cod}/"
            }
            message = render_to_string('email_confirmare.txt', context)
            send_mail(subject, message, 'noreply@electronice.com', [user.email])
            
            # Lab 7, Task 4 - INFO: Utilizator inregistrat cu succes
            logger.info(f'Utilizator nou inregistrat: {user.username} (email: {user.email})')
            
            return render(request, 'register_success.html', {
                'mesaj': 'Verifica e-mailul pentru a confirma inregistrarea.'
            })
    else:
        form = RegisterForm()
    
    return render(request, 'register.html', {'form': form, 'eroare_admin': eroare_admin})

# Lab 7, Task 1e - Confirma email prin cod
def confirma_mail(request, cod): #<str:cod> din templates->path converter care capteaza codul din url si il trimite ca argument
    try:
        date_client = DateClient.objects.get(cod=cod)#cauta in DB inregistrarea cu acel cod
        date_client.email_confirmat = True
        date_client.save()
        
        return render(request, 'email_confirmat.html', {
            'succes': True,
            'mesaj': 'E-mailul a fost confirmat cu succes!'
        })
    except DateClient.DoesNotExist:
        # Lab 7, Task 4 - WARNING: Cod confirmare invalid
        logger.warning(f'Incercare confirmare email cu cod invalid: {cod}')
        return render(request, 'email_confirmat.html', {
            'succes': False,
            'mesaj': 'Cod de confirmare invalid.'
        })


# Lab 7, Task 1f, 1g - Login cu verificare email confirmat
# Lab 7, Task 3a - Tracking incercari login esuate
def login_view(request):
    global incercari_login_esuate
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        ip_utilizator = get_client_ip(request)
        username_incercat = request.POST.get('username', '')
        
        
        if form.is_valid():
            user = form.get_user()
            
            #Lab 8, task 4 - verificare blocare cont
            try:
                date_client = DateClient.objects.get(user=user)
                if date_client.blocat:
                    return render(request, 'login.html', {
                        'form': form,
                        'eroare': 'Contul tau a fost blocat de un moderator.'
                    })
            except DateClient.DoesNotExist:
                pass
            
            # Lab 7, Task 1f - Verifica daca email e confirmat
            try:
                date_client = DateClient.objects.get(user=user)
                if not date_client.email_confirmat:
                    # Lab 7, Task 4 - WARNING: Incercare login cu email neconfirmat
                    logger.warning(f'Incercare login cu email neconfirmat: {user.username} de la IP {ip_utilizator}')
                    return render(request, 'login.html', {
                        'form': form,
                        'eroare': 'Trebuie sa confirmati e-mailul inainte de a va loga.'
                    })
            except DateClient.DoesNotExist:
                pass
            
            # Lab 7, Task 3a - Login reusit, sterge istoricul de incercari pentru acest IP
            if ip_utilizator in incercari_login_esuate:
                del incercari_login_esuate[ip_utilizator]
            
            login(request, user)
            
            # Lab 7, Task 4 - INFO: Login reusit
            logger.info(f'Login reusit pentru utilizatorul: {user.username} de la IP {ip_utilizator}')
            
            if form.cleaned_data.get('remember_me'):
                request.session.set_expiry(86400)
            else:
                request.session.set_expiry(0)
            
            return redirect('electronice:profil')
        else:
            # Lab 7, Task 3a - Login esuat, inregistreaza incercarea
            acum = datetime.now()
            
            # Initializeaza lista pentru IP daca nu exista
            if ip_utilizator not in incercari_login_esuate:
                incercari_login_esuate[ip_utilizator] = []
            
            # Adauga incercarea curenta
            incercari_login_esuate[ip_utilizator].append((acum, username_incercat))
            
            # Filtreaza incercarile din ultimele 2 minute
            limita_timp = acum - timedelta(minutes=2)
            incercari_login_esuate[ip_utilizator] = [
                (t, u) for t, u in incercari_login_esuate[ip_utilizator]
                if t > limita_timp
            ]
            
            # Lab 7, Task 3a - Daca sunt 3+ incercari esuate in 2 minute, trimite mail_admins
            if len(incercari_login_esuate[ip_utilizator]) >= 3:
                usernames_incercate = [u for t, u in incercari_login_esuate[ip_utilizator]]
                # Lab 7, Task 4 - ERROR: Multiple incercari login esuate (posibil atac brute-force)
                logger.error(f'Posibil atac brute-force de la IP {ip_utilizator}. Usernames: {usernames_incercate}')
                mail_admins(
                    subject='ALERTA SECURITATE: Multiple incercari de login esuate',
                    message=f'S-au detectat {len(incercari_login_esuate[ip_utilizator])} incercari de login esuate in ultimele 2 minute.\n'
                            f'IP: {ip_utilizator}\n'
                            f'Data/ora: {acum.strftime("%d.%m.%Y %H:%M:%S")}\n'
                            f'Usernames incercate: {usernames_incercate}',
                    fail_silently=True
                )
                # Goleste lista dupa trimiterea alertei pentru a nu trimite spam
                incercari_login_esuate[ip_utilizator] = []
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

'''
# Lab 6, Task 2, Ex 4 - Login personalizat
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Lab 6, Task 2, Ex 4 - Daca e bifat "Tine-ma logat", seteaza sesiune 1 zi
            if form.cleaned_data.get('remember_me'):
                request.session.set_expiry(86400)  # 1 zi = 86400 secunde
            else:
                request.session.set_expiry(0)  # Sesiune temporara (inchide browser = logout)
            
            return redirect('electronice:profil')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})
'''

# Lab 6, Task 2, Ex 4 - Logout
# Lab 8, Task 3.4 - La logout se sterge permisiunea vizualizeaza_oferta
def logout_view(request):
    # Lab 8, Task 3.4 - Sterge permisiunea vizualizeaza_oferta inainte de logout
    if request.user.is_authenticated:
        from django.contrib.auth.models import Permission
        try:
            perm = Permission.objects.get(codename='vizualizeaza_oferta')
            request.user.user_permissions.remove(perm)
        except Permission.DoesNotExist:
            pass
    
    logout(request)
    return redirect('electronice:index')


# Lab 8, Task 3.3 - View pentru activare oferta (cand userul da click pe banner)
@login_required(login_url='electronice:login')
def activeaza_oferta(request):
    from django.contrib.auth.models import Permission
    
    # Adauga permisiunea vizualizeaza_oferta utilizatorului
    try:
        perm = Permission.objects.get(codename='vizualizeaza_oferta')
        request.user.user_permissions.add(perm)
    except Permission.DoesNotExist:
        pass
    
    return redirect('electronice:oferta')


# Lab 8, Task 3.5 - Pagina oferta (doar pentru cei cu permisiune)
@login_required(login_url='electronice:login')
def pagina_oferta(request):
    # Verifica daca userul are permisiunea vizualizeaza_oferta
    if not request.user.has_perm('electronice.vizualizeaza_oferta'):
        return eroare_403_view(
            request,
            titlu='Eroare afisare oferta',
            mesaj_personalizat='Nu ai voie sa vizualizezi oferta.'
        )
    
    # Lista cu produse in oferta (exemplu: toate produsele cu reducere)
    produse_oferta = Produs.objects.all()[:5]  # Primele 5 produse ca exemplu
    produse_si_preturi = [(produs, round(produs.pret * Decimal('0.5'), 2)) for produs in produse_oferta]
    return render(request, 'oferte.html', {
        'produse_si_preturi': produse_si_preturi,
        'reducere': 50
    })


# Lab 6, Task 2, Ex 5 - Pagina profil
@login_required(login_url='electronice:login')
def profil(request):
    user = request.user
    
    # Gestioneaza cazul cand utilizatorul nu are DateClient (ex: superuser)
    try:
        date_client = DateClient.objects.get(user=user)
    except DateClient.DoesNotExist:
        date_client = None
    
    context = {
        'user': user,
        'date_client': date_client,
    }
    
    return render(request, 'profil.html', context)


# Lab 6, Task 2, Ex 5 - Schimba parola
@login_required(login_url='electronice:login')
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = request.user
            
            # Lab 6, Task 2, Ex 5 - Verifica parola veche
            if not user.check_password(form.cleaned_data['old_password']):
                form.add_error('old_password', 'Parola veche nu e corecta.')
            else:
                # Lab 6, Task 2, Ex 5 - Seteaza parola noua
                user.set_password(form.cleaned_data['new_password'])
                user.save()
                
                # Lab 6, Task 2, Ex 5 - Re-login cu parola noua
                login(request, user)
                return redirect('electronice:profil')
    else:
        form = ChangePasswordForm()
    
    return render(request, 'change_password.html', {'form': form})


# Lab 7, Task 2.5/2.6/2.7 - Pagina promotii cu formular si trimitere email-uri
from django.core.mail import send_mass_mail
from .forms import PromotieForm
from django.db.models import Count

def promotii(request):
    succes = False
    nume_promotie = ''
    nr_emailuri = 0
    
    if request.method == 'POST':
        form = PromotieForm(request.POST)
        if form.is_valid():
            # Lab 7, Task 2.6 - Salveaza promotia in baza de date
            promotie = Promotie.objects.create(
                nume=form.cleaned_data['nume_promotie'],
                data_expirare=form.cleaned_data['data_expirare'],
                descriere=form.cleaned_data['mesaj'],
                procent_reducere=form.cleaned_data['procent_reducere']
            )
            promotie.categorii.set(form.cleaned_data['categorii'])
            
            # Lab 7, Task 2.6 - Gaseste utilizatorii cu minim K vizualizari pentru categoriile selectate
            categorii_selectate = form.cleaned_data['categorii']
            minim_k = form.cleaned_data['minim_vizualizari']
            
            # Lab 7, Task 2.7 - Grupeaza email-urile pe categorii
            emailuri_de_trimis = []
            
            for categorie in categorii_selectate:
                # Gaseste utilizatorii care au vizualizat minim K produse din aceasta categorie
                utilizatori = Vizualizare.objects.filter(
                    produs__categorie=categorie
                ).values('user').annotate(
                    nr_vizualizari=Count('id')
                ).filter(nr_vizualizari__gte=minim_k)
                
                # Selecteaza template-ul pentru categorie
                template_name = f'promotie_email_{categorie.nume.lower()}.txt'
                try:
                    template_content = render_to_string(template_name, {
                        'subiect': form.cleaned_data['subiect'],
                        'nume_promotie': form.cleaned_data['nume_promotie'],
                        'procent_reducere': form.cleaned_data['procent_reducere'],
                        'data_expirare': form.cleaned_data['data_expirare'].strftime('%d.%m.%Y %H:%M'),
                        'mesaj': form.cleaned_data['mesaj'],
                        'categorie': categorie.nume,
                        'username': ''  # placeholder
                    })
                except:
                    # Foloseste template-ul default daca nu exista unul specific
                    template_name = 'promotie_email_default.txt'
                
                # Pregateste emailurile pentru fiecare utilizator
                from django.contrib.auth.models import User
                for viz in utilizatori:
                    user = User.objects.get(id=viz['user'])
                    if user.email:
                        mesaj_email = render_to_string(template_name, {
                            'subiect': form.cleaned_data['subiect'],
                            'nume_promotie': form.cleaned_data['nume_promotie'],
                            'procent_reducere': form.cleaned_data['procent_reducere'],
                            'data_expirare': form.cleaned_data['data_expirare'].strftime('%d.%m.%Y %H:%M'),
                            'mesaj': form.cleaned_data['mesaj'],
                            'categorie': categorie.nume,
                            'username': user.username
                        })
                        emailuri_de_trimis.append((
                            form.cleaned_data['subiect'],
                            mesaj_email,
                            'noreply@electronice.com',
                            [user.email]
                        ))
            
            # Lab 7, Task 2.7 - Trimite toate emailurile cu send_mass_mail
            if emailuri_de_trimis:
                try:
                    send_mass_mail(emailuri_de_trimis, fail_silently=False)
                except Exception as e:
                    # Lab 7, Task 4 - CRITICAL: Eroare la trimitere emailuri promotie
                    logger.critical(f'Eroare critica la trimitere emailuri promotie "{form.cleaned_data["nume_promotie"]}": {str(e)}')
            
            succes = True
            nume_promotie = form.cleaned_data['nume_promotie']
            nr_emailuri = len(emailuri_de_trimis)
            
            # Reseteaza formularul
            form = PromotieForm(initial={'categorii': Categorie.objects.all()})
    else:
        # Lab 7, Task 2.5 - Implicit toate categoriile selectate
        form = PromotieForm(initial={'categorii': Categorie.objects.all()})
    
    return render(request, 'promotii.html', {
        'form': form,
        'succes': succes,
        'nume_promotie': nume_promotie,
        'nr_emailuri': nr_emailuri
    })