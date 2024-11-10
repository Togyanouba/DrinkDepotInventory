from django.contrib import admin
from .models import Article, EntreeStock, SortieStock

from django.core.exceptions import ValidationError

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('nom_article','prix_achat', 'prix_vente' ,'quantite' ,'categorie', 'modele')
    list_filter = ('modele', 'categorie')
    search_fields = ('nom_article', 'code_article')
    fields = ('nom_article', 'prix_achat', 'prix_vente', 'quantite', 'modele', 'categorie')
    list_editable = ('prix_vente', 'quantite')

@admin.register(EntreeStock)
class EntreeStockAdmin(admin.ModelAdmin):
    list_display = ('date_achat', 'numero_de_commande', 'nom_article', 'quantite', 'cout_total')
    list_filter = ('date_achat', 'nom_article')
    search_fields = ('numero_de_commande',)
    readonly_fields = ('cout_total',)

    def save_model(self, request, obj, form, change):
        if not change:  # Nouvelle entrée de stock
            obj.cout_total = obj.quantite * obj.nom_article.prix_achat
        obj.save()


@admin.register(SortieStock)
class SortieStockAdmin(admin.ModelAdmin):
    list_display = ('date_vente', 'client', 'nom_article', 'quantite', 'prix_total')
    list_filter = ('date_vente', 'nom_article')
    search_fields = ('client', 'nom_article__nom_article')
    readonly_fields = ('prix_total',)

    def save_model(self, request, obj, form, change):
        try:
            obj.full_clean()  # Appel à clean() pour vérifier les contraintes avant la sauvegarde
            super().save_model(request, obj, form, change)
        except ValidationError as e:
            form.add_error(None, e)