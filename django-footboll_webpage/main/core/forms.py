from django.forms import 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import Booking_Type, Player, User, Groups, Camp_register, Camp, Prov_traning_register,Cups, Cup_register, Prov_traning, Pt_traning,Payment_type, Booking
from datetime import datetime


from django.utils.translation import gettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField
from datetime import date

class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True, label=_('First name'))
    last_name = forms.CharField(max_length=100, required=True, label=_('Last name'))

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password1", "password2"]
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("This email is already taken."))
        return email

class UpdateUserForm(forms.Form):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    phone_number = PhoneNumberField(required=False)
    img_profile = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['email'].initial = user.email
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['address'].initial = user.address
            self.fields['phone_number'].initial = user.phone_number

    def save(self, user):
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.address = self.cleaned_data.get('address')
        user.phone_number = self.cleaned_data.get('phone_number')
        if self.cleaned_data.get('img_profile'):
            user.img_profil.save(self.cleaned_data['img_profile'].name, self.cleaned_data['img_profile'])
        user.save()

class CampRegisterationForm(forms.ModelForm):
    class Meta:
        model = Camp_register

        fields = ['shirt_size','parents_name','social_security_nr']
   

class CampCreationForm(forms.ModelForm):
    img = FileField(required=True)
    class Meta:
        model = Camp
        fields = ['name','description','date', 'img']


class CupRegisterationForm(forms.ModelForm):
    class Meta:
        model = Cup_register
        fields = ['team_name','team_captain','age_younest_oldest_player', 'name_of_all_players']
   

class Cup_CreationForm(forms.ModelForm):
    img = FileField(required=True)
    class Meta:
        model = Cups
        fields = ['name','description','date', 'img', 'Location', 'price']
  

class BookingTypeForm(forms.ModelForm):
    class Meta:
        model = Booking_Type
        fields = ['pass_type', 'payment_types']

class PaymentTypes(forms.ModelForm):
    class Meta:
        model = Payment_type
        fields = ['name', 'price', 'short_description', 'description', 'type']



class Prov_traningForm(forms.ModelForm):
    class Meta:
        model = Prov_traning
        fields = ['name', 'description', 'image','price']


class Prov_traning_RegisterForm(forms.ModelForm):
    class Meta:
        model = Prov_traning_register
        fields = ['name','age','phone','parents_phone','current_team','location','day','time','message']

# class Pt_traningForm(forms.ModelForm):
#     class Meta:
#         model = Pt_traning
#         fields = ['name', 'description', 'image','price']


class Boka_passForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['coach', 'players', 'date','pass_type','location','start_time','end_time','address','group']


class PlayerForm(forms.ModelForm):
    max_birth_year = date.today().year - 6
    min_birth_year = date.today().year - 70
    YEAR_CHOICES = [(year, year) for year in range(max_birth_year, min_birth_year, -1)]
    year_of_birth = forms.IntegerField(widget=forms.Select(choices=YEAR_CHOICES), 
                                       required=True, min_value=min_birth_year,
                                        max_value=max_birth_year)
    class Meta:
        model = Player
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'year_of_birth', 'img_player']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if field != 'img_player':
                field.required = True

        if user:
            self.fields['email'].initial = user.email
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['phone_number'].initial = user.phone_number
    
    def save(self, user):
        player = super().save(commit=False)
        player.first_name = self.cleaned_data['first_name']
        player.last_name = self.cleaned_data['last_name']
        player.email = self.cleaned_data['email']
        player.phone_number = self.cleaned_data['phone_number']
        player.customer = user
        player.save()
        birth_year = self.cleaned_data['year_of_birth']
        group, create = get_group(birth_year)
        player.group.add(group)
        player.year_of_birth = birth_year
        img_player = self.cleaned_data.get('img_player')
        print("img",img_player)
        if img_player:
            if not isinstance(img_player, InMemoryUploadedFile):
                player.img_player = img_player
            else:
                player.img_player.save(img_player.name, img_player)
        player.save()
        return player
         

class UpdatePlayerForm(forms.Form):
    email = forms.EmailField()
    phone_number = PhoneNumberField(required=False)
    img_player = forms.ImageField(required=False)
    max_birth_year = date.today().year - 6
    min_birth_year = date.today().year - 70
    YEAR_CHOICES = [(year, year) for year in range(max_birth_year, min_birth_year, -1)]
    year_of_birth = forms.IntegerField(widget=forms.Select(choices=YEAR_CHOICES), 
                                       required=True, min_value=min_birth_year,
                                        max_value=max_birth_year)

    def save(self, player):
        player.email = self.cleaned_data['email']
        birth_year = self.cleaned_data.get('year_of_birth')
        if player.year_of_birth != birth_year:
            group, create = get_group(birth_year)
            groups = player.group.all()
            for any_group in groups:
                if len(any_group) == 5 and any_group[0] in ["+", "-"]:
                    player.group.remove(any_group)
            player.group.add(group)
        player.year_of_birth = birth_year
        player.phone_number = self.cleaned_data.get('phone_number')
        if self.cleaned_data.get('img_player'):
            player.img_player.save(self.cleaned_data['img_player'].name, self.cleaned_data['img_player'])
        player.save()

def get_group(player_year):
    current_year = datetime.now().year
    print("year",current_year)
    age = current_year - player_year
    if age < 10:
        return Groups.objects.get_or_create(group="-" + str(current_year-10))
    elif age < 12:
        return Groups.objects.get_or_create(group="+" + str(current_year-10))
    elif age < 14:
        return Groups.objects.get_or_create(group="+" + str(current_year-12))
    elif age < 17:
        return Groups.objects.get_or_create(group="+" + str(current_year-14))
    else:
        return Groups.objects.get_or_create(group="+" + str(current_year-17))
    
class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking
        fields = ['coach', 'players', 'date', 'pass_type', 'location', 'start_time', 'end_time', 'max_players', 'address', 'group']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if field != 'players':
                field.required = False