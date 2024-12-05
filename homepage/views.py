from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from .models import Villa, Homepage
from .models import Recensione
from .models import Homepage
from .models import Booking
from datetime import date, datetime
from .forms import CustomUserCreationForm, RecensioneForm  # Assicurati di importare il tuo form

def homepage(request):
    immagini = Homepage.objects.all()
    return render(request, 'homepage/homepage.html', {'immagini': immagini})

def chi_siamo(request):
    return render(request, 'homepage/chi_siamo.html')

def prenota(request):
    return render(request, 'homepage/prenota.html')

def foto_gallery(request):
    return render(request, 'homepage/foto_gallery.html')

def contattaci(request):
    return render(request, 'homepage/contattaci.html')

def disponibilita(request):
    today = datetime.today().date()
    
    data_inizio = request.GET.get('dataInizio')
    data_fine = request.GET.get('dataFine')
    numero_persone = int(request.GET.get('numeroPersone', 1))

    if not data_inizio or not data_fine:
        return render(request, 'homepage/error.html', {'error': 'Date non valide!'})

    try:
        data_inizio_obj = datetime.strptime(data_inizio, "%Y-%m-%d").date()
        data_fine_obj = datetime.strptime(data_fine, "%Y-%m-%d").date()
    except ValueError:
        return render(request, 'homepage/error.html', {'error': 'Formato data non valido!'})

    # Validazione date
    if data_inizio_obj < today:
        return render(request, 'homepage/error.html', {'error': 'La data di inizio deve essere uguale o successiva a oggi!'})
    if data_fine_obj <= data_inizio_obj:
        return render(request, 'homepage/error.html', {'error': 'La data di fine deve essere successiva alla data di inizio!'})

    villa = Villa.objects.get(nomeVilla="Villa Murgo")

    prezzo_per_notte_base = 100
    prezzo_per_persona_aggiuntiva = 20

    if numero_persone > 1:
        prezzo_per_notte = prezzo_per_notte_base + (prezzo_per_persona_aggiuntiva * (numero_persone - 1))
    else:
        prezzo_per_notte = prezzo_per_notte_base

    giorni_totali = (data_fine_obj - data_inizio_obj).days
    prezzo_totale = prezzo_per_notte * giorni_totali

    # Salvataggio dei dati nella sessione
    request.session['checkin'] = data_inizio
    request.session['checkout'] = data_fine
    request.session['persone'] = numero_persone
    request.session['prezzo'] = prezzo_totale

    context = {
        'dataInizio': data_inizio,
        'dataFine': data_fine,
        'numeroPersone': numero_persone,
        'prezzoNotte': prezzo_per_notte,
        'giorniTotali': giorni_totali,
        'prezzoTotale': prezzo_totale
    }

    return render(request, 'homepage/disponibilita.html', context)

def registrazione_o_prenotazione(request, tipo="registrazione"):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['email']
            user.save()

            # Salva i dati corretti nella sessione
            request.session['email'] = form.cleaned_data['email']
            request.session['nome'] = form.cleaned_data['first_name']
            request.session['cognome'] = form.cleaned_data['last_name']

            if tipo == "prenotazione":
                return redirect('riepilogoprenotazione')  # Reindirizza al riepilogo della prenotazione
            else:
                login(request, user)  # Effettua il login automatico per la registrazione
                return redirect('homepage')
    else:
        form = CustomUserCreationForm()

    # Determina il contesto dinamico
    context = {
        'form': form,
        'titolo': "Prenotazione" if tipo == "prenotazione" else "Registrazione",
        'bottone': "Prosegui con la prenotazione" if tipo == "prenotazione" else "Registrati",
        'action': '/prenotazione/' if tipo == "prenotazione" else '/registrazione/',  # URL di destinazione
    }

    return render(request, 'homepage/registrazione.html', context)

def riepilogoprenotazione(request):

    # Recupera i dati dalla sessione
    nome = request.session.get('nome')
    cognome = request.session.get('cognome')
    email = request.session.get('email')

    # Recupera i dati dalla query string
    data_inizio = request.session.get('checkin')
    data_fine = request.session.get('checkout')
    numero_persone = request.session.get('persone')
    prezzo_totale = request.session.get('prezzo')

    context = {
        'data_inizio': data_inizio,
        'data_fine': data_fine,
        'numero_persone': numero_persone,
        'prezzo_totale': prezzo_totale,
        'nome': nome,
        'cognome': cognome,
        'email': email,
    }

    return render(request, 'homepage/riepilogoprenotazione.html', context)

@login_required
def gestisci_prenotazioni(request):
    prenotazioni = Booking.objects.filter(utente=request.user).order_by('-checkin')

    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        prenotazione = get_object_or_404(Booking, id=booking_id, utente=request.user)

        if 'delete' in request.POST:
            prenotazione.delete()
            messages.success(request, "Prenotazione cancellata con successo!")
            return redirect('gestisci_prenotazioni')

        elif 'edit' in request.POST:
            checkin = request.POST.get('checkin')
            checkout = request.POST.get('checkout')

            if checkin and checkout:
                prenotazione.checkin = checkin
                prenotazione.checkout = checkout
                prenotazione.save()
                messages.success(request, "Prenotazione aggiornata con successo!")
            else:
                messages.error(request, "Dati non validi. Riprova!")
            return redirect('gestisci_prenotazioni')

    return render(request, 'homepage/gestisci_prenotazioni.html', {'prenotazioni': prenotazioni})


def gestisci_recensioni(request):
    recensioni = Recensione.objects.order_by('-data_creazione')
    return render(request, 'homepage/recensioni.html', {'recensioni': recensioni})

def aggiungi_recensione(request):
    if request.method == 'POST':
        form = RecensioneForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('recensioni')  # Torna alla lista delle recensioni
    else:
        form = RecensioneForm()
    return render(request, 'homepage/aggiungi_recensione.html', {'form': form})



def logout(request):
    logout(request)
    return redirect('homepage')  # Reindirizza alla homepage dopo il logout

def login(request):
    return redirect(request, "login.html")

def verifica_disponibilita_view(request, villa_id):
    villa = get_object_or_404(Villa, id=villa_id)
    
    checkin = request.GET.get('checkin')
    checkout = request.GET.get('checkout')
    numero_persone = int(request.GET.get('persone', 1))  # Default a 1 persona
    prezzo_per_notte = villa.prezzo_base + (villa.prezzo_per_persona * numero_persone)
    
    if checkin and checkout:
        checkin_date = date.fromisoformat(checkin)
        checkout_date = date.fromisoformat(checkout)
        
        # Calcolare il numero di notti
        giorni_totali = (checkout_date - checkin_date).days
        
        # Calcolare il prezzo totale
        prezzo_totale = giorni_totali * prezzo_per_notte
        
        disponibilita = villa.verifica_disponibilita(checkin_date, checkout_date)
    else:
        disponibilita = None
        giorni_totali = prezzo_totale = 0

    return render(request, 'disponibilita.html', {
        'villa': villa,
        'disponibilita': disponibilita,
        'checkin': checkin,
        'checkout': checkout,
        'numeroPersone': numero_persone,
        'prezzoNotte': prezzo_per_notte,
        'prezzoTotale': prezzo_totale,
        'giorniTotali': giorni_totali,
        'dataInizio': checkin,
        'dataFine': checkout,
    })