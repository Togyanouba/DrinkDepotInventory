from django.shortcuts import render, redirect
from .forms import ArticleRegistration, EntreeStockForm, SortieStockForm
from .models import Article, EntreeStock, SortieStock

# Fonction d'ajout et d'affichage des articles
def add_show(request):
    if request.method == 'POST':
        fm = ArticleRegistration(request.POST)
        if fm.is_valid():
            na = fm.cleaned_data['nom_article']
            pa = fm.cleaned_data['prix_achat']
            pv = fm.cleaned_data['prix_vente']
            qte = fm.cleaned_data['quantite']
            mdl = fm.cleaned_data['modele']
            ctg = fm.cleaned_data['categorie']
            
            if pa < 0 or pv < 0 or qte < 0:
                error_message = "Les quantités et les prix ne doivent pas être négatifs."
                return render(request, 'Articles/addandshow.html', {'form': fm, 'art': Article.objects.all(), 'error_message': error_message})
            
            reg = Article(nom_article=na, prix_achat=pa, prix_vente=pv, quantite=qte, modele=mdl, categorie=ctg)
            reg.save()
    else:
        fm = ArticleRegistration()
    art = Article.objects.all()
    return render(request, 'Articles/addandshow.html', {'form': fm, 'art': art})

# Fonction de suppression d'un article dans un tableau
def delete_article(request, id=None):
    if id is not None:
        cible = Article.objects.get(id=id)
        cible.delete()
    return redirect('add_show')

def update_article(request, id):
    pi = Article.objects.get(pk=id)
    if request.method == 'POST':
        fm = ArticleRegistration(request.POST, instance=pi)
        if fm.is_valid():
            if fm.cleaned_data['prix_achat'] < 0 or fm.cleaned_data['prix_vente'] < 0 or fm.cleaned_data['quantite'] < 0:
                error_message = "Les quantités et les prix ne doivent pas être négatifs."
                return render(request, "Articles/updateArticle.html", {'form': fm, 'error_message': error_message})
            fm.save()
            return redirect('add_show')
    else:
        fm = ArticleRegistration(instance=pi)
    return render(request, "Articles/updateArticle.html", {'form': fm})


# Fonction d'ajout et d'affichage des entrées de stock
def add_show_entree_stock(request):
    if request.method == 'POST':
        fm = EntreeStockForm(request.POST)
        if fm.is_valid():
            entree_stock = fm.save(commit=False)
            article = entree_stock.nom_article

            if entree_stock.quantite <= 0:
                fm.add_error('quantite', 'La quantité doit être positive.')
            else:
                entree_stock.cout_total = entree_stock.quantite * article.prix_achat
                article.quantite += entree_stock.quantite
                article.save()
                entree_stock.save()
                return redirect('add_show_entree_stock')
    else:
        fm = EntreeStockForm()

    entrees = EntreeStock.objects.all()
    return render(request, 'stock/ajoutentreestock.html', {'form': fm, 'entrees': entrees})

# Fonction de modification d'une entrée de stock
def update_entree_stock(request, id):
    try:
        entree = EntreeStock.objects.get(pk=id)
    except EntreeStock.DoesNotExist:
        return redirect('add_show_entree_stock')

    article = entree.nom_article
    quantite_initiale = entree.quantite

    if request.method == 'POST':
        fm = EntreeStockForm(request.POST, instance=entree)
        if fm.is_valid():
            entree_stock = fm.save(commit=False)
            nouvelle_quantite = entree_stock.quantite

            if nouvelle_quantite <= 0:
                fm.add_error('quantite', 'La quantité doit être positive.')
            else:
                difference = nouvelle_quantite - quantite_initiale
                entree_stock.cout_total = nouvelle_quantite * article.prix_achat
                article.quantite += difference
                article.save()
                entree_stock.save()
                return redirect('add_show_entree_stock')
    else:
        fm = EntreeStockForm(instance=entree)

    entrees = EntreeStock.objects.all()
    return render(request, 'stock/update_entree_stock.html', {'form': fm, 'entrees': entrees})



# Suppression des entrées de stock
def delete_entree_stock(request, id=None):
    fm = EntreeStockForm()
    entrees = EntreeStock.objects.all()
    if id is not None:
        entree = EntreeStock.objects.get(id=id)
        article = entree.nom_article
        article.quantite -= entree.quantite
        article.save()
        entree.delete()
    return redirect('add_show_entree_stock')
    #return render(request, 'stock/ajoutentreestock.html', {'form': fm, 'entrees': entrees})

