from django import template
register = template.Library()
from prodavnica.models import Artikal

@register.assignment_tag()
def brojProcesora():
 return Artikal.objects.filter(kategorija_id = 1).count()