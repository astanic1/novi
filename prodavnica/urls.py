"""projekt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from . import views
from django.urls import reverse
from django.conf.urls import handler404
app_name = 'prodavnica'
handler404 = 'projekt.prodavnica.views.greska404'
urlpatterns = [
    url(r'^$', views.index, name= 'index'),
    url(r'^nesto/$', views.myview, name="nesto"),

    url(r'^nekaFunkcija/$', views.nekaFunkcija, name="pretraga"),
    url(r'^nekaFunkcija2/$', views.nekaFunkcija2, name="pretraga"),

    url(r'^pretraga/$', views.pretraga, name="pretraga"),
    url(r'^pretraga/([0-9]{1})$', views.pretraga, name="pretragaIndex"),
    url(r'^filtriraj/([0-9]{1})$', views.filtriraj, name="filtrirajIndex"),
    url(r'^pocetna/$', views.index, name="index"),
    url(r'^artikal/create/$', views.ArtikalCreate.as_view(), name="artikal-create"),
    url(r'^artikalListView/$', views.ArtikalListView.as_view(), name="artikal-list-view"),
    url(r'^artikalDetailView/(?P<pk>\d+)$', views.ArtikalDetailView.as_view(), name="artikal-detail-view"),

    url(r'^artikal/update/(?P<pk>[0-9]+)/$', views.ArtikalUpdate.as_view(), name="artikal-update"),
    url(r'artikal/delete/(?P<pk>[0-9]+)/$', views.ArtikalDelete.as_view(), name='artikal-delete'),
    url(r'^ajax/filtriraj/$', views.filtriraj, name="filtriraj"),
    url(r'^ajax/dodajUKorpu/$', views.dodajUKorpu, name="dodajUKorpu"),
    url(r'^ajax/obrisiIzKorpe/$', views.obrisiIzKorpe, name="obrisiIzKorpe"),
    url(r'^ajax/finalizujKupovinu/$', views.finalizujKupovinu, name="finalizujKupovinu"),
    url(r'^ajax/vratiArtikal/$', views.vratiArtikal, name="vratiArtikal"),
    url(r'^ajax/spasiPromjene/$', views.spasiPromjene, name="spasiPromjene"),

    url(r'^spasiRecenziju$', views.spasiRecenziju, name="spasiRecenziju"),
    url(r'^account$', views.account, name="account"),
    url(r'^zaposlenik', views.zaposlenik, name="zaposlenik"),
    url(r'^dajba', views.dajba, name="zaposlenik"),

    url(r'^dodajArtikal', views.ArtikalCreate.as_view(), name="dodajArtikal"),

    url(r'^register/$', views.register, name="register"),
    url(r'^login/$', views.login_user, name="login_user"),
    url(r'^logout/$', views.logout_user, name="logout_user"),

    url(r'^katalog/$', views.katalog, name="katalog"),
    url(r'^korpa/$', views.korpa, name="korpa"),

    url(r'^katalog/([0-9]{1})$', views.katalog, name="katalogIndex"),

    url(r'^(?P<artikal_id>[0-9]+)/$', views.artikal, name="artikalView"),
    url(r'^(?P<artikal_naziv>\w+)/$', views.artikalPoNazivu, name="artikalPoNazivu"),

]
