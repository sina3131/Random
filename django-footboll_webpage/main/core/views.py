
from django.shortcuts import render, redirect, redirect, get_object_or_404
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_users, is_superuser
from datetime import datetime
import json
from .models import *
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.template.loader import render_to_string



from .chatbot import get_response

from django.http import JsonResponse

def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message', '')
        response = get_response(message)
        return JsonResponse({'response': response})
    else:
        return render(request, 'chat.html')
    


# def get_bot_response(request):
#     user_message = request.GET.get('msg', '')
#     bot_response = traning.get_response(user_message)

#     data = {
#         'response': bot_response,
#     }

#     return JsonResponse(data)

def boka_pass(request):
    session = Booking.objects.all()
    context = {
        'session': session
    }
    return render(request, 'boka_pass.html', context)



def offside(request):
    return render(request, 'offside.html')


def camps(request):
    camp = Camp.objects.all()
    context = {
        'camp': camp
    }
    return render(request, 'camp.html', context)


def camp_detail(request, pk):
    camp = Camp.objects.get(pk=pk)
    context = {
        'camp': camp
    }
    return render(request, 'camp_detail.html', context)



def cups(request):
    cup = Cups.objects.all()
    context = {
        'cup': cup
    }
    return render(request, 'cups.html', context)


def cups_detail(request, pk):
    cup = Cups.objects.get(pk=pk)
    context = {
        'cup': cup
    }
    return render(request, 'cups.detail.html', context)

def prov_traning(request):
    traning = Prov_traning.objects.all()
    context = {
        'traning': traning
    }
    return render(request, 'prov_traning.html', context)

def pt_traning(request):
    traning_pt = Pt_traning.objects.all()
    context = {
        'traning_pt': traning_pt
    }
    return render(request, 'pt_traning.html', context)

def group_traning(request):
    traning_group = Group_traning.objects.all()
    context = {
        'traning_group': traning_group
    }
    return render(request, 'group_traning.html', context)


@login_required
def boka_pass_register(request):
    form_pass = Boka_passForm()
    if request.method == "POST":
        form_pass = Boka_passForm(request.POST)
        if form_pass.is_valid():
            form_pass.save()
            data = form_pass.cleaned_data
            messages.success(request, f" {data['pass_type']} registerd ")
            message = f"""Pass registraion approved for {data['players']} """
            group, created = Group.objects.get_or_create(name='pass')
            # user.groups.add(group)
            send_mail('Pass registration', message, 'settings.EMAIL_HOST_USER',[settings.CONTACT_EMAIL], fail_silently=False)
            return redirect("login")
    error_messages = [error[0] for error in form_pass.errors.values()]
    content = {'form_pass': form_pass, 'errors':error_messages}
    return render(request, "boka_pass_register.html",  content)

@login_required
def prov_traning_register(request):
    form_prov = Prov_traning_RegisterForm()
    if request.method == "POST":
        form_prov = Prov_traning_RegisterForm(request.POST)
        if form_prov.is_valid():
            form_prov.save()
            data = form_prov.cleaned_data
            messages.success(request, f" {data['name']} registerd for the prov training")
            message = f"""Prov training registraion approved for {data['name']} """
            group, created = Group.objects.get_or_create(name='cup')
            # user.groups.add(group)
            send_mail('Prov Traning registration', message, 'settings.EMAIL_HOST_USER',[settings.CONTACT_EMAIL], fail_silently=False)
            return redirect("login")
    error_messages = [error[0] for error in form_prov.errors.values()]
    content = {'form_prov': form_prov, 'errors':error_messages}
    return render(request, "prov_traning_register.html",  content)

