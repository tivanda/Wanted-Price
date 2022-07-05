from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Link
from django.http import HttpResponse
from .forms import AddLinkForm, CreateUserForm
from django.views.generic import DeleteView
import smtplib
import time
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.

#


@csrf_exempt
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Račun je napravljen za ' + user)

            return redirect('login')
    context = {'form': form}
    return render(request, 'links/register.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'links/login.html', context)


def logutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home_view(request):
    no_discounted = 0
    error = None

    form = AddLinkForm(request.POST or None)

    if request.method == 'POST':
        try:
            if form.is_valid():
                form.save()
        except AttributeError:
            error = "Uopa...ne mogu dohvatit ime ili cijenu"
        except:
            error = "Uopa...nesto je poslo po krivu"

    form = AddLinkForm()

    qs = Link.objects.all()
    items_no = qs.count()

    if items_no > 0:
        discount_list = []
        for item in qs:
            if item.old_price > item.current_price:
                discount_list.append(item)
            no_discounted = len(discount_list)

    if discount_list != []:
        send_mail()

    context = {
        'qs': qs,
        'items_no': items_no,
        'no_discounted': no_discounted,
        'form': form,
        'error': error,
    }

    return render(request, 'links/main.html', context)

#


class LinkDeleteView(DeleteView):
    model = Link
    template_name = 'links/confirm_del.html'
    success_url = reverse_lazy('home')

# Karlo


def update_prices(request):
    qs = Link.objects.all()
    for link in qs:
        link.save()
    return redirect('home')


# Karlo

def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('karlozeko@gmail.com', 'oxwlrqyfhqjiftpy')

    subject = 'Cijena se promijenila'
    body = 'Provjeri amazon stranicu https://wantedpriceamazon.herokuapp.com/'

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        'karlozeko@gmail.com',

        'k_zeko@hotmail.com',
        msg


    )

    server.quit()
