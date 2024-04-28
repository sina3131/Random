from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Remove the username field from the user model
    # Use email as the primary identifier for the user
    email = models.EmailField(unique=True)
    username = models.CharField(default='',null=True, max_length=255)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    phone_number = PhoneNumberField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    img_profil = models.ImageField(default="default_profil.png")
    max_players = models.PositiveIntegerField(default=1)
 
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}   {self.email}"

class Groups(models.Model):
    group = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.group

class Player(models.Model):
    first_name = models.CharField(max_length=101)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    year_of_birth = models.IntegerField()
    img_player = models.ImageField(default="default_profil.png")
    group = models.ManyToManyField(Groups, related_name='player')
    customer = models.ForeignKey(
        User, null=True, on_delete=models.CASCADE, related_name='players')

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Location(models.Model):
    location = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.location

class Coach (models.Model):
    customer = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='coach')
    certified = models.BooleanField(default=False)

    def __str__(self) -> str:
      return str(self.customer)
    
class Payment_type(models.Model):
    name = models.CharField(max_length=100)
    price =  models.DecimalField(max_digits=8, decimal_places=2)
    short_description = models.CharField(max_length=100)
    description = models.TextField(default='')
    TYPE_CHOICES = [
        ('Once', 'Once'),
        ('Membership', 'Membership'),
        ('Package', 'Package')
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='Once')

    def __str__(self) -> str:
        return f"{self.name}: {self.price} {self.short_description}"

class Booking_Type(models.Model):
    pass_type = models.CharField(max_length=100)
    payment_types = models.ManyToManyField(Payment_type, related_name="booking_type")


    def __str__(self) -> str:
        return self.pass_type



class Booking(models.Model):
    coach = models.ManyToManyField(Coach, related_name='passes_coached')
    players = models.ManyToManyField(Player, related_name='passes_played')
    date = models.DateField()
    pass_type = models.ForeignKey(Booking_Type, on_delete=models.CASCADE, related_name='passes')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='passes')
    start_time = models.TimeField()
    end_time = models.TimeField()
    address = models.CharField(max_length=200)
    group = models.ManyToManyField(Groups, related_name='passes')
    max_players = models.PositiveIntegerField(default=6)


    def __str__(self) -> str:
        return f"{self.location}-  {self.date},    from {self.start_time} to {self.end_time}"

class PlayerBooking(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='bookings')
    pass_booked = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='bookings')

    def __str__(self) -> str:
        return f"{self.player.first_name} {self.player.last_name} - {self.pass_booked.date}"


class Payment(models.Model):
    player = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name='payments')
    player_booking = models.ForeignKey(
        PlayerBooking, on_delete=models.CASCADE, related_name='payments')
    payed_with_membership = models.BooleanField(default=False)
    payed_with_payment = models.BooleanField(default=False)
    payment_date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.player.first_name} {self.player.last_name} - {self.player_booking.pass_booked.date}"
    
class Camp(models.Model):
    name = models.CharField(max_length=150, default='')
    description = models.TextField(default='')
    img = models.ImageField(default='default_profil.png', upload_to='camp/')
    date = models.DateField(default='')
   

class Camp_register(models.Model):
    shirt_size = models.CharField(max_length=30,default='')
    parents_name = models.CharField(max_length=100,default='')
    social_security_nr = models.IntegerField(default='')
    
class Cups(models.Model):
    name = models.CharField(max_length=100, default='')
    description = models.TextField(default='')
    img = models.ImageField(default='default_profil.png', upload_to='camp/')
    date = models.DateField(default='')
    Location = models.CharField(max_length=100, default='')
    price = models.CharField(max_length=50, default='Gratis')

class Cup_register(models.Model):
      team_name = models.CharField(max_length=100, default='')
      team_captain = models.CharField(max_length=100, default='')
      age_younest_oldest_player = models.CharField(max_length=100, default='')
      name_of_all_players = models.TextField(max_length=500, default='')

class Prov_traning(models.Model):
    name = models.CharField(default= '', max_length=100)
    description = models.TextField(default='')
    price = models.CharField(default='Gratis',max_length=50)
    image = models.ImageField(default='default_profil.png', upload_to='camp/')

class Prov_traning_register(models.Model):
    name = models.CharField(default= '',max_length=100)
    age = models.IntegerField(default= '')
    phone = PhoneNumberField(default= '')
    parents_phone = PhoneNumberField(default='')
    current_team = models.CharField(default='',max_length=100)
    location= models.CharField(default='',max_length=100)
    day = models.DateField(default=None)
    time = models.TimeField(default=None)
    message = models.TextField(default='')
  
class Pt_traning(models.Model):
    name = models.CharField(default= '', max_length=100)
    description = models.TextField(default='')
    price = models.CharField(default='',max_length=50)
    image = models.ImageField(default='default_profil.png', upload_to='camp/')

class Group_traning(models.Model):
    name = models.CharField(default= '', max_length=100)
    description = models.TextField(default='')
    price = models.CharField(default='',max_length=50)
    image = models.ImageField(default='default_profil.png', upload_to='camp/')
