from django.contrib import admin
from .models import Homepage, Villa, Recensione

admin.site.register(Homepage)

@admin.register(Villa)
class VillaAdmin(admin.ModelAdmin):
    list_display  = ('nomeVilla', 'prezzo_base', 'prezzo_per_persona')

@admin.register(Recensione)
class RecensioneAdmin(admin.ModelAdmin):
    list_display = ('nome', 'voto', 'commento')  # Mostra queste colonne nell'elenco
    search_fields = ('nome', 'commento')         # Aggiungi una barra di ricerca
    list_filter = ('voto',)                      # Aggiungi un filtro per voto
    actions = ['delete_selected']                 # Permetti di eliminare selezionando più recensioni
