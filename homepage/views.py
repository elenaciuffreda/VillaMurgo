from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from .models import Villa, Homepage
from .models import Recensione
from .models import Homepage
from .models import Booking
from .models import Attivita
from datetime import date, datetime
from .forms import CustomUserCreationForm, RecensioneForm  

def homepage(request):
    immagini = Homepage.objects.all()
    return render(request, 'homepage/homepage.html', {'immagini': immagini})

def chi_siamo(request):
    attivita_list = Attivita.objects.all()  
    return render(request, 'homepage/chi_siamo.html', {'attivita_list': attivita_list})

def prenota(request):
    return render(request, 'homepage/prenota.html')

def contattaci(request):
    return render(request, 'homepage/contattaci.html')

def disponibilita(request):
    today = datetime.today().date()
    data_inizio = request.GET.get('dataInizio')
    data_fine = request.GET.get('dataFine')
    numero_persone = int(request.GET.get('numeroPersone', 1))

    disponibile = False

    if not data_inizio or not data_fine:
        return render(request, 'homepage/error.html', {'error': 'Date non valide!'})

    try:
        data_inizio_obj = datetime.strptime(data_inizio, "%Y-%m-%d").date()
        data_fine_obj = datetime.strptime(data_fine, "%Y-%m-%d").date()
    except ValueError:
        return render(request, 'homepage/error.html', {'error': 'Formato data non valido!'})

    if data_inizio_obj < today:
        return render(request, 'homepage/error.html', {'error': 'La data di inizio deve essere uguale o successiva a oggi!'})
    if data_fine_obj <= data_inizio_obj:
        return render(request, 'homepage/error.html', {'error': 'La data di fine deve essere successiva alla data di inizio!'})

    villa = Villa.objects.get(nomeVilla="Villa Murgo")
    
    # Verifica disponibilità
    disponibile = villa.verifica_disponibilita(data_inizio_obj, data_fine_obj)
    print(disponibile)

    if not disponibile:
        return render(request, 'homepage/error.html', {'error': 'La villa non è disponibile per le date selezionate.'})

    # Calcolo del prezzo
    prezzo_per_notte_base = 100
    prezzo_per_persona_aggiuntiva = 20
    prezzo_per_notte = prezzo_per_notte_base + (prezzo_per_persona_aggiuntiva * (numero_persone - 1))
    giorni_totali = (data_fine_obj - data_inizio_obj).days
    prezzo_totale = prezzo_per_notte * giorni_totali

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
        'prezzoTotale': prezzo_totale,
        'disponibile': disponibile, 
    }

    return render(request, 'homepage/disponibilita.html', context)

def registrazione(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['email']
            user.is_staff = False
            user.is_superuser = False
            user.save()

            auth_login(request, user)
            
              # Salvataggio dei dati nella sessione
            request.session['email'] = form.cleaned_data['email']
            request.session['nome'] = form.cleaned_data['first_name']
            request.session['cognome'] = form.cleaned_data['last_name']

            # Recupera i dati della prenotazione dalla query string
            checkin = request.GET.get('checkin')
            checkout = request.GET.get('checkout')
            persone = request.GET.get('persone')
            prezzo = request.GET.get('prezzo')

            # Log per verificare i parametri dell'URL
            print(f"URL Parametri - Checkin: {checkin}, Checkout: {checkout}, Persone: {persone}, Prezzo: {prezzo}")

            # Salva questi dati nella sessione
            if checkin and checkout and persone and prezzo:
                request.session['checkin'] = checkin
                request.session['checkout'] = checkout
                request.session['persone'] = persone
                request.session['prezzo'] = prezzo

            # Verifica i dati della sessione prima di redirigere
            print(f"Sessione dopo il salvataggio: Checkin: {request.session.get('checkin')}, Checkout: {request.session.get('checkout')}, Persone: {request.session.get('persone')}, Prezzo: {request.session.get('prezzo')}")

            return redirect('riepilogoprenotazione')
    else:
        form = CustomUserCreationForm()

    return render(request, 'homepage/registrazione.html', {
        'form': form,
        'bottone': 'Registrati',
        'titolo': 'Registrazione'})


def riepilogoprenotazione(request):
    nome = request.session.get('nome')
    cognome = request.session.get('cognome')
    email = request.session.get('email')
    data_inizio = request.session.get('checkin')
    data_fine = request.session.get('checkout')
    numero_persone = request.session.get('persone')
    prezzo_totale = request.session.get('prezzo')

    # Log per vedere lo stato della sessione
    print(f"Sessione - Checkin: {data_inizio}, Checkout: {data_fine}, Persone: {numero_persone}, Prezzo: {prezzo_totale}")

    # Verifica che i dati della prenotazione siano disponibili
    if not all([data_inizio, data_fine, numero_persone, prezzo_totale]):
        messages.error(request, "Dati della prenotazione non disponibili!")
        return redirect('homepage')

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
    # Recupera tutte le prenotazioni (booking) dell'utente loggato
    bookings = Booking.objects.filter(utente=request.user).order_by('-checkin')
    print(f"Booking trovati: {bookings}")  # Debug per controllare i risultati

    if request.method == 'POST':
        # Ottieni l'ID del booking dalla richiesta POST
        booking_id = request.POST.get('booking_id')
        booking = get_object_or_404(Booking, id=booking_id, utente=request.user)

        if 'delete' in request.POST:
            # Elimina il booking
            booking.delete()
            messages.success(request, "Prenotazione cancellata con successo!")
        
        elif 'edit' in request.POST:
            # Ottieni le nuove date per modificare il booking
            checkin = request.POST.get('checkin')
            checkout = request.POST.get('checkout')

            # Controlla se le date sono valide
            if checkin and checkout:
                try:
                    # Converti le date in oggetti `date`
                    checkin = datetime.strptime(checkin, '%Y-%m-%d').date()
                    checkout = datetime.strptime(checkout, '%Y-%m-%d').date()

                    # Controlla se la data di check-in è prima di quella di check-out
                    if checkin < checkout:
                        booking.checkin = checkin
                        booking.checkout = checkout
                        booking.save()
                        messages.success(request, "Prenotazione aggiornata con successo!")
                    else:
                        messages.error(request, "La data di check-in deve essere prima della data di check-out.")
                except ValueError:
                    messages.error(request, "Le date non sono nel formato corretto. Usa il formato YYYY-MM-DD.")
            else:
                messages.error(request, "Le date di check-in e check-out sono obbligatorie.")

        return redirect('gestisci_prenotazioni')

    # Renderizza la pagina con i booking dell'utente
    return render(request, 'homepage/gestisci_prenotazioni.html', {'prenotazioni': bookings})

def gestisci_cancellazione(request, prenotazione):
    prenotazione.delete()
    messages.success(request, "Prenotazione cancellata con successo!")
    return redirect('gestisci_prenotazioni')

def gestisci_modifica(request, prenotazione):
    checkin = request.POST.get('checkin')
    checkout = request.POST.get('checkout')

    if checkin and checkout:
        checkin_date = datetime.strptime(checkin, '%Y-%m-%d').date()
        checkout_date = datetime.strptime(checkout, '%Y-%m-%d').date()

        if checkin_date < checkout_date:
            if prenotazione.villa.verifica_disponibilita(checkin_date, checkout_date):
                prenotazione.checkin = checkin_date
                prenotazione.checkout = checkout_date
                prenotazione.save()
                messages.success(request, "Prenotazione aggiornata con successo!")
            else:
                messages.error(request, "Le nuove date non sono disponibili per questa villa.")
        else:
            messages.error(request, "La data di check-out deve essere successiva alla data di check-in.")
    else:
        messages.error(request, "Le date non sono valide. Controlla e riprova.")

    return redirect('gestisci_prenotazioni')

@login_required
def crea_prenotazione(request):
    # Recupera i dati dalla sessione
    nome = request.session.get('nome')
    cognome = request.session.get('cognome')
    email = request.session.get('email')
    checkin = request.session.get('checkin')
    checkout = request.session.get('checkout')
    persone = request.session.get('persone')
    prezzo = request.session.get('prezzo')

    print(f"Checkin: {checkin}, Checkout: {checkout}, Persone: {persone}, Prezzo: {prezzo}")

    if all([checkin, checkout, persone, prezzo]):
        villa = Villa.objects.first()  # Recupero villa
        if not villa:
            messages.error(request, "Nessuna villa disponibile per la prenotazione.")
            return redirect('homepage')

        booking = Booking.objects.create(
            utente=request.user,  # Utente loggato
            villa=villa,          # Unica villa
            checkin=checkin,
            checkout=checkout,
            numero_persone=persone,
            prezzo_totale=prezzo
        )

        messages.success(request, 'Prenotazione confermata con successo!')
        return redirect('gestisci_prenotazioni')
    else:
        messages.error(request, 'Dati mancanti, impossibile confermare la prenotazione.')
        return redirect('riepilogoprenotazione')


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

def user_logout(request):
    logout(request)
    return redirect('homepage')  # Reindirizza alla homepage dopo il logout

def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():

            user = form.get_user()

            auth_login(request, user)
            return redirect('homepage')  # Redirigi alla home dopo il login
        else:
            messages.error(request, "Nome utente o password errati.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'homepage/login.html', {'form': form})

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

def attivita_view (request): 
     return render(request, 'homepage/attivita.html')