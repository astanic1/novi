from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.utils.timezone import now

# Create your views here.
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.views.generic import View
from .forms import UserForm
from django.contrib.auth.models import User

import hashlib

from django.shortcuts import get_object_or_404
from django.urls import reverse
from .models import Artikal
from .models import Recenzija
from .models import Korpa
from .models import StavkaKorpe
from .models import Narudzba
from .models import StavkaNarudzbe
from .models import StatusNarudzbe
from .models import Slika
from .models import Kategorija
from .models import Proizvodjac
from django.template import Context,RequestContext,Template

import io

from .models import Narudzba


from .models import Korisnik
from django.contrib.auth.models import User
from django.core import paginator

from .validacija import *
from django.contrib.sessions.models import Session


from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from django import forms

from django.contrib.auth.forms import UserCreationForm
from .forms import UploadFileForm
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView,DetailView


@login_required(login_url='/prodavnica/katalog')
def myview():
    return HttpResponse('asdasdasd')


class ArtikalForm(forms.ModelForm):
    class Meta :
        model = Artikal
        fields = ['naziv', 'cijena', 'ikona','kategorija','proizvodjac']
        widgets = {
            'naziv' : forms.TextInput(attrs={'class': 'mycssclass'}),
            'cijena': forms.NumberInput(attrs={'class': 'mycssclass'}),
            'ikona': forms.TextInput(attrs={'class': 'mycssclass'})
        }

class ArtikalCreate(CreateView):
    model = Artikal
    form_class = ArtikalForm
    success_url = '/prodavnica/katalog'


class ArtikalUpdate(UpdateView):
    model = Artikal
    fields = ['naziv', 'cijena', 'ikona']
    success_url = '/prodavnica/katalog'


class ArtikalDelete(DeleteView):
    model = Artikal
    success_url = '/prodavnica/katalog'


class ArtikalListView(ListView):
    queryset = Artikal.objects.all()
    context_object_name = 'lista_katalog'
    paginate_by = 6
    template_name = 'prodavnica/katalog.html'
    extra_context = {'dodatniPodaci': 'pozdrav'}

class ArtikalDetailView(DetailView):
    model = Artikal
    context_object_name = 'artikal'
    template_name = 'prodavnica/artikal.html'
    extra_context = {'dodatniPodaci': 'pozdrav'}

def nekaFunkcija(request):
    request.session['kljuc'] = 'vrijednost'
    return HttpResponse('uredu')


def nekaFunkcija2(request):
    nesto = request.session['kljuc']
    return HttpResponse(nesto)


@permission_required('prodavnica.add_artikal', raise_exception=True)
def zaposlenik(request):
    if request.method=='POST':
        artikal_id = request.POST.get('artikal_id')
        novi_naziv = request.POST.get('novi_naziv')
        nova_cijena = request.POST.get('nova_cijena')

        print(artikal_id)
        obj = Artikal.objects.get(id=artikal_id)
        setattr(obj, 'naziv',novi_naziv)
        setattr(obj, 'cijena', nova_cijena)
        obj.save()

        return HttpResponse('uredu')

    else:
        data = {
            'artikli' : Artikal.objects.all()
        }
        return render(request, 'prodavnica/zaposlenik.html',data)

def spasiPromjene(request):
    artikal_id = request.GET['artikal_id']
    novi_naziv = request.GET['novi_naziv']
    nova_cijena = request.GET['nova_cijena']

    print(artikal_id)
    obj = Artikal.objects.get(id=artikal_id)
    setattr(obj, 'naziv', novi_naziv)
    setattr(obj, 'cijena', nova_cijena)
    obj.save()

    return HttpResponse('uredu')


def vratiArtikal(request):
    artikal = Artikal.objects.get(id=request.GET['artikal_id'])
    pomoc=string = ' <div class="card card-inverse card-info"><img class="card-img-top" src="' + artikal.ikona + '"><div class="card-block"> <figure class="profile profile-inline"> <img src="' + artikal.ikona + '" class="profile-avatar" alt=""> </figure> </figure> <h4 class="card-title">' + artikal.naziv + '</h4> <div class="card-text"> Cijena: ' + str(
        artikal.cijena) + ',00 KM </div> </div>  <div class="card-footer"> <button class="btn btn-success" onclick="pokusaj(' + str(
        artikal.id) + ')" id="' + str(artikal.id) + '">U korpu</button> </div> </div>       Novi naziv<input type=text id="novi_naziv" placeholder="' + artikal.naziv + '"> Nova cijena<input type=text id="nova_cijena" placeholder="' + str(artikal.cijena) + '">           '


    forma = '<form class="form-horizontal"> <div class="form-group"> <label class="control-label col-sm-2" for="novi_naziv">Novi Naziv</label> <div class="col-sm-10"> <input type="text" class="form-control" id="novi_naziv" placeholder="' +artikal.naziv+'"> </div> </div><div class="form-group"> <label class="control-label col-sm-2" for="nova_cijena">Nova Cijena</label> <div class="col-sm-10"> <input type="text" class="form-control" id="nova_cijena" placeholder="' +str(artikal.cijena) + ',00 KM"> </div></div> </form>'


    string = '<div id="cuvajId" style="display:none">' + str(artikal.id) + '</div> <div class="card card-inverse card-info"><img class="card-img-top" src="' + artikal.ikona + '"><div class="card-block"> </figure> <div class="card-text"> '+forma+'   </div> </div>  <div class="card-footer"> <button class="btn btn-success" onclick="spasiPromjene()", id="spasiPromjene"> Spasi promjene</button> </div> </div>               '

    return HttpResponse(string)

def account(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                Slika.objects.create(korisnik_id=request.user.id,slika=form.cleaned_data['file'])
                return redirect('http://localhost:8000/prodavnica/account')
    else:
        form = UploadFileForm()

    slika = list(Slika.objects.filter(korisnik_id=request.user.id))[0].slika.url
    print(slika)
    return render(request, 'prodavnica/account.html', {'form': form,'slika':slika})



class UserFormView(View):
    form_class = UserForm
    template_name = '/prodavnica/registration_form.html'

    def get(self,request):
        form = self.form_class(None)
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            #class KatalogView(generic.ListView):
    #   template_name = 'prodavnica/katalog.html'
    #   context_object_name = 'lista_katalog'


    #  def get_queryset(self):
#     return Artikal.objects.all()
    #        return Artikal.objects.filter(kategorija=2) ako hoces one iz kategorije 2 odnosno maticne




def register(request):
    form = RegisterForm(request.POST or None)
    if request.method=='GET':
        if not request.user.is_authenticated() :
            return render(request, 'prodavnica/register.html', {'form': form})
        else :
            return redirect('http://localhost:8000/prodavnica/katalog')
    else:
        if form.is_valid():
            data = form.cleaned_data
            user = User(username = data['username'])
            user.set_password(data['password'])
            password = user.password
            User.objects.create(email=data['email'],username=data['username'],first_name=data['first_name'],last_name=data['last_name'],password=password)
            Korpa.objects.create(korisnik_id=User.objects.last().id)
            user = authenticate(username=data['username'], password=data['password'])
            login(request,user)
            return redirect('http://localhost:8000/prodavnica/katalog')
        else:
            return render(request, 'prodavnica/register.html', {'form': form})


def login_user_after_registration(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect('http://localhost:8000/prodavnica/katalog')

    else:
        return redirect('http://localhost:8000/prodavnica/katalog', {'poruka': 'neuspjeh'})


def dajba(request):
    id = Artikal.objects.filter(naziv = 'qwegggggg').first().id
    recenzija = Recenzija.objects.filter(id=id).first()
    print(recenzija.tekst)
    print(id)
    return HttpResponse('asasd')

def login_user(request):

    if request.method == 'POST':
        username = request.POST.get('username_login')
        password = request.POST.get('password_login')
        user = authenticate(username=username, password=password)

        if user is not None :
            login(request,user)
            return redirect('http://localhost:8000/prodavnica/katalog')
        else :
            return render(request,'prodavnica/login.html',{'poruka':'neuspjeh'})
    else :
        if not request.user.is_authenticated() :
            return render(request,'prodavnica/login.html')
        else :
            return redirect('http://localhost:8000/prodavnica/katalog')


def logout_user(request):
    logout(request)
    return redirect('http://localhost:8000/prodavnica/login')

def katalog(request,page=1,naziv='svi_artikli',minCijena='0',maxCijena='1000'):

    print(page)


    if naziv=='svi_artikli' :
        artikli=list(Artikal.objects.all())

    else:
        artikli = list(Artikal.objects.filter(naziv__contains=naziv).filter(cijena__gte=minCijena).filter(cijena__lte=maxCijena))


    procesori = Artikal.objects.filter(kategorija_id=1).count()
    maticne =  Artikal.objects.filter(kategorija_id=2).count()
    graficke = Artikal.objects.filter(kategorija_id=3).count()

    paginator = Paginator(artikli,6)

    try :
        artikli = paginator.page(page).object_list
    except Exception :
        context = {
            'lista_katalog': None,
            'procesori': procesori,
            'maticne': maticne,
            'graficke': graficke,
            'page' : paginator.page(page)
        }
        return render(request, 'prodavnica/katalog.html', context=context)



    context = {
        'lista_katalog':artikli,
        'procesori':procesori,
        'maticne':maticne,
        'graficke':graficke,
        'page':paginator.page(page)
    }
    return render(request, 'prodavnica/katalog.html', context=context)




    print(page)

    if naziv == 'svi_artikli':
        artikli = list(Artikal.objects.all())
    else :
        artikli = Artikal.objects.filter(naziv__contains=naziv,cijena__gte=minCijena,cijena__lte=maxCijena)








    procesori = Artikal.objects.filter(kategorija_id=1).count()
    maticne =  Artikal.objects.filter(kategorija_id=2).count()
    graficke = Artikal.objects.filter(kategorija_id=3).count()


    print("tri")

    context = {
        'lista_katalog': artikli,
        'procesori': procesori,
        'maticne': maticne,
        'graficke': graficke,
        'kategorije': kategorije,
        'proizvodjaci': proizvodjaci,
        'minCijena': minCijena,
        'maxCijena': maxCijena,
    }
    print("cetri")

    return render(request, 'prodavnica/katalog.html', context=context)



def artikal(request,artikal_id):
    recenzije = Recenzija.objects.filter(artikal=artikal_id)
    artikal = Artikal.objects.get(id=artikal_id)
    pomocni=list(recenzije)
    ids=[]
    for p in pomocni :
        ids.append(p.korisnik_id)

    korisnici = list(User.objects.filter(id__in=ids))

    korisnicka_imena=[]
    tekstovi=[]
    ocjene=[]
    brojac=0



    korisnici=[]
    for recenzija in recenzije:
        korisnici.append(list(User.objects.filter(id=recenzija.korisnik_id))[0])



    korisnik_popunio="ne"
    for korisnik in korisnici:
        if korisnik.id == request.user.id :
            korisnik_popunio="da"

    context = {
        'lista_korisnika' : korisnici,
        'artikal' : artikal,
        'lista_recenzije': recenzije,

        'korisnik_popunio' : korisnik_popunio,


        'korisnicka_imena' : korisnicka_imena,
        'tekstovi' : tekstovi,
        'ocjene' : ocjene,


        'procesori': Artikal.objects.filter(kategorija_id=1).count(),
        'maticne': Artikal.objects.filter(kategorija_id=2).count(),
        'graficke': Artikal.objects.filter(kategorija_id=3).count()

    }

    return render(request, 'prodavnica/artikal.html', context)



def artikalPoNazivu(request,artikal_naziv):
    artikli = Artikal.objects.filter(naziv=artikal_naziv)
    pomocni = list(artikli)
    ids = []
    for p in pomocni:
        ids.append(p.id)


    recenzije = Recenzija.objects.filter(artikal_id__in=ids)

    pomocni = list(recenzije)
    ids = []
    for p in pomocni:
        ids.append(p.korisnik_id)

    korisnici = User.objects.filter(id__in=ids)

    context = {
        'lista_korisnika': korisnici,
        'artikal': artikal,
        'lista_recenzije': recenzije,
    }

    return render(request, 'prodavnica/artikal.html', context)


from .forms import RegisterForm

def greska404(request):
    return render(request,'prodavnica/404.html')

def index(request):
    if request.method == 'GET':
        if not request.user.is_authenticated() :
            return redirect('http://localhost:8000/prodavnica/login')
            return register(request)
        else :
            return redirect('http://localhost:8000/prodavnica/katalog')
            return katalog(request)

ARTIKLI_PO_STRANICI = 6

@csrf_exempt
def pretraga(request,page=1):
    minCijena = request.POST.get('minCijena')
    maxCijena = request.POST.get('maxCijena')
    naziv = request.POST.get('upit')
    kategorije = request.POST.getlist('kategorije[]')
    proizvodjaci = request.POST.getlist('proizvodjaci[]')


    sviartikli = list(Artikal.objects.filter(naziv__contains=request.POST.get('upit')).filter(cijena__gt=minCijena).filter(cijena__lt=maxCijena))
    page=int(page)
    filtriraniArtikli = []



    print(len(kategorije))
    print(len(proizvodjaci))

    if kategorije is None or proizvodjaci is None :
        string = '<div class="col-sm-4 "></div><div class="col-sm-4 "><h4>Nazalost nema takvih artikala</h4></div><div class="col-sm-4 "></div>'
        return HttpResponse(string)

    print("ASDASD")

    kategorijeObjekti = list(Kategorija.objects.filter(naziv__in=kategorije))
    proizvodjaciObjekti = list(Proizvodjac.objects.filter(naziv__in=proizvodjaci))


    kategorije=[]
    proizvodjaci=[]
    for kategorija in kategorijeObjekti :
        kategorije.append(kategorija.id)
    for proizvodjac in proizvodjaciObjekti:
        proizvodjaci.append(proizvodjac.id)

    for artikal in sviartikli :
        if artikal.kategorija_id in kategorije and artikal.proizvodjac_id in proizvodjaci :
            filtriraniArtikli.append(artikal)

    print(len(filtriraniArtikli))

    sviartikli = filtriraniArtikli
    brojac = (int(page) - 1) * ARTIKLI_PO_STRANICI
    artikli = []
    if (page * (ARTIKLI_PO_STRANICI-1)) < len(sviartikli) :
        artikli = sviartikli[brojac:(page * (ARTIKLI_PO_STRANICI)) ]
    else :
        artikli = sviartikli[brojac:]




    string = '<div class="container"><div class="row"><div class = "container"><ul class="pagination" id="nesto">'
    if not page == 1:
        string = string + '<li onclick="dajPretragu(' + str(page - 1) + ',\'' + str(naziv) + '\',' + str(
            minCijena) + ',' + str(maxCijena) + ')"><a>«</a></li>'
    if not len(artikli) == 0 and not artikli[-1] == sviartikli[-1]:
        string = string + '<li onclick="dajPretragu(' + str(page + 1) + ',\'' + str(naziv) + '\',' + str(
            minCijena) + ',' + str(maxCijena) + ')"><a>»</a></li>'

    string = string + '</ul></div></div></div><div class="container"><div class="row">'

    for artikal in artikli:
        string = string + '<div class="col-sm-4 "> <div class="card card-inverse card-info"><a href="http://127.0.0.1:5000/artikal/' + str(
            artikal.id) + '"> <img class="card-img-top" src="' + artikal.ikona + '"> </a><div class="card-block"> <figure class="profile profile-inline"> <img src="' + artikal.ikona + '" class="profile-avatar" alt=""> </figure> </figure> <h4 class="card-title">' + artikal.naziv + '</h4> <div class="card-text"> Cijena: ' + str(
            artikal.cijena) + ',00 KM </div> </div>  <div class="card-footer"> '
        if request.user.is_authenticated() :
            string = string + '<button class="btn btn-success" onclick="pokusaj(' + str(artikal.id) + ')" id="' + str(artikal.id) + '">U korpu</button> '
        string = string + '</div> </div> </div>'

    string = string + '</div></div>'
    if len(artikli) == 0:
        string = '<div class="col-sm-4 "></div><div class="col-sm-4 "><h4>Nazalost nema takvih artikala</h4></div><div class="col-sm-4 "></div>'


    return HttpResponse(string)

@csrf_exempt
def filtriraj(request,page=1):

    minCijena=1
    maxCijena=1000

    minCijena=request.POST.get('minCijena')
    maxCijena=request.POST.get('maxCijena')
    kategorija=request.POST.get('kategorija')

    print(minCijena)
    print(maxCijena)
    print(kategorija)

    if kategorija=='kategorija_procesori':
        pomocni_artikli = Artikal.objects.filter(kategorija=1,cijena__gt=minCijena,cijena__lt=maxCijena)
    elif kategorija=='kategorija_maticne' :
        pomocni_artikli = Artikal.objects.filter(kategorija=2,cijena__gt=minCijena,cijena__lt=maxCijena)
    else:
        pomocni_artikli = Artikal.objects.filter(kategorija=3,cijena__gt=minCijena,cijena__lt=maxCijena)


    print("AAA" + str(len(pomocni_artikli)))


    sviartikli = list(pomocni_artikli)
    page=int(page)

    brojac = (int(page) - 1) * 6

    artikli = []
    artikli = sviartikli[brojac:(page * 6)]

    string = '<div class="container"><div class="row"><div class = "container"><ul class="pagination" id="nesto">'
    if not page == 1:
        string = string + '<li onclick="dajKategoriju(' + str(page - 1) + ',\'' + str(kategorija) + '\',' + str(
            minCijena) + ',' + str(maxCijena) + ')"><a>«</a></li>'
    if not artikli[len(artikli) - 1] == sviartikli[len(sviartikli) - 1]:
        string = string + '<li onclick="dajKategoriju(' + str(page + 1) + ',\'' + str(kategorija) + '\',' + str(
            minCijena) + ',' + str(maxCijena) + ')"><a>»</a></li>'

    string = string + '</ul></div></div></div><div class="container"><div class="row">'

    for artikal in artikli:
        string = string + '<div class="col-sm-4 "> <div class="card card-inverse card-info"><a href="http://127.0.0.1:5000/artikal/' + str(
            artikal.id) + '"> <img class="card-img-top" src="' + artikal.ikona + '"> </a><div class="card-block"></figure> <h4 class="card-title">' + artikal.naziv + '</h4> <div class="card-text"> Cijena: ' + str(
            artikal.cijena) + ',00 KM </div> </div>  <div class="card-footer"> <button class="btn btn-success" onclick="pokusaj(' + str(
            artikal.id) + ')" id="' + str(artikal.id) + '">U korpu</button> </div> </div> </div>'

    string = string + '</div></div>'
    if len(artikli) == 0:
        string = '<div class="col-sm-4 "></div><div class="col-sm-4 "><h4>Nazalost nema takvih artikala</h4></div><div class="col-sm-4 "></div>'

    procesori=Artikal.objects.filter(kategorija=1).count()
    maticne = Artikal.objects.filter(kategorija=2).count()
    graficke = Artikal.objects.filter(kategorija=3).count()

    procesori=str(procesori)
    maticne = str(maticne)
    graficke = str(graficke)

    response =  string
    return HttpResponse(response)


def dodajUKorpu(request):

    artikal = int(request.GET['artikal'])

    korisnik = request.user



    if request.user.is_authenticated()  :

        korisnik_id=korisnik.id
        korpa_id=list(Korpa.objects.filter(korisnik_id=korisnik_id))[0].id

        if StavkaKorpe.objects.filter(korpa_id=korpa_id,artikal_id=artikal).count() == 0:
            StavkaKorpe.objects.create(artikal_id=artikal, korpa_id=korpa_id, kolicina=1)

        else:
            print("postoji")
            obj = StavkaKorpe.objects.get(korpa_id=korpa_id,artikal_id=artikal)
            setattr(obj,'kolicina',obj.kolicina+1)
            obj.save()






    return HttpResponse("asdasdasd")



def korpa(request):



    if request.user.is_authenticated() :
        korisnik_id = request.user.id

        korpa_id = list(Korpa.objects.filter(korisnik_id=korisnik_id))[0].id

        stavke_korpe = list(StavkaKorpe.objects.filter(korpa_id=korpa_id))

        ids=[]
        cijene=[]
        brojac=0
        for stavka in stavke_korpe :
            ids.append(stavka.artikal_id)


        artikli_korpe=[]
        for id in ids:
            artikli_korpe.append(list(Artikal.objects.filter(id=id))[0])
            cijene.append(stavke_korpe[brojac].kolicina * int(list(Artikal.objects.filter(id=id))[0].cijena))
            brojac=brojac+1




        data={
            'korisnik_id':korisnik_id,
            'korpa_id':korpa_id,
            'stavke_korpe':stavke_korpe,
            'artikli_korpe':artikli_korpe,
            'cijene': cijene,
            'procesori': Artikal.objects.filter(kategorija_id=1).count(),
            'maticne': Artikal.objects.filter(kategorija_id=2).count(),
            'graficke': Artikal.objects.filter(kategorija_id=3).count()

        }

        return render(request,'prodavnica/korpa.html',data)

    return redirect(request,'http://localhost:8000/prodavnica/katalog')


def obrisiIzKorpe(request):
    korpa_id = int(request.GET['korpa_id'])
    korisnik_id = int(request.GET['korisnik_id'])
    stavka_id = int(request.GET['stavka_id'])
    artikal_id = int(request.GET['artikal_id'])



    print("id stavke je " + str(stavka_id)+ " kraj")
    kolicina = getattr(StavkaKorpe.objects.get(id=stavka_id),'kolicina')
    print(str(kolicina))

    if kolicina == 1:
        StavkaKorpe.objects.filter(artikal_id=artikal_id,korpa_id=korpa_id).delete()
    else :
        obj = StavkaKorpe.objects.get(artikal_id=artikal_id,korpa_id=korpa_id)
        setattr(obj,'kolicina',int(getattr(obj,'kolicina'))-1)
        obj.save()


    stavke_korpe = list(StavkaKorpe.objects.filter(korpa_id=korpa_id))
    ids = []
    for stavka in stavke_korpe:
        ids.append(stavka.artikal_id)

    artikli_korpe = []
    for id in ids:
        artikli_korpe.append(list(Artikal.objects.filter(id=id))[0])

    response = '<div class="kolona dva" id="sadrzaj_korpe"><h1>Vasa korpa sadrzi</h1><div class="list-group">'

    brojac = 0

    for stavka in stavke_korpe:
        response = response + '<a href = "#" ' \
                              'class ="list-group-item"> &nbsp;' + artikli_korpe[brojac].naziv + ' <span class ="badge" style="float: right;" >' + str(stavka.kolicina) + 'x' + str(
            artikli_korpe[brojac].cijena) + ',00 KM </span><span style = "float: left;" > <button type = "button" style = "float: left;" class ="btn btn-default btn-xs" onclick = "obrisiIzKorpe(' + str(
            korpa_id) + ',' + str(artikli_korpe[brojac].id) + ',' + str(stavka.id) + ',' + str(
            korisnik_id) + ' )"><span class ="glyphicon glyphicon-remove" aria-hidden="true" > </span> </button> </span> </a>'
        brojac = brojac + 1

    if len(stavke_korpe) == 0:
        return HttpResponse( 'praznaKorpa')


    odgovor =  '<h1>Vasa korpa sadrzi</h1><table class="table table-hover"><thead><tr><th>Artikal</th><th>Naziv Artikla</th><th>Kolicina</th><th>Cijena</th><th>Smanji Kolicinu</th><th>Ukupna cijena</th></tr></thead><tbody>'

    brojac=0

    for stavka in stavke_korpe:
        odgovor=odgovor + '<tr>' \
        '<td style="vertical-align: middle;horiz-align: center;"><img style="width: 100px;height: 100px;" src="' + artikli_korpe[brojac].ikona +'"> </td> <td style="vertical-align: middle;horiz-align: center;">' + artikli_korpe[brojac].naziv + '</td>' \
        '<td style="vertical-align: middle;horiz-align: center;">' + str(stavka.kolicina) + '</td>' \
        '<td style="vertical-align: middle;horiz-align: center;">' + str(artikli_korpe[brojac].cijena) + ',00 KM</td>' \
        '<td style="vertical-align: middle;horiz-align: center;">' + '<button type="button" style="float: left;" class="btn btn-default btn-sm"' \
                'onclick="obrisiIzKorpe(' + str(
            korpa_id) + ',' + str(artikli_korpe[brojac].id) + ',' + str(stavka.id) + ',' + str(
            korisnik_id) + ')"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span></button>' \
        '<td style="vertical-align: middle;horiz-align: center;">' + str(artikli_korpe[brojac].cijena * stavka.kolicina) + ',00 KM </td>'  \
        '</tr>'
        brojac=brojac+1


    odgovor = odgovor + '</tbody></table>'



    return HttpResponse(odgovor)




def finalizujKupovinu(request):
    korisnik_id = int(request.GET['korisnik_id'])
    adresa = request.GET['adresa']

    if len(adresa) < 8 :
        return HttpResponse('adresa ispod 8 karaktera')

    korpa_id = list(Korpa.objects.filter(korisnik_id=korisnik_id))[0].id
    stavke_korpe = list(StavkaKorpe.objects.filter(korpa_id=korpa_id))

    Narudzba.objects.create(datum_narudzbe = now(),korisnik_id=korisnik_id,adresa=adresa,status_narudzbe_id=1)
    narudzba_id = Narudzba.objects.last().id

    print("korisnik id" + str(korisnik_id) + "korpa id " + str(korpa_id) + " adresa " + adresa + " datum " + str(now()))


    for stavka in stavke_korpe:
        StavkaNarudzbe.objects.create(artikal_id=stavka.artikal_id,narudzba_id=narudzba_id,kolicina=stavka.kolicina)

    StavkaKorpe.objects.filter(korpa_id=korpa_id).delete()

    return HttpResponse('odgovor')




def spasiRecenziju(request):

    tekst = request.GET['tekst_recenzije']
    if len(tekst) < 5:
        return HttpResponse('recenzija ispod 5 karaktera')


    artikal_id = request.GET['artikal_id']
    ocjena = request.GET['ocjena']
    korisnik_id = request.user.id

    Recenzija.objects.create(tekst=tekst,artikal_id=artikal_id,ocjena=ocjena,korisnik_id=korisnik_id)

    return redirect('http://localhost:8000/prodavnica/katalog')
