# Sistema di Prenotazione Villa - Progetto Django

## Descrizione

Questo progetto sviluppato con **Django** è un sistema di prenotazione online che consente agli utenti di prenotare una villa per un determinato periodo di tempo. L'applicazione include funzionalità come la gestione delle prenotazioni, la visualizzazione della disponibilità della villa, le recensioni degli utenti, attività disponibili e una lista d'attesa per i casi di villa non disponibile.

## Funzionalità

- **Prenotazioni**: Gli utenti possono prenotare una villa specificando le date desiderate.
- **Gestione della disponibilità**: Il sistema verifica la disponibilità della villa in base alle date di prenotazione.
- **Recensioni e attività**: Gli utenti possono lasciare recensioni e visualizzare le attività disponibili presso la villa.
- **Lista d'attesa**: Se la villa è occupata, gli utenti possono essere aggiunti a una lista d'attesa e verranno notificati quando la villa diventa disponibile.
- **Sistema di notifiche**: Gli utenti ricevono notifiche automatiche per promemoria relativi alla disponibilità della villa.

## Tecnologie Utilizzate

- **Django**: Framework principale per lo sviluppo web.
- **Python 3.7**: Linguaggio di programmazione utilizzato per il backend.
- **SQLite**: Database utilizzato per il progetto (può essere facilmente sostituito con altri sistemi di database come PostgreSQL).

## Installazione
Clona il repository:

   git clone https://github.com/elenaciuffreda/VillaMurgo

Una volta clonato, aprire il progetto nel proprio IDE e lanciare il seguente comando da terminale:
   python manage.py runserver
Una volta lanciato verrà visualizzato nel terminale un link che avrà la seguente forma
http://127.0.0.1:8000

Aggiungere al seguente link: /homepage/
Il link quindi dovrà avere questa forma: http://127.0.0.1:8000/homepage/
