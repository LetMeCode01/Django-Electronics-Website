@echo off
REM Lab 6, Task 2, Ex 1 - Backup baza de date

REM Directorul proiectului Django
cd /d c:\Users\Mihai Sima\Desktop\proiect_electronice\proiect_electronice

REM Verificam daca manage.py exista
if not exist manage.py (
    echo EROARE: manage.py nu a fost gasit!
    echo Directorul actual: %cd%
    pause
    exit /b 1 #iesire din script cu cod de eroare
)

REM Activam virtual environment (daca exista)
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

REM Generam backup
echo Creez backup...
python manage.py dumpdata electronice > backup_data.json 
#redirectioneaza output in fisier; 
#dumpdata extrage datele din baza de date in format JSON

REM Verificam daca s-a creat fisierul
if exist backup_data.json (
    echo Backup creat cu succes: backup_data.json
) else (
    echo EROARE: Fisierul nu s-a creat!
)

pause #asteapta apasare tasta inainte de a inchide fereastra