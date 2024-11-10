from django.contrib import admin
from django.urls import path
from Articles import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.add_show, name="add_show"),
    path('delete_article/<int:id>', views.delete_article, name="delete_article"),
    path('<int:id>', views.update_article, name="update_article"),
    path('stock/', views.add_show_entree_stock, name="add_show_entree_stock"),
    path('stock/delete_entree/<int:id>', views.delete_entree_stock, name="delete_entree_stock"),
    path('stock/update_entree/<int:id>', views.update_entree_stock, name="update_entree_stock"),
    path('sortie/', views.add_show_sortie_stock, name="add_show_sortie_stock"),
    path('sortie/update/<int:id>/', views.update_sortie_stock, name="update_sortie_stock"),
    path('sortie/delete/<int:id>/', views.delete_sortie_stock, name="delete_sortie_stock"),
]
