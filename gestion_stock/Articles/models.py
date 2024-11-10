from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver

class Article(models.Model):
    MODELE_CHOICES = (
        ('PM', 'Petit Modèle'),
        ('GM', 'Grand Modèle'),
    )
    
    CATEGORIE_CHOICES = (
        ('AL', 'Alcoolisé'),
        ('NA', 'Non Alcoolisé'),
    )

    nom_article = models.CharField(max_length=100)
    prix_achat = models.DecimalField(max_digits=10, decimal_places=2)
    prix_vente = models.DecimalField(max_digits=10, decimal_places=2)
    quantite = models.PositiveIntegerField()
    modele = models.CharField(max_length=2, choices=MODELE_CHOICES)
    categorie = models.CharField(max_length=2, choices=CATEGORIE_CHOICES)

    def __str__(self):
        return self.nom_article


class EntreeStock(models.Model):
    date_achat = models.DateField()
    numero_de_commande_base = models.PositiveIntegerField(help_text="Entrez le numéro de commande de base")
    numero_de_commande = models.CharField(max_length=20, blank=True, unique=True)
    nom_article = models.ForeignKey(Article, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    cout_total = models.DecimalField(max_digits=10, decimal_places=2)

    #Cette fonction permettra juste à l'utilisateur d'entrer une valeur spécifique comme  1 et le numero sera A0001-Année 
    def save(self, *args, **kwargs):
        if not self.numero_de_commande:
            current_year = timezone.now().year
            self.numero_de_commande = f'A{self.numero_de_commande_base:04d}-{current_year}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Commande {self.numero_de_commande} - {self.nom_article.nom_article}"
    


class SortieStock(models.Model):
    date_vente = models.DateField()
    client = models.CharField(max_length=100)
    nom_article = models.ForeignKey(Article, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    prix_total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def clean(self):
        article = Article.objects.get(id=self.nom_article.id)
        if self.pk:
            # Sortie existante (modification)
            sortie_initiale = SortieStock.objects.get(pk=self.pk)
            changement_quantite = self.quantite - sortie_initiale.quantite
        else:
            # Nouvelle sortie
            changement_quantite = self.quantite
        
        if changement_quantite > article.quantite:
            raise ValidationError("La quantité demandée est supérieure à la quantité en stock.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Appel à clean() pour vérifier les contraintes avant la sauvegarde
        article = Article.objects.get(id=self.nom_article.id)
        if self.pk:
            # Sortie existante (modification)
            sortie_initiale = SortieStock.objects.get(pk=self.pk)
            article.quantite += sortie_initiale.quantite  # Annuler la sortie précédente
        article.quantite -= self.quantite  # Appliquer la nouvelle sortie
        article.save()
        self.prix_total = self.quantite * self.nom_article.prix_vente
        super().save(*args, **kwargs)


@receiver(pre_delete, sender=SortieStock)
def ajouter_stock_a_la_suppression(sender, instance, **kwargs):
    article = Article.objects.get(id=instance.nom_article.id)
    article.quantite += instance.quantite
    article.save()
