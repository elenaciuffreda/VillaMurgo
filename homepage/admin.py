from django.contrib import admin
from .models import Homepage, Villa, Recensione, Attivita, Booking, Waitlist



admin.site.register(Homepage)

admin.site.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('utente', 'checkin', 'checkout', 'prezzo_totale', 'numero_persone')
    list_filter = ('utente', 'checkin', 'checkout')
    search_fields = ('utente__username',)

@admin.register(Villa)
class VillaAdmin(admin.ModelAdmin):
    list_display  = ('nomeVilla', 'prezzo_base', 'prezzo_per_persona')

@admin.register(Recensione)
class RecensioneAdmin(admin.ModelAdmin):
    list_display = ('nome', 'voto', 'commento')  # Mostra queste colonne nell'elenco
    search_fields = ('nome', 'commento')         # Aggiungi una barra di ricerca
    list_filter = ('voto',)                      # Aggiungi un filtro per voto
    actions = ['delete_selected']                 # Permetti di eliminare selezionando più recensioni

@admin.register(Attivita)
class AttivitaAdmin(admin.ModelAdmin):
    list_display = ('titolo', 'descrizione', 'immagine')  # Mostra nella lista
    search_fields = ('titolo',)  # Aggiungi una barra di ricerca
    list_filter = ('titolo',)  # Aggiungi un filtro per il titolo



@admin.register(Waitlist)
class WaitlistAdmin(admin.ModelAdmin):
    list_display = ('email', 'data_iscrizione')  # Visualizza la colonna email e data di iscrizione
    search_fields = ('email',)  # Permette di cercare gli utenti per email
    list_filter = ('data_iscrizione',)  # Filtro per data di iscrizione
    ordering = ('-data_iscrizione',)  # Ordina in modo decrescente in base alla data di iscrizione
