from django.urls import path
from . import views

urlpatterns = [
    # Pagine principali
    path('homepage/', views.homepage, name="homepage"),
    path('chi_siamo/', views.chi_siamo, name='chi_siamo'),
    path('attivita/', views.attivita_view, name='attivita'),

    # Prenotazioni
    path('prenota/', views.prenota, name='prenota'),
    path('riepilogo-prenotazione/', views.riepilogoprenotazione, name='riepilogoprenotazione'),
    path('gestisci-prenotazioni/', views.gestisci_prenotazioni, name='gestisci_prenotazioni'),
    path('verifica-disponibilita/<int:villa_id>/', views.verifica_disponibilita_view, name='verifica_disponibilita'),
    path('disponibilita/', views.disponibilita, name='disponibilita'),
    path('crea_prenotazione/', views.crea_prenotazione, name='crea_prenotazione'),

    # Utenti e autenticazione
    path('registrazione/', views.registrazione, name='registrazione'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Recensioni
    path('recensioni/', views.gestisci_recensioni, name='recensioni'),
    path('recensioni/aggiungi/', views.aggiungi_recensione, name='aggiungi_recensione'),

    # Contatti
    path('contattaci/', views.contattaci, name="contattaci"),
]
