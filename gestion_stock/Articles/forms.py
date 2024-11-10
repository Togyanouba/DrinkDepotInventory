from django.core import validators
from django import forms 
from .models import *

class ArticleRegistration(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['nom_article', 'prix_achat','prix_vente', 'quantite', 'modele', 'categorie']
        widgets = {
            'nom_article': forms.TextInput(attrs={'class': 'form-control'}),
            'prix_achat': forms.NumberInput(attrs={'class': 'form-control'}),
            'prix_vente': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control'}),
            #'modele': forms.MultipleChoiceField(choices=[ ('PM', 'Petit Modèle'),('GM', 'Grand Modèle')],attrs={'class': 'form-control'}),
            #'categorie': forms.TextInput(attrs={'class': 'form-control'}),
            
        }

#Formulaire d'entrée de stock 

class EntreeStockForm(forms.ModelForm):
    class Meta:
        model = EntreeStock
        fields = ['date_achat', 'numero_de_commande_base', 'nom_article', 'quantite']
        widgets = {
            'date_achat': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'numero_de_commande_base': forms.NumberInput(attrs={'class': 'form-control'}),
            'nom_article': forms.Select(attrs={'class': 'form-control'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'numero_de_commande_base': 'Entrez le numéro de commande de base, par exemple 1 pour A0001-2024.',
        }

#Formulaire d'insertion des sorties de stock

class SortieStockForm(forms.ModelForm):
    class Meta:
        model = SortieStock
        fields = ['date_vente', 'client', 'nom_article', 'quantite']
        widgets = {
            'date_vente': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'client': forms.TextInput(attrs={'class': 'form-control'}),
            'nom_article': forms.Select(attrs={'class': 'form-control'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }
        labels = {
            'date_vente': 'Date de vente',
            'client': 'Client',
            'nom_article': 'Nom de l\'article',
            'quantite': 'Quantité',
        }
        help_texts = {
            'quantite': 'La quantité doit être positive et ne doit pas dépasser la quantité en stock.',
        }