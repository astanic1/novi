from django import template

register = template.Library()

@register.filter(is_safe=True)
def dajPrviKarakter(string):
    return string[0]

@register.filter(is_safe=True)
def mojfilter(kolekcija,brojac):
    return kolekcija[brojac-1].username

@register.filter(is_safe=True)
def dajStavku(kolekcija,brojac):
    return kolekcija[brojac-1].id

@register.filter(is_safe=True)
def djeljivo(brojac):
    if brojac%3==0:
        return 'da'
    return 'ne'

@register.filter(is_safe=True)
def dajURL(lokacija):
    url = lokacija[17:len(lokacija)]
    return url


@register.filter(is_safe=True)
def dajKolicinu(kolekcija,brojac):
    return kolekcija[brojac-1].kolicina

@register.filter(is_safe=True)
def dajCijenu(kolekcija,brojac):
    return kolekcija[brojac-1]





@register.filter(is_safe=True)
def tostring(arg):
    return str(arg)


@register.filter(is_safe=True)
def prebrojProcesore(kolekcija):
    brojac=0
    for artikal in kolekcija:
        if artikal.kategorija_id==1:
            brojac=brojac+1
    return brojac

@register.filter(is_safe=True)
def prebrojMaticne(kolekcija):
    brojac = 0
    for artikal in kolekcija:
        if artikal.kategorija_id == 2:
            brojac = brojac + 1
    return brojac
@register.filter(is_safe=True)
def prebrojGraficke(kolekcija):
    brojac = 0
    for artikal in kolekcija:
        if artikal.kategorija_id == 3:
            brojac = brojac + 1
    return brojac
