import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelformset_factory
from django.http import JsonResponse
from django.http.response import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from twilio.rest import Client

from evangelisation.forms import PersonneForm, FormNbre
from evangelisation.models import Personne

from evangelisation.send_sms import send_sms




@login_required(login_url="user_login")
def notification_app_index(request):
    context = dict()
    personne = None
    personnes = None
    personnes_select_box = None
    anniversaires = None

    if 'liste-anniv' in request.GET:
        try:
            pers_select = Personne.objects.get(id=int(request.GET['liste-anniv']))
            anniversaires = Personne.objects.filter(date_naissance=pers_select.date_naissance)
            personnes = Personne.objects.filter(date_naissance__month=pers_select.date_naissance.month)
            context['pers_select'] = pers_select
        except Personne.DoesNotExist:
            raise Http404("Pages non disponible")
        context['pers_select'] = pers_select
    else:
        anniversaires = Personne.objects.filter(date_naissance__month=datetime.date.today().month, date_naissance__year=datetime.date.today().year)
        personnes = Personne.objects.all()

    context['anniversaires'] = anniversaires
    context['personnes'] = personnes
    context['personnes_select_box'] = Personne.objects.all()
    context['select_link'] = 'sms'
    return render(request, 'index.html', context)


@login_required(login_url="user_login")
def notification_app_recherche(request):
    context = dict()
    if 'liste-message' in request.GET:
        try:
            pers_select = Personne.objects.get(id=int(request.GET['liste-message']))
            personnes_send = Personne.objects.filter(date_naissance=pers_select.date_naissance)
        except Personne.DoesNotExist:
            raise Http404("Pages non disponible")

    context['pers_select'] = pers_select
    context['personnes_send'] = personnes_send
    return redirect('notification:notification_app_index')



@login_required(login_url="user_login")
def notification_app_ajouter_personne(request, type_opera):
    context = dict()
    form = None
    if request.method == 'POST':
        form = PersonneForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Personne ajouté avec success")
            return redirect('notification:notification_app_index')
    else:
        form = PersonneForm()
    context['form'] = form
    context['type_opera'] = type_opera
    context['personnes'] = Personne.objects.all()
    context['select_link'] = 'sms'
    return render(request, 'index.html', context)


@login_required(login_url="user_login")
def notification_app_detail_personne(request, type_opera, pk):
    context = dict()
    form = None
    personne = None
    try:
        personne = Personne.objects.get(id=pk)
        if request.method=="POST":
            form = PersonneForm(data=request.POST, instance=personne)
            if form.is_valid():
                form.save()
                messages.success(request, f"Personne modifier avec success")
                return redirect('notification:notification_app_index')
        else:
            form = PersonneForm(instance=personne)
            context['personne'] = personne
    except Personne.DoesNotExist:
        return Http404('page non disponible')

    context['pers_select'] = personne
    context['form'] = form
    context['type_opera'] = type_opera
    context['personnes'] = Personne.objects.all()
    context['select_link'] = 'sms'
    return render(request, 'index.html', context)


@login_required(login_url="user_login")
def notification_app_supprimer_personne(request, type_opera, pk):
    try:
        personne = Personne.objects.get(id=pk)
        personne.delete()
        messages.error(request, f"Supprission reuissie de {personne.nom_et_prenom}")
        return redirect('notification:notification_app_index')
    except Personne.DoesNotExist:
        return Http404('page non disponible')










