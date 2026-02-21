from django.contrib import admin
from django.urls import path, include
from electronice import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('electronice.urls')),
    
    # Lab 7, Task 1e - Confirmare email cu prefix electronice/
    path('electronice/confirma_mail/<str:cod>/', views.confirma_mail, name='confirma_mail_lab7'),
    
    # Lab 7, Task 2.5 - Pagina promotii cu prefix electronice/
    path('electronice/promotii/', views.promotii, name='promotii_lab7'),
]

# Lab 8, Task 1 - Handler pentru pagina de eroare 403 personalizata
handler403 = views.eroare_403_view
