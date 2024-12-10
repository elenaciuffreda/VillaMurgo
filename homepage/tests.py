from django.test import TestCase
from django.contrib.auth.models import User
from .models import Villa, Booking, Recensione, Attivita, Waitlist
from datetime import date


class RecensioneTestCase(TestCase):
    def setUp(self):
        # Creiamo una recensione
        self.recensione = Recensione.objects.create(
            nome='Test User',
            commento='Bella villa!',
            voto=5
        )

    def test_creazione_recensione(self):
        """Testa la creazione di una recensione"""
        recensione = Recensione.objects.get(nome='Test User')
        self.assertEqual(recensione.voto, 5)
        self.assertEqual(recensione.commento, 'Bella villa!')

class AttivitaTestCase(TestCase):
    def setUp(self):
        # Creiamo un'attività
        self.attivita = Attivita.objects.create(
            titolo='Escursione in montagna',
            descrizione='Un\'escursione panoramica in montagna.',
            immagine='attivita_pics/escursione.jpg'
        )

    def test_creazione_attivita(self):
        """Testa la creazione di un'attività"""
        attivita = Attivita.objects.get(titolo='Escursione in montagna')
        self.assertEqual(attivita.titolo, 'Escursione in montagna')
        self.assertEqual(attivita.descrizione, 'Un\'escursione panoramica in montagna.')

class WaitlistTestCase(TestCase):
    def setUp(self):
        # Creiamo un'iscrizione alla waitlist
        self.waitlist = Waitlist.objects.create(email='test@example.com')

    def test_creazione_waitlist(self):
        """Testa la creazione di una registrazione alla waitlist"""
        waitlist = Waitlist.objects.get(email='test@example.com')
        self.assertEqual(waitlist.email, 'test@example.com')

    def test_waitlist_email_unica(self):
        """Testa che un'email non possa essere duplicata nella waitlist"""
        with self.assertRaises(Exception):
            Waitlist.objects.create(email='test@example.com')
