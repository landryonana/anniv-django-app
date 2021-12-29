from django.db import models
from django.utils.translation import gettext as _
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.utils.text import slugify



#override username(max_length, help_text), email(_unique) and password(max_length, help_text)
User._meta.get_field('username').validators[1].limit_value = 150
User._meta.get_field('email')._unique = True
User._meta.get_field('username').help_text = 'Obligatoire. 150 caractères ou moins. Lettres, chiffres et @/./+/-/_ uniquement.'
User._meta.get_field('password').help_text = 'Il doit contenir au moins 8 caractères.<br> Ne doit pas etre courant.<br> doit etre alphanuméric'



#==========Participants à l'évangelisation
class Personne(models.Model):
    SEXE = (
        ('masculin', 'Masculin'),
        ('féminin', 'Féminin')
    )
    nom_et_prenom = models.CharField(max_length=200, unique=True, 
        error_messages={'unique':"Une personne avec ce nom et\ou prénom existe déjà"})
    sexe = models.CharField(choices=SEXE, max_length=15, verbose_name='Sexe')
    telephone = models.PositiveIntegerField(unique=True, 
                error_messages={'unique':"Une personne avec ce numéro de télephone existe déjà"})
    date_naissance = models.DateField(auto_now=False, auto_now_add=False, 
        verbose_name="Date de naissance", help_text="la date doit etre sous format: <b>jour/mois/année</b>. Par ex:12/01/1885")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nom_et_prenom



#==========Profile utilisateur
class Profile(models.Model):
    SEXE = (
        ('masculin', 'Masculin'),
        ('féminin', 'Féminin')
    )
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True,  null=True)
    image = models.ImageField(upload_to='images/profile/%Y/', null=True, blank=True, help_text="ajouter une photo")
    phone = models.PositiveIntegerField(null=True, unique=True, blank=True, 
        help_text="le numéro de télephone doit avoir 9 chiffres",
        error_messages={'unique':"Une boss avec ce numéro de télephone existe déjà"})
    sexe = models.CharField(choices=SEXE, max_length=15, verbose_name='Sexe')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile de {self.user}"




































