@login_required(login_url='login')
def registerPage_cup(request):
    form_3 = CupRegisterationForm()
    if request.method == "POST":
        form_3 = CupRegisterationForm(request.POST)
        if form_3.is_valid():
            form_3.save()
            data = form_3.cleaned_data
            messages.success(request, f" {data['team_name']} registerd for the cup")
            message = f"""Cup registraion approved for {data['team_name']} """
            group, created = Group.objects.get_or_create(name='cup')
            # user.groups.add(group)
            send_mail('Cup registration', message, 'settings.EMAIL_HOST_USER',[settings.CONTACT_EMAIL], fail_silently=False)
            return redirect("login")
    error_messages = [error[0] for error in form_3.errors.values()]
    content = {'form_3': form_3, 'errors':error_messages}
    return render(request, "register_cup.html",  content)


@login_required(login_url='login')
def create_cup(request):
    form_4 = Cup_CreationForm()
    if request.method == 'POST':
        form_4 = Cup_CreationForm(request.POST, request.FILES) # <-- pass request.FILES to handle the uploaded file
        if form_4.is_valid():
            cup = form_4.save(commit=False)
            cup.img = request.FILES.get('img') # <-- get the uploaded image and assign it to the img field
            cup.save()
            data_1 = form_4.cleaned_data
            messages.success(request, f" {data_1['name']} cupp created ")
            message = f""" Cup {data_1['name']} sucessfully has been created"""
            group, created = Group.objects.get_or_create(name ='Create_cup' )
            # user_1.groups.add(group)
            send_mail('The cup has been created sucessfully', message, 'settings.EMAIL_HOST_USER', [settings.CONTACT_EMAIL], fail_silently=False )
            return redirect("login")
        else:
            print(form_4.errors)
    error_messages = [error[0] for error in form_4.errors.values()]
    content = {'form_4': form_4, 'errors':error_messages}
    return render(request, "create_cup.html", content)


@login_required(login_url='login')
def registerPage_camp(request):
    form_1 = CampRegisterationForm()
    if request.method == "POST":
        form_1 = CampRegisterationForm(request.POST)
        if form_1.is_valid():
            user = form_1.save()
            data = form_1.cleaned_data
            messages.success(request, f" {data['parents_name']} registerd for the camp")
            message = f"""Camp registraion approved for {data['parents_name']} """
            group, created = Group.objects.get_or_create(name='camp')
            # user.groups.add(group)
            send_mail('Camp registration', message, 'settings.EMAIL_HOST_USER',[settings.CONTACT_EMAIL], fail_silently=False)
            return redirect("login")
    error_messages = [error[0] for error in form_1.errors.values()]
    content = {'form_1': form_1, 'errors':error_messages}
    return render(request, "register_camp.html",  content)


@login_required(login_url='login')
def create_camp(request):
    form_2 = CampCreationForm()
    if request.method == 'POST':
        form_2 = CampCreationForm(request.POST, request.FILES) # <-- pass request.FILES to handle the uploaded file
        if form_2.is_valid():
            camp = form_2.save(commit=False)
            camp.img = request.FILES.get('img') # <-- get the uploaded image and assign it to the img field
            camp.save()
            data_1 = form_2.cleaned_data
            messages.success(request, f" {data_1['name']} camp created ")
            message = f""" Camp {data_1['name']} sucessfully has been created"""
            group, created = Group.objects.get_or_create(name ='Create_camp' )
            # user_1.groups.add(group)
            send_mail('The camp has been created sucessfully', message, 'settings.EMAIL_HOST_USER', [settings.CONTACT_EMAIL], fail_silently=False )
            return redirect("login")
        else:
            print(form_2.errors)
    error_messages = [error[0] for error in form_2.errors.values()]
    content = {'form_2': form_2, 'errors':error_messages}
    return render(request, "create_camp.html", content)

def index(request,next=None):
    context = {}
    return render(request, "main.html", context, status=200)

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            data = form.cleaned_data
            messages.success(request, f"Account created for {data['first_name']} {data['last_name']}")
            message = f"""Welcome {data['first_name']} {data['last_name']} to MVP Akademi"""

            group, created = Group.objects.get_or_create(name='customer')
            user.groups.add(group)
            send_mail('New MVP Account', message, 'settings.EMAIL_HOST_USER', [data["email"]], fail_silently=False)
            return redirect("login")
    error_messages = [error[0] for error in form.errors.values()]
    content = {'form': form, 'errors':error_messages}

    return render(request, "register.html", content)

