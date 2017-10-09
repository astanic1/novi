from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Artikal)
admin.site.register(Korisnik)
admin.site.register(Narudzba)
admin.site.register(StatusNarudzbe)
admin.site.register(StavkaNarudzbe)
admin.site.register(Recenzija)
admin.site.register(Proizvodjac)
admin.site.register(Kategorija)
admin.site.register(Slika)


