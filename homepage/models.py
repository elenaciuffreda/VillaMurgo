from django.db import models
from django.contrib.auth.models import User

class Homepage(models.Model):
        immagine = models.ImageField()
        nome = models.CharField(max_length=20)
        descrizione = models.CharField(max_length=20)


        def __str__(self):
                return self.nome

class Villa(models.Model):
        nomeVilla = models.CharField(max_length=20)
        prezzo_base = models.DecimalField(max_digits=6, decimal_places=2)
        prezzo_per_persona = models.DecimalField(max_digits=6,decimal_places=2)

        def __str__(self):
                return self.nomeVilla
        
        def verifica_disponibilita(self, checkin, checkout):
                return not self.bookings.filter(
                        checkin__lt=checkout,
                        checkout__gt=checkin
                ).exists()
        
class Booking(models.Model):
    utente = models.ForeignKey(User, on_delete=models.CASCADE)
    villa = models.ForeignKey(Villa, on_delete=models.CASCADE, related_name='bookings')  
    checkin = models.DateField()
    checkout = models.DateField()
    numero_persone = models.PositiveIntegerField()
    prezzo_totale = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Prenotazione {self.id} - {self.utente.username}"



#Modello per le recensioni
class Recensione(models.Model):
    nome = models.CharField(max_length=100)
    commento = models.TextField()
    voto = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # Valutazione da 1 a 5
    data_creazione = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} - {self.voto}/5"
    
#Modello per le attività 
class Attivita(models.Model):
    titolo = models.CharField(max_length=200)
    descrizione = models.TextField()
    immagine = models.ImageField(upload_to='attivita_pics/', null=True, blank=True)

    def __str__(self):
        return self.titolo