# Fonction d'ajout et d'affichage des sorties de stock
def add_show_sortie_stock(request):
    if request.method == 'POST':
        fm = SortieStockForm(request.POST)
        if fm.is_valid():
            sortie_stock = fm.save(commit=False)
            article = sortie_stock.nom_article

            if sortie_stock.quantite <= 0:
                fm.add_error('quantite', 'La quantité doit être positive.')
            elif sortie_stock.quantite > article.quantite:
                fm.add_error('quantite', 'La quantité demandée est supérieure à la quantité en stock.')
            else:
                sortie_stock.prix_total = sortie_stock.quantite * article.prix_vente
                article.quantite -= sortie_stock.quantite
                article.save()
                sortie_stock.save()
                return redirect('add_show_sortie_stock')
    else:
        fm = SortieStockForm()

    sorties = SortieStock.objects.all()
    return render(request, 'stock/ajoutsortiestock.html', {'form': fm, 'sorties': sorties})

# Fonction de modification d'une sortie de stock
def update_sortie_stock(request, id):
    try:
        sortie = SortieStock.objects.get(pk=id)
    except SortieStock.DoesNotExist:
        return redirect('add_show_sortie_stock')

    article = sortie.nom_article
    quantite_initiale = sortie.quantite

    if request.method == 'POST':
        fm = SortieStockForm(request.POST, instance=sortie)
        if fm.is_valid():
            sortie_stock = fm.save(commit=False)
            nouvelle_quantite = sortie_stock.quantite

            if nouvelle_quantite <= 0:
                fm.add_error('quantite', 'La quantité doit être positive.')
            else:
                difference = nouvelle_quantite - quantite_initiale
                if difference > article.quantite:
                    fm.add_error('quantite', 'La quantité demandée est supérieure à la quantité en stock.')
                else:
                    sortie_stock.prix_total = nouvelle_quantite * article.prix_vente
                    article.quantite -= difference
                    article.save()
                    sortie_stock.save()
                    return redirect('add_show_sortie_stock')
    else:
        fm = SortieStockForm(instance=sortie)

    sorties = SortieStock.objects.all()
    return render(request, 'stock/update_sortie_stock.html', {'form': fm, 'sorties': sorties})

# Fonction de suppression d'une sortie de stock
def delete_sortie_stock(request, id=None):
    if id is not None:
        sortie = SortieStock.objects.get(id=id)
        article = sortie.nom_article
        article.quantite = article.quantite + sortie.quantite
        article.save()
        sortie.delete()
    return redirect('add_show_sortie_stock')


# # Fonction d'ajout et d'affichage des sorties de stock
# def add_show_sortie_stock(request):
#     if request.method == 'POST':
#         fm = SortieStockForm(request.POST)
#         if fm.is_valid():
#             sortie_stock = fm.save(commit=False)
#             article = sortie_stock.nom_article

#             if sortie_stock.quantite <= 0:
#                 fm.add_error('quantite', 'La quantité doit être positive.')
#             elif sortie_stock.quantite > article.quantite:
#                 fm.add_error('quantite', 'La quantité demandée est supérieure à la quantité en stock.')
#             else:
#                 sortie_stock.prix_total = sortie_stock.quantite * article.prix_vente
#                 article.quantite -= sortie_stock.quantite
#                 article.save()
#                 sortie_stock.save()
#                 return redirect('add_show_sortie_stock')
#     else:
#         fm = SortieStockForm()

#     sorties = SortieStock.objects.all()
#     return render(request, 'stock/ajoutsortiestock.html', {'form': fm, 'sorties': sorties})

# # Fonction de modification d'une sortie de stock
# def update_sortie_stock(request, id):
#     try:
#         sortie = SortieStock.objects.get(pk=id)
#     except SortieStock.DoesNotExist:
#         return redirect('add_show_sortie_stock')

#     article = sortie.nom_article
#     quantite_initiale = sortie.quantite

#     if request.method == 'POST':
#         fm = SortieStockForm(request.POST, instance=sortie)
#         if fm.is_valid():
#             nouvelle_quantite = fm.cleaned_data['quantite']

#             if nouvelle_quantite <= 0:
#                 fm.add_error('quantite', 'La quantité doit être positive.')
#             elif nouvelle_quantite > article.quantite + quantite_initiale:
#                 fm.add_error('quantite', 'La quantité demandée est supérieure à la quantité en stock.')
#             else:
#                 difference = quantite_initiale - nouvelle_quantite
#                 sortie_stock = fm.save(commit=False)
#                 sortie_stock.prix_total = nouvelle_quantite * article.prix_vente
#                 article.quantite += difference
#                 article.save()
#                 sortie_stock.save()
#                 return redirect('add_show_sortie_stock')
#     else:
#         fm = SortieStockForm(instance=sortie)

#     return render(request, 'stock/update_sortie_stock.html', {'form': fm})

# # Suppression des sorties de stock
# def delete_sortie_stock(request, id=None):
#     fm = SortieStockForm()
#     sorties = SortieStock.objects.all()
#     if id is not None:
#         sortie = SortieStock.objects.get(id=id)
#         article = sortie.nom_article
#         article.quantite += sortie.quantite
#         article.save()
#         sortie.delete()
#         return redirect('add_show_sortie_stock')
#     return render(request, 'stock/ajoutsortiestock.html', {'form': fm, 'sorties': sorties})