@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            if user.last_login is None:
                login(request, user)
                return redirect('edit_profil')
            else:
                login(request, user)
                next = request.GET.get('next')
                if next:
                    return redirect(next, 'index')
                else:
                    return redirect('index')
        else:

            messages.error(request, 'Username or password incorrect')

    return render(request, "login.html")

def logoutPage(request):
    logout(request)
    
    return redirect("login")

@login_required(login_url='login')
def profilPage(request):
    context = {}

    return render(request, 'profil.html', context)

@login_required(login_url='login')
@is_superuser
def coach(request):
    coaches = Coach.objects.all()
    if request.method == "POST":
        email = request.POST.get("email")
        user = User.objects.filter(email=email).first()
        group, created = Group.objects.get_or_create(name="coach")
        if user is not None:
            if group.id not in user.groups.values_list(flat=True):
                coach = Coach.objects.create(customer=user)
                user.groups.add(group)
                message = f"You have been uppdated as a MVP Akademi Coach"
                send_mail('MVP Coach', message, 'settings.EMAIL_HOST_USER', [user.email], fail_silently=False)

                csrf_token = get_token(request)
                element = render_to_string('fill_coach_html.html', {'csrf_token': csrf_token, 'coach':coach})
                success = {
                'status': 1,
                'html': element,
                }
                return JsonResponse(success)
            else:
                msg = f"{email} is already a coach"
        else:
            msg = f"{email} didn't match any existing user"
        success = {
        'status': 0,
        'msg': msg,
        }
        return JsonResponse(success)
    content = {"coaches":coaches}
    return render(request, "coach.html", content)

@login_required(login_url='login')
@is_superuser
def update_coach(request, coach_id):
    coach_id = int(coach_id)
    coach = Coach.objects.filter(id=coach_id).first()
    if coach:
        if request.method == "POST":
            certified = request.POST.get("certified")
            if certified == "false":
                coach.certified = False
            else:
                coach.certified = True
            coach.save()
            success = {
            'status': 1,
            'id': coach_id,
            'certified': str(coach.certified)
            }
            return JsonResponse(success)
        else:
            return JsonResponse({
            'status': 0,
            'msg': "Something went wrong, try again"
            })
    else:
        return JsonResponse({
            'status': 0,
            'msg': "Couldn't find the Coach"
            })
    
@login_required(login_url='login')
@is_superuser
def delete_coach(request, coach_id):
    coach = Coach.objects.filter(id=coach_id).first()
    if coach:
        group = Group.objects.get(name='coach')
        coach.customer.groups.remove(group.id)
        coach.delete()
        success = {
           'status': 1,
           'id': coach_id
        }
        return JsonResponse(success)
    else:
        return JsonResponse({
           'status': 0,
           'msg': 'Coach already deleted'
        })

@login_required(login_url='login')
@is_superuser
def location(request):
    locations = Location.objects.all()
    if request.method == "POST":
        location = request.POST.get("location")
        location, created = Location.objects.get_or_create(location=location)
        if created:
            html = f"""<div id="{location.id}" class="delete-location mb-1 p-1 flex justify-between items-center border-solid border-2 border-black rounded-lg"
                    location-id="{location.id}" location-name="{location.location}">
                        <p class="text-lg font-semibold">{location.location}</p>
                        <p id="delete-{location.id}" class="text-white p-2 bg-red-700 rounded-md px-3 border-solid border-2 font-semibold hover:border-red-700 hover:bg-white hover:text-red-700 hover:cursor-pointer">
                            Delete
                        </p>
                    </div>"""
            success = {
            'status': 1,
            'html': html,
            }
            return JsonResponse(success)
        else:
            return JsonResponse({
            'status': 0,
            'message': f'{location} already exists'
            })
    content = {"locations":locations}
    return render(request, "location.html", content)

@login_required(login_url='login')
@is_superuser
def delete_location(request, location_id):
    location = Location.objects.filter(id=location_id).first()
    if location:
        location.delete()
        success = {
           'msg': 1,
           'id': location_id
        }
        return JsonResponse(success)
    else:
        return JsonResponse({
           'msg': 0
        })
    
@login_required(login_url='login')
@is_superuser
def booking_type(request):
    payment_types = Payment_type.objects.all()
    booking_types = Booking_Type.objects.all()
    form = BookingTypeForm()
    if request.method == "POST":
        form = BookingTypeForm(request.POST)
        if form.is_valid():
            booking_type = request.POST.get("pass_type")
            booking_type = Booking_Type.objects.filter(pass_type=booking_type).first()
            if booking_type is None:
                booking_type = form.save()
                csrf_token = get_token(request)
                choices = Payment_type.objects.all()
                html = render_to_string('fill_booking.html', {'csrf_token': csrf_token,
                                        'booking_type':booking_type, 'choices':choices})
                success = {
                'status': 1,
                'html': html,
                }
                return JsonResponse(success)
            else:
                msg = f"Booking Type with name {booking_type} already exists"
                success = {
                'status': 0,
                'msg': msg,
                }
                return JsonResponse(success)
        else:
            msg = 'Form data invalid'
            success = {
            'status': 0,
            'msg': msg,
            }
            return JsonResponse(success)

    content = {'form': form, 'errors':form.errors.values(),
                'booking_types':booking_types, 'choices': payment_types}

    return render(request, "booking_type.html", content)

@login_required(login_url='login')
@is_superuser
def update_booking_type(request, booking_type_id):
    booking_type_id = int(booking_type_id)
    booking_type = Booking_Type.objects.filter(id=booking_type_id).first()
    if booking_type:
        if request.method == "POST":
            type = request.POST.get("type")
            pay_types = request.POST.getlist("paytype[]")
            booking_type.pass_type = type
            all_payment_types = Payment_type.objects.all()
            innerHTML = ""
            for pay_type in all_payment_types:
                if str(pay_type.id) in pay_types:
                    booking_type.payment_types.add(pay_type)
                    innerHTML += f'<li class="font-semibold p-1"> { pay_type }</li>'
                    print("INNERHTML", innerHTML)
                else:
                    print("no",pay_type, pay_type.id)
                    booking_type.payment_types.remove(pay_type)
            booking_type.save()
            print(innerHTML)
            success = {
            'status': 1,
            'id': booking_type_id,
            'type': type,
            'innerhtml': innerHTML
            }
            return JsonResponse(success)
        else:
            return JsonResponse({
            'status': 0,
            'msg': "Something went wrong, try again"
            })
    else:
        return JsonResponse({
            'status': 0,
            'msg': "Couldn't find the payment_type"
            })
    

@login_required(login_url='login')
@is_superuser
def delete_booking_type(request, booking_type_id):
    booking_type = Booking_Type.objects.filter(id=booking_type_id).first()
    if booking_type:
        booking_type.delete()
        success = {
           'status': 1,
           'id': booking_type_id
        }
        return JsonResponse(success)
    else:
        return JsonResponse({
           'msg': 0
        })

@login_required(login_url='login')
@is_superuser
def payment_types(request):
    form = PaymentTypes()
    payment_types = Payment_type.objects.all()
    if request.method == "POST":
        form = PaymentTypes(request.POST)
        if form.is_valid():
            payment_type = form.save()
            csrf_token = get_token(request)
            element = render_to_string('fill_payment_type_html.html', {'csrf_token': csrf_token, 'payment_type':payment_type})
            success = {
            'status': 1,
            'html': element,
            }
            return JsonResponse(success)
        else:
            error_messages = [error[0] for error in form.errors.values()]
            errors = [str(error) + "\n" for error in error_messages]
            msg = errors
        success = {
        'status': 0,
        'msg': msg,
        }
        return JsonResponse(success)
    content = {"payment_types":payment_types, 'form':form}
    return render(request, "payment_types.html", content)

@login_required(login_url='login')
@is_superuser
def update_payment_type(request, payment_type_id):
    payment_type_id = int(payment_type_id)
    payment_type = Payment_type.objects.filter(id=payment_type_id).first()
    if payment_type:
        if request.method == "POST":
            name = request.POST.get("name")
            price = request.POST.get("price")
            short = request.POST.get("short")
            long = request.POST.get("long")
            type = request.POST.get("type")
            payment_type.name = name
            payment_type.price = price
            payment_type.short_description = short
            payment_type.description = long
            payment_type.type = type
            payment_type.save()
            success = {
            'status': 1,
            'id': payment_type_id,
            'name': name,
            'price': price,
            'short': short,
            'long': long,
            'type': type,
            }
            return JsonResponse(success)
        else:
            return JsonResponse({
            'status': 0,
            'msg': "Something went wrong, try again"
            })
    else:
        return JsonResponse({
            'status': 0,
            'msg': "Couldn't find the payment_type"
            })


@login_required(login_url='login')
@is_superuser
def delete_payment_type(request, payment_type_id):
    payment_type = Payment_type.objects.filter(id=payment_type_id).first()
    if payment_type:
        payment_type.delete()
        success = {
           'status': 1,
           'id': payment_type_id
        }
        return JsonResponse(success)
    else:
        return JsonResponse({
           'status': 0,
           'msg': 'Payment type already deleted'
        })
        
def calender(request):
    bookings = Booking.objects.all()
    passes = []  # Initialize the 'passes' variable as an empty list

    for booking in bookings:
        # Format the datetime object in the desired format
        start_time = "'" + datetime.combine(booking.date, booking.start_time).strftime('%Y-%m-%dT%H:%M:%S') + "'"
        end_time = "'" + datetime.combine(booking.date, booking.end_time).strftime('%Y-%m-%dT%H:%M:%S') + "'"
        title = "title"
        passes.append([title, start_time, end_time])  # Append values to the 'passes' list

    return render(request, "calender.html", {'passes': passes})

    
# def calender(request):
#     bookings = Booking.objects.all()
#     html = ""
#     for booking in bookings:

#         # Format the datetime object in the desired format
#         start_time = "'" + datetime.combine(booking.date, booking.start_time).strftime('%Y-%m-%dT%H:%M:%S') + "'"
#         end_time = "'" + datetime.combine(booking.date, booking.end_time).strftime('%Y-%m-%dT%H:%M:%S') + "'"
#         title = "title"
#         passes = [[title, start_time, end_time]]
#     return render(request, "calender.html", {'passes':passes})

@login_required(login_url='login')
def edit_profil(request):
    user = request.user
    form, form2 = None, None
    form1_errors = None
    
    if request.method == 'POST':
        if 'address' in request.POST:
            form = UpdateUserForm(request.POST, request.FILES)
            if form.is_valid():
                new_email = request.POST['email']
                if new_email != user.email and User.objects.filter(email=new_email).exists():
                    form.add_error("email", "Email address already taken")
                else:
                    form.save(request.user)
                    return redirect('profil')

        elif 'first_name' in request.POST:
            form2 = PlayerForm(request.POST, request.FILES)
            if form2.is_valid():
                if user.players.count() + 1 <= user.max_players:
                    player = form2.save(request.user) 
                    csrf_token = get_token(request)
                    update_player_form = UpdatePlayerForm()
                    element = render_to_string('fill_player.html', {'csrf_token': csrf_token, 'player':player, 'update_player_form':update_player_form})
                    success = {
                    'status': 1,
                    'html': element,
                    }
                    return JsonResponse(success)
                else:
                    msg = f"You can't add any more players, ask admin"
                    success = {
                    'status': 0,
                    'msg': msg,
                    }
                    return JsonResponse(success)
            else:
                print(form2.errors)
                msg = f"Something went wrong, invalid input"
                success = {
                'status': 0,
                'msg': msg,
                }
                return JsonResponse(success)
                
    if form:
        form1_errors = [error[0] for error in form.errors.values()]
    form = UpdateUserForm(user=user)
    players = user.players.all()
    player_form = PlayerForm(user=user)
    update_player_form = UpdatePlayerForm()
    content = {'form': form, 'player_form': player_form, 'form1_errors': form1_errors,
                "players":players, "update_player_form":update_player_form,
                }

    return render(request, 'edit_profil.html', content)

