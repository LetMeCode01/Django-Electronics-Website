from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Produs, Brand, Categorie, Discount, Tag, DateClient, Specificatie


# Lab 8, Task 2.1 - Inline pentru DateClient in UserAdmin
class DateClientInline(admin.StackedInline):
    model = DateClient
    can_delete = False
    verbose_name_plural = 'Date Client Suplimentare'
    fk_name = 'user'

#cand aditam un user in admin, apar automat si campurile din DateCLient
# Lab 8, Task 2.1 - UserAdmin personalizat cu DateClient inline
class UserAdmin(BaseUserAdmin):
    inlines = (DateClientInline,)
    #tupluri de clase Inline pentru a le include in UserAdmin
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    
    def get_inline_instances(self, request, obj=None):
        if not obj:#daca nu e instanta User
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)


# Lab 8, Task 2.1 - Re-inregistrare User cu noul UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# Lab 4, Task Admin, Ex 2 - Inregistrare modele in admin
class TagAdmin(admin.ModelAdmin):
    # Lab 4, Task Admin, Ex 5 - Search fields pentru 2 campuri
    search_fields = ['nume', 'culoare_hex']
    list_per_page = 10

class ProdusAdmin(admin.ModelAdmin):
    # Lab 4, Task Admin, Ex 4 - Schimbarea ordinii coloanelor
    list_display = ('pret', 'nume', 'cod_produs', 'stoc', 'status', 'brand', 'categorie', 'afisare_taguri')
    #tuplu de stringuri cu numele campurilor in ordinea dorita
    
    # Lab 4, Task Admin, Ex 7 - Filtre laterale
    list_filter = ('status', 'brand', 'categorie', 'data_adaugare')
    #tuplu cu campurile aparute ca filtre in sidebar-ul din dreapta
    
    # Lab 4, Task Admin, Ex 5 - Search fields pentru 2 campuri
    search_fields = ('nume', 'descriere')
    #tuplu cu numele campurilor cautate; LIKE '%cuvant%'
    
    # Lab 4, Task Admin, Ex 8 - Schimbarea numarului de itemuri pe pagina la 5
    list_per_page = 5
    #paginare automata; se genereaza link-uri pt navigare intre pagini
    
    # Lab 4, Task Admin, Ex 6 - Ordonare descrescatoare dupa pret
    ordering = ('-pret',)
    #tuplu cu campurile pentru sortare; ORDER BY pret DESC;
    
    # Lab 4, Task Admin, Ex 9 - Fieldsets 
    fieldsets = ( #tuplu de tupluri titlu_sectiune, dictionar_optiuni
        ('Informatii principale', {#campurile incluse in sectiune
            'fields': ('nume', 'cod_produs', 'pret', 'brand', 'categorie')
        }),
        ('Detalii suplimentare', {
            'fields': ('descriere', 'stoc', 'status', 'taguri'),
            'classes': ('collapse',) #adauga clasa CSS collapse pentru a face sectiunea colapsabila
        }),
    )
    
    # Lab 4, Task Admin, Ex 9 - Filter horizontal pentru many-to-many
    filter_horizontal = ('taguri',)

    def afisare_taguri(self, obj):
        return ", ".join([t.nume for t in obj.taguri.all()])
    afisare_taguri.short_description = 'Taguri'

class BrandAdmin(admin.ModelAdmin):
    # Lab 4, Task Admin, Ex 5 - Search fields pentru 2 campuri
    search_fields = ('nume', 'tara_origine')
    
    # Lab 4, Task Admin, Ex 7 - Filtre laterale
    list_filter = ('an_infiintare',)
    
    list_display = ('nume', 'tara_origine', 'an_infiintare')
    list_per_page = 10

class CategorieAdmin(admin.ModelAdmin):
    # Lab 4, Task Admin, Ex 5 - Search fields pentru 2 campuri
    search_fields = ('nume', 'descriere')
    
    # Lab 4, Task Admin, Ex 7 - Filtre laterale
    list_filter = ('discount',)
    
    list_display = ('nume', 'discount')
    list_per_page = 10

class DiscountAdmin(admin.ModelAdmin):
    # Lab 4, Task Admin, Ex 5 - Search fields pentru 2 campuri
    search_fields = ('nume', 'procent')
    
    # Lab 4, Task Admin, Ex 7 - Filtre laterale
    list_filter = ('activ', 'data_start', 'data_sfarsit')
    
    # Lab 4, Task Admin, Ex 6 - Ordonare descrescatoare dupa procent
    ordering = ('-procent',)
    
    list_display = ('nume', 'procent', 'activ', 'data_start', 'data_sfarsit')
    list_per_page = 10

class SpecificatieAdmin(admin.ModelAdmin):
    # Lab 4, Task Admin, Ex 2 - Inregistrare Specificatie in admin
    # Lab 4, Task Admin, Ex 5 - Search fields pentru 2 campuri
    search_fields = ('produs__nume', 'nume_atribut')
    
    # Lab 4, Task Admin, Ex 7 - Filtre laterale
    list_filter = ('produs',)
    
    list_display = ('produs', 'nume_atribut', 'valoare')
    list_per_page = 10

class DateClientAdmin(admin.ModelAdmin):
    # Lab 4, Task Admin, Ex 5 - Search fields pentru 2 campuri
    search_fields = ('user__username', 'display_user')
    # Lab 4, Task Admin, Ex 7 - Filtre laterale
    list_filter = ('vip', 'a_cumparat', 'data_inregistrarii', 'blocat')
    # Afiseaza si permite editarea campului 'blocat' direct din lista
    list_display = ('user', 'display_user', 'vip', 'a_cumparat', 'data_inregistrarii', 'blocat')
    list_editable = ('blocat',)
    list_per_page = 10

# Lab 4, Task Admin, Ex 10 - Personalizarea paginii de administrare
#textul afisat in header-ul paginii admin
admin.site.site_header = "Administrare Proiect Electronice"
#titlul din tab-ul browserului <title>
admin.site.site_title = "Admin Proiect Electronice"
#titlul de pe pagina principala a admin-ului
admin.site.index_title = "Bine ai venit in panoul de administrare"
#aplicate global pentru intregul site admin

# Lab 4, Task Admin, Ex 2 - Inregistrare modele in admin
admin.site.register(Produs, ProdusAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Categorie, CategorieAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(Specificatie, SpecificatieAdmin)
admin.site.register(DateClient, DateClientAdmin)
#functii care fa modelul vizibil in panoul admin
#Model-clasa modelului din models.py, ModelAdmin-clasa de personalizare a interfetei admin pentru acel model