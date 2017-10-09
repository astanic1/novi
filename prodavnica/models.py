from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.

import datetime
from django.utils import timezone

class Proizvodjac(models.Model):
    naziv = models.CharField(max_length=200)
    def __str__(self):
        return self.naziv

class Kategorija(models.Model):
    naziv = models.CharField(max_length=200)

    def __str__(self):
        return self.naziv

class Artikal(models.Model):
    naziv = models.CharField(max_length=200)
    datum_unosa = models.DateTimeField('datum unosa')
    cijena=models.IntegerField(default=0)
    ikona=models.CharField(max_length=250)
    proizvodjac = models.ForeignKey(Proizvodjac, on_delete=models.DO_NOTHING)
    kategorija = models.ForeignKey(Kategorija,on_delete=models.DO_NOTHING)


    def __str__(self):
        return self.naziv

class Korisnik(models.Model):
    username= models.CharField(max_length=25)
    ime= models.CharField(max_length=25)
    prezime= models.CharField(max_length=25)
    password= models.CharField(max_length=25)
    tip= models.CharField(max_length=9)




    def __str__(self):
        return self.username


class Slika(models.Model):
    slika = models.ImageField(upload_to = 'prodavnica/slike/', default = r'C:\Python34\Scripts\env_site1\korisnik.png')
    korisnik = models.ForeignKey(User, on_delete=models.CASCADE)



class Recenzija(models.Model):
    ocjena=models.IntegerField(default=0)
    tekst=models.CharField(max_length=600)
    artikal = models.ForeignKey(Artikal, on_delete=models.CASCADE)
    korisnik = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.korisnik.username



class StatusNarudzbe(models.Model):
    status = models.CharField(max_length=50)



class Narudzba(models.Model):
    korisnik =models.ForeignKey(User, on_delete=models.CASCADE)
    datum_narudzbe = models.DateTimeField('datum narudzbe',default=timezone.now, blank=True)
    adresa = models.CharField(max_length=200)
    status_narudzbe= models.ForeignKey(StatusNarudzbe, on_delete=models.CASCADE)
    def __str__(self):
        return self.korisnik.username



class StavkaNarudzbe(models.Model):
    artikal = models.ForeignKey(Artikal, on_delete=models.CASCADE)
    narudzba = models.ForeignKey(Narudzba, on_delete=models.CASCADE)
    kolicina = models.IntegerField(default=0)


class Korpa(models.Model):
    korisnik =models.ForeignKey(User, on_delete=models.CASCADE)


class StavkaKorpe(models.Model):
    artikal = models.ForeignKey(Artikal, on_delete=models.CASCADE)
    korpa = models.ForeignKey(Korpa, on_delete=models.CASCADE)
    kolicina = models.IntegerField(default=0)