@login_required(login_url='login')
def update_player(request, player_id):
    user = request.user
    update_player_form = UpdatePlayerForm(request.POST, request.FILES)
    if update_player_form.is_valid():
        player = Player.objects.filter(id=player_id, customer=user).first()
        if player:
            update_player_form.save(player)
            email = request.POST.get("email")
            phone_number = request.POST.get("phone_number")
            year_of_birth = request.POST.get("year_of_birth")
            success = {
                'status': 1,
                'email': email,
                'number': phone_number,
                'year': year_of_birth
                }
            return JsonResponse(success)
        else:
            return JsonResponse({
            'status': 0,
            'msg': "Couldn't find the player, try again"
            })
    else:
        return JsonResponse({
            'status': 0,
            'msg': "Something went wrong invalid input"
            })
@is_superuser
def new_year(request):
    groups = Groups.objects.all()
    for group_ in groups:
        if len(group_.group) == 5 and group_.group[0] in ["+", "-"]:
            group_.delete()
    players = Player.objects.all()
    for player in players:
        group, create = get_group(player.year_of_birth)
        player.group.add(group)
        player.save()
    return render(request, 'new_year.html')

@login_required(login_url='login')
def delete_player(request, player_id):
    user = request.user
    player = Player.objects.filter(customer=user, id=player_id).first()
    if player:
        player.delete()
        success = {
           'status': 1,
           'id': player_id
        }
        return JsonResponse(success)      
    else:
        return JsonResponse({
           'status': 0,
           'msg': "Did not found player"
        })

@is_superuser
def booking(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'booking.html', {'form':form})

def get_bookings(request):
    bookings = Booking.objects.all()
    booking_list =[]
    for booking in bookings:
        start_time = datetime.combine(booking.date, booking.start_time).strftime('%Y-%m-%dT%H:%M:%S')
        end_time = datetime.combine(booking.date, booking.end_time).strftime('%Y-%m-%dT%H:%M:%S')
        booking_list.append({ 'title': str(booking.pass_type),
                        'start': str(start_time),
                        'end': str(end_time),
                        'editable': False,
                        'id':booking.id,
                    })
    success = {
        'events': booking_list
    }
    return JsonResponse(success)

def get_booking_info(request, booking_id):
        booking = Booking.objects.filter(id=booking_id).first()
        if booking:
            coaches = ', '.join([f"{item.customer.first_name} {item.customer.last_name}" for item in booking.coach.all()])
            spot_left = booking.max_players - len(booking.players.all())
            adress_url = "https://www.google.com/maps/place/" + ("+").join(booking.address.split(" ")) + "/"
            adress_list = booking.address.split(" ")[:5] + [""] * (5 - len(booking.address.split(" ")))
            adress20 = "".join([adress_list[0],'%20',adress_list[1],'%20',adress_list[2],'%20',adress_list[3],'%20', adress_list[4]])
            map_html = render_to_string('fill_map.html', {'adress20':adress20})
            success = {
                'status':1,
                'location':str(booking.location),
                'date': booking.date,
                'from': booking.start_time,
                'to': booking.end_time,
                'coaches': coaches,
                'spot_left': spot_left,
                'adress': booking.address,
                'adress_url': adress_url,
                'map_html': map_html
            }
            return JsonResponse(success)
        else:
            success = {
                'status':0,
                'msg':'booking not find'
            }
            return JsonResponse(success)      