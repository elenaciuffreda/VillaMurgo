from django.urls import path 
from . import views
#Imposto l'url specifico
urlpatterns = [
    path('homepage/', views.homepage,name="homepage"),
    path('chi_siamo/', views.chi_siamo,  name='chi_siamo'),
    path('prenota/', views.prenota, name='prenota'),
    path('foto_gallery/', views.foto_gallery, name="foto_gallery"),
    path('contattaci/', views.contattaci,name="contattaci"),
    path('disponibilita/', views.disponibilita, name='disponibilita'),
    path('registrazione/', views.registrazione_o_prenotazione, {'tipo': 'registrazione'}, name='registrazione'),
    path('prenotazione/', views.registrazione_o_prenotazione, {'tipo': 'prenotazione'}, name ='prenotazione'),
    path('riepilogo-prenotazione/', views.riepilogoprenotazione, name='riepilogoprenotazione'),
    path('recensioni/', views.gestisci_recensioni, name='recensioni'),  
    path('recensioni/aggiungi/', views.aggiungi_recensione, name='aggiungi_recensione'),
    path('gestisci-prenotazioni/', views.gestisci_prenotazioni, name='gestisci_prenotazioni'),
    path('logout/', views.logout, name='logout'),
    path('login/', views.login, name='login')
]
