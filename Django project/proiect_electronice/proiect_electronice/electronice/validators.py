from django.core.exceptions import ValidationError
from datetime import date
import re

import secrets #lab 7, task 1B
import string

# Lab 5, Task 2, Ex 2a - Validator: expeditorul trebuie sa fie major (peste 18 ani)
def validator_majorat(data_nasterii):
    today = date.today()
    age = today.year - data_nasterii.year - ((today.month, today.day) < (data_nasterii.month, data_nasterii.day))
    if age < 18:
        raise ValidationError("Trebuie sa fiti major (peste 18 ani) pentru a trimite mesaj.")

# Lab 5, Task 2, Ex 2b - Validator: mesaj cu 5-100 cuvinte
def validator_numar_cuvinte(mesaj):
    cuvinte = re.findall(r'\w+', mesaj)
    if len(cuvinte) < 5:
        raise ValidationError("Mesajul trebuie sa contina minim 5 cuvinte.")
    if len(cuvinte) > 100:
        raise ValidationError("Mesajul trebuie sa contina maxim 100 cuvinte.")

# Lab 5, Task 2, Ex 2c - Validator: lungime cuvant maxim 15 caractere
def validator_lungime_cuvant(mesaj):
    cuvinte = re.findall(r'\w+', mesaj)
    for cuvant in cuvinte:
        if len(cuvant) > 15:
            raise ValidationError(f"Cuvantul '{cuvant}' depaseste 15 caractere. Maxim 15 caractere pe cuvant.")

# Lab 5, Task 2, Ex 2d - Validator: fara linkuri in mesaj si subiect
def validator_fara_linkuri(text):
    if 'http://' in text or 'https://' in text:
        raise ValidationError("Mesajul/subiectul nu poate contine linkuri (http:// sau https://).")

# Lab 5, Task 2, Ex 2e - Validator: tip mesaj nu trebuie neselectat
def validator_tip_mesaj_selectat(tip):
    if tip == 'neselectat':
        raise ValidationError("Trebuie sa selectati un tip de mesaj valid.")

# Lab 5, Task 2, Ex 2f - Validator: CNP doar cifre
def validator_cnp_cifre(cnp):
    if cnp and not cnp.isdigit():
        raise ValidationError("CNP-ul trebuie sa contina doar cifre.")

# Lab 5, Task 2, Ex 2g - Validator: CNP format valid (incepe cu 1/2/5/6 + 6 cifre data valida)
def validator_cnp_format(cnp):
    if not cnp:
        return
    
    if cnp[0] not in ['1', '2', '5', '6']:
        raise ValidationError("CNP-ul trebuie sa inceapa cu 1, 2, 5 sau 6.")
    
    # Extrage data: pozitiile 1-6 sunt AAMMDD
    an = cnp[1:3]
    luna = cnp[3:5]
    zi = cnp[5:7]
    
    try:
        luna_int = int(luna)
        zi_int = int(zi)
        
        if not (1 <= luna_int <= 12):
            raise ValidationError("CNP-ul contine o luna invalida (01-12).")
        if not (1 <= zi_int <= 31):
            raise ValidationError("CNP-ul contine o zi invalida (01-31).")
    except ValueError:
        raise ValidationError("CNP-ul contine date invalide.")

# Lab 5, Task 2, Ex 2h - Validator: email nu e temporar
def validator_email_temporar(email):
    domenii_temporare = ['guerrillamail.com', 'yopmail.com']
    for domeniu in domenii_temporare:
        if email.endswith(domeniu):
            raise ValidationError(f"Email-urile de la {domeniu} nu sunt acceptate.")

# Lab 5, Task 2, Ex 2i - Validator: text incepe cu litera mare, doar spatii/cratima/litere
def validator_format_text(text):
    if not text:
        return
    
    # Verifica daca incepe cu litera mare
    if not text[0].isupper():
        raise ValidationError("Textul trebuie sa inceapa cu litera mare.")
    
    # Verifica daca contine doar litere, spatii si cratima
    if not re.match(r'^[a-zA-Z\s\-]+$', text):
        raise ValidationError("Textul poate contine doar litere, spatii si cratima.")

# Lab 5, Task 2, Ex 2j - Validator: dupa spatiu sau cratima, litera mare
def validator_majuscula_dupa_separator(text):
    if not text:
        return
    
    # Verifica daca dupa spatiu sau cratima avem litera mare
    for i in range(len(text) - 1):
        if text[i] in [' ', '-'] and text[i + 1].isalpha():
            if not text[i + 1].isupper():
                raise ValidationError("Dupa spatiu sau cratima trebuie sa aveti litera mare.")



# Lab 5, Task 2, Ex 3b - Validator: semnatura in mesaj (ultimul cuvant sa fie numele utilizatorului)
def validator_semnatura_in_mesaj(mesaj, nume):
    cuvinte = re.findall(r'\w+', mesaj)
    if not cuvinte:
        raise ValidationError("Mesajul trebuie sa contina cuvinte.")
    
    ultim_cuvant = cuvinte[-1].lower()
    nume_lower = nume.lower()
    
    if ultim_cuvant != nume_lower:
        raise ValidationError(f"Mesajul trebuie sa se termine cu semnatura (numele '{nume}').")

# Lab 5, Task 2, Ex 3d - Validator: CNP corespunde cu data nasterii
def validator_cnp_data_nasterii(cnp, data_nasterii):
    if not cnp:
        return
    
    # CNP: pozitiile 1-6 sunt AAMMDD
    an = int(cnp[1:3])
    luna = int(cnp[3:5])
    zi = int(cnp[5:7])
    
    # Detecteaza secolul din prima cifra
    # 1-2 = 1900s, 5-6 = 2000s
    if cnp[0] in ['1', '2']:
        an_complet = 1900 + an
    elif cnp[0] in ['5', '6']:
        an_complet = 2000 + an
    else:
        return
    
    # Verifica daca luna si ziua din CNP se potrivesc cu data nasterii
    if data_nasterii.year != an_complet or data_nasterii.month != luna or data_nasterii.day != zi:
        raise ValidationError("CNP-ul nu corespunde cu data nasterii.")
    

# Lab 5, Task 2, Ex 4a - Preprocesare: calculeaza varsta in ani si luni
def preproceseaza_varsta(data_nasterii):
    today = date.today()
    ani = today.year - data_nasterii.year - ((today.month, today.day) < (data_nasterii.month, data_nasterii.day))
    luni = (today.month - data_nasterii.month) % 12
    return f"{ani} ani si {luni} luni"

# Lab 5, Task 2, Ex 4b -  elimina linii noi si comaseaza spatii
def preproceseaza_mesaj_spatii(mesaj):
    mesaj = mesaj.replace('\n', ' ').replace('\r', ' ')
    mesaj = re.sub(r' +', ' ', mesaj)
    return mesaj.strip()

# Lab 5, Task 2, Ex 4c - majuscula dupa terminatori de fraza
def preproceseaza_majuscula_dupa_terminatori(mesaj):
    # Majuscula dupa . ? ! ...
    mesaj = re.sub(r'([.!?])\s+([a-z])', lambda m: m.group(1) + ' ' + m.group(2).upper(), mesaj)
    #Regex: dupa .!? si spatii, litera mica devine mare; 
    #lambda: functie anonima care primeste match-ul si returneaza textul modificat
    #m.group(1) = terminatorul de fraza, m.group(2) = litera care trebuie transformata in majuscula
    mesaj = re.sub(r'(\.\.\.\s+)([a-z])', lambda m: m.group(1) + m.group(2).upper(), mesaj)
    return mesaj

# Lab 5, Task 2, Ex 4d - seteaza urgent si genereaza nume fisier
def preproceseaza_urgent(tip_mesaj, minim_zile):
    urgent = False
    
    # Determina minimul de zile necesar pentru tipul de mesaj
    minim_required = 2
    if tip_mesaj in ['review', 'cerere']:
        minim_required = 4
    
    # Daca zile = minim required, e urgent
    if minim_zile == minim_required:
        urgent = True
    
    return urgent


# Lab 6, Task 2, Ex 3 - Validator telefon (10 cifre)
def validator_telefon(telefon):
    if telefon and not telefon.replace(' ', '').replace('-', '').isdigit():
        raise ValidationError("Telefonul trebuie sa contina doar cifre.")
    if telefon and len(telefon.replace(' ', '').replace('-', '')) != 10:
        raise ValidationError("Telefonul trebuie sa aiba exact 10 cifre.")

# Lab 6, Task 2, Ex 3 - Validator cod postal (5 cifre)
def validator_cod_postal(cod):
    if cod and not cod.isdigit():
        raise ValidationError("Codul postal trebuie sa contina doar cifre.")
    if cod and len(cod) != 5:
        raise ValidationError("Codul postal trebuie sa aiba exact 5 cifre.")

# Lab 6, Task 2, Ex 3 - Validator judet (minim 3 caractere)
def validator_judet(judet):
    if judet and len(judet) < 3:
        raise ValidationError("Judetul trebuie sa aiba minim 3 caractere.")
    
# Lab 7, Task 1b - Generare cod aleator pentru confirmare email
def genereaza_cod_confirmare():
    caractere = string.ascii_letters + string.digits
    return ''.join(secrets.choice(caractere) for _ in range(20)) #alegere aleatorie 
    
    