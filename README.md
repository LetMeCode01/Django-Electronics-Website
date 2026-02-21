# 🎩Proiect Django – Aplicatie E-commerce Electronice

**Aceasta este o aplicatie web dezvoltata in Django pentru gestionarea produselor electronice, utilizatori, comenzi, promotii si administrare avansata.**

_Vom parcurge in cele ce urmeaza laboratoarele rezolvate si conceptele invatate pe parcursul acesora._

# 🥼Laboratoare:

## 🧱 Laborator 2 – Modelare baze de date si arhitectura

### 🔹 Database Modeling

- Definirea entitatilor (User, Produs, Brand, Categorie etc.) si a relatiilor dintre ele.


### 🔹 Relatii intre entitati (1:1, 1:N, N:M)

Fundamental pentru orice aplicatie enterprise (e-commerce, CRM, ERP).
Asigura integritate si performanta la interogari.

<img width="852" height="519" alt="image" src="https://github.com/user-attachments/assets/985e3d7a-4707-4ee6-8eb0-4580c9fce85a" />

---

## 🗄️ Laborator 3 – Django ORM si Model Design

### 🔹 Django ORM

- Abstractizeaza SQL-ul si permite lucrul cu baza de date prin Python.

### 🔹 Field Options (null, blank, default, unique)

- Control asupra validarii si consistentei datelor.

---

## 📄 Laborator 4 – Views, Routing si Paginare

### 🔹 Function Based Views

- Control complet asupra logicii aplicatiei.

### 🔹 URL Routing

- Separarea clara a rutelor si logicii.

### 🔹 Pagination

- Optimizare pentru volume mari de date.
- Critic in e-commerce si aplicatii cu multe rezultate.

### 🔹 Sorting si Filtering

- Experienta dinamica pentru utilizator.

### 🔹 Custom 404 Handling

- Gestionarea erorilor pentru UX profesional.

---

## 📝 Laborator 5 – Formulare si Validari Avansate

### 🔹 Django Forms

- Validare automata si securizata a datelor primite.
- Standard industry pentru input handling.

### 🔹 Custom Validators

- Validari personalizate (CNP, corelare emailuri, reguli business).
- Foarte important pentru aplicatii enterprise.

### 🔹 Data Preprocessing

- Curatarea si normalizarea datelor inainte de salvare.
- Best practice pentru data integrity.

### 🔹 JSON Storage

- Salvare date in format JSON.
- Relevant pentru loguri, mesaje, microservicii.

### 🔹 IP Tracking

- Identificare utilizator pentru audit si securitate.

---

## 👤 Laborator 6 – Autentificare si Sistem E-commerce

### 🔹 Extended User Model (Profile Pattern)

- Separarea User de DateClient.
- Best practice pentru aplicatii scalabile.

<img width="940" height="847" alt="image" src="https://github.com/user-attachments/assets/0d9bf700-d5af-4fc6-8e06-f76f3f35979f" />


### 🔹 CRUD Operations

- Create, Read, Update, Delete pentru produse si utilizatori.
- Baza oricarui sistem backend.

### 🔹 Order System

- Simulare flux real de comenzi.

### 🔹 Backup & Restore (dumpdata / loaddata)
 
- Management date productie.
- Critic pentru DevOps si mentenanta.

### 🔹 Authentication System

- Register, login, change password.
- Fundamental pentru orice aplicatie web.

---

## 📧 Laborator 7 – Email, Promotii si Securitate

### 🔹 Email Confirmation Flow

- Verificare cont prin token unic.
- Standard in aplicatii reale pentru securitate.

### 🔹 Token Generation

- Generare cod random pentru validare.
- Folosit in reset password si verificari.

### 🔹 send_mass_mail

- Trimitere emailuri bulk segmentate.
- Relevant pentru marketing automation.

### 🔹 Activity Tracking (Vizualizari)

- Tracking comportament utilizator.
- Baza pentru recomandari si marketing.

### 🔹 Rate Limiting Login Attempts

- Protectie impotriva brute-force.
- Concept important in cybersecurity.

### 🔹 mail_admins

- Alertare automata pentru incidente.
- Practic in productie.

## 📊 Logging si Monitorizare

### 🔹 Python Logging

- Loguri separate pe niveluri: DEBUG, INFO, WARNING, ERROR, CRITICAL.
- Critic pentru debugging si productie.

### 🔹 File-based logging

- Persistenta evenimentelor sistemului.

### 🔹 Try-Except Error Handling

- Gestionare controlata a exceptiilor.

---

## 🔐 Laborator 8 – Permisiuni si Control Acces

### 🔹 Django Groups & Permissions

- Control granular al accesului.
- Foarte important in aplicatii enterprise.

### 🔹 Custom 403 Handler

- Personalizare pagina acces interzis.
- UX profesional si securitate.

### 🔹 Session Tracking

- Monitorizare acces repetat (protectie abuz).

### 🔹 Role-Based Access Control (RBAC)

- Implementare roluri: Administratori_produse, Administratori_site.

### 🔹 Conditional UI Rendering

- Afisare elemente in functie de permisiuni.


# 🎯 Functionalitati Avansate

### 🔹 Dynamic Promotional Banner (probabilistic display)

- Afisare conditionata 30% probabilitate.
- Concept folosit in marketing digital.

### 🔹 Runtime Permission Granting

- Acordare permisiuni dinamice la click.
- Simuleaza feature unlock.

### 🔹 Account Blocking System

- Control moderare utilizatori.
- Relevanta pentru marketplace-uri.

---

# 🏆 Concluzie - Competente Demonstrate

* Backend Development (Django)
* Database Design
* Authentication & Security
* Email Systems
* Logging & Monitoring
* Role-Based Access Control
* Data Validation & Processing
* E-commerce Architecture
* Production-ready Error Handling

**Pentru o vizualizare mai detaliata a taskurilor si rezultatele practice ale conceptelor aplicate, va invit sa parcurgeti documentatia si sa rulati local aplicatia.**
