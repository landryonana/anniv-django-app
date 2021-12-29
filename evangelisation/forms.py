from django import forms

from evangelisation.models import Personne


#==================================================================================
#===========================Personne form
class PersonneForm(forms.ModelForm):
    class Meta:
        model = Personne
        fields = ['nom_et_prenom', 'telephone', 'sexe', 'date_naissance']

    def clean_nom_et_prenom(self):
        nom_et_prenom = self.cleaned_data['nom_et_prenom']
        if len(str(nom_et_prenom))<3:
            raise forms.ValidationError("Problème lors du remplissage du nom et prenom d'un participant : Le champ doit avoir au moins 03 caractères ")
        return nom_et_prenom
    
    def clean_telephone(self):
        telephone = self.cleaned_data['telephone']
        if len(str(telephone))!=9:
            raise forms.ValidationError("Le numéro de télephone est invalide")
        else:
            if len(str(telephone))==9:
                telephone_6 = str(telephone)[0]
                if int(telephone_6)!=6:
                    raise forms.ValidationError("Le numéro de télephone doit commencer par 6")
        return telephone



class FormNbre(forms.Form):
    formulaires = forms.IntegerField(label="Entrez le nombre de formulaire que vous voulez", help_text="le nombre de formulaire sera crée")



















































