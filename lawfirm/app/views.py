from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ClientForm, UserRegistration
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum
from .models import *
import random
import datetime

def home(request):
    totalCases=Clients.objects.all().count()
    activeCases=Clients.objects.filter(status='ongoing').count()
    closedCases=Clients.objects.filter(status='case closed').count()
    closedCasesPercentage=(closedCases/totalCases)*100
    ongoingCasesPercentage=(activeCases/totalCases)*100
    totalBillPaid=Clients.objects.all().aggregate(Sum('billing'))['billing__sum']
    context={
        "totalCases":totalCases,
        "activeCases":activeCases,
        "closedCases":closedCases,
        "totalBillPaid":totalBillPaid,
        "closedCasesPercentage":closedCasesPercentage,
        "ongoingCasesPercentage":ongoingCasesPercentage
    }
    return render(request, "dashboard.html",context)

def signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.warning(request, "Username or Password is incorrect")
            return redirect("signin")
    return render(request, "Accounts/login.html")

def register(request):
    form = UserRegistration()
    if request.method == "POST":
        form = UserRegistration(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account was created for {username}")
            return redirect("signin")
    context = {"forms": form}
    return render(request, "Accounts/register.html", context)

def clientManagement(request):
    data=Clients.objects.all()
    context = {
        "data": data,
    }
    return render(request, "clientManagement.html",context)

def newClient(request):
    number = random.randint(1000, 9999)
    letter = "CMS"
    currentDate = datetime.datetime.now()
    generalNumber = f"{letter}/{number}/{currentDate.strftime('%d/%m/%Y')}"

    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Client data saved successfully.")
            return redirect('clientManagement')
        else:
            messages.error(request, "Please correct the errors below.")
    
    else:
        form = ClientForm()

    return render(request, "newClient.html", {
        "number": generalNumber,
        "form": form,
    })


def updateClient(request, pk):
    client = Clients.objects.get(id=pk)
    form = ClientForm(instance=client)
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, "Client data updated successfully.")
            return redirect('clientManagement')
        else:
            messages.error(request, "Please correct the errors below.")
    
    return render(request, "newClient.html", {
        "form": form,
    })

def deleteClient(request, pk):
    client = Clients.objects.get(id=pk)
    client.delete()
    messages.success(request, "Client data deleted successfully.")
    return redirect('clientManagement')


def clientInfo(request, pk):
    client = Clients.objects.filter(id=pk).first()
    context={
        "client":client
    }
    return render(request,'clientInfo.html',context)


def courtAttendances(request,pk):
    client = Clients.objects.filter(id=pk).first()
    if request.method == 'POST':
        date=request.POST.get('date')
        matterNumber=request.POST.get('matterNumber')
        matterName=request.POST.get('matterName')
        parties=request.POST.get('parties')
        purpose=request.POST.get('purpose')
        court_presiding=request.POST.get('courtPresiding')
        advocates=request.POST.get('advocatesAttending')
        timeTaken=request.POST.get('timeTaken')
        furtherAction=request.POST.get('furtherAction')
        signedBy=request.POST.get('signedBy')
        courtAttendance.objects.create(date=date,matterNumber=matterNumber,matterName=matterName,parties=parties,purpose=purpose,court_presiding=court_presiding,advocates=advocates,timeTaken=timeTaken,furtherAction=furtherAction,signedBy=signedBy)
        messages.success(request, "Court attendance saved successfully.")
        return redirect('clientManagement')
    context={
        "client":client
    }
    return render(request,'attendance.html',context)


def activeClient(request):
    data=Clients.objects.filter(status='ongoing')
    context = {
        "data": data,
    }
    return render(request, "ongoing.html",context)


def closedClient(request):
    data=Clients.objects.filter(status='case closed')
    context = {
        "data": data,
    }
    return render(request, "closed.html",context)


def Billing(request):
    unpaid=Clients.objects.filter(payment_status='unpaid')[:5]
    paid=Clients.objects.filter(payment_status='paid')[:5]
    proBono=Clients.objects.filter(payment_status='pro Bono')[:5]
    TotalAmountPaid=Clients.objects.filter(payment_status='paid').aggregate(Sum('billing'))['billing__sum']
    TotalAmountUnpaid=Clients.objects.filter(payment_status='unpaid').aggregate(Sum('billing'))['billing__sum']

    context={
        "unpaid":unpaid,
        "paid":paid,
        "proBono":proBono,
        "TotalAmountPaid":TotalAmountPaid,
        "TotalAmountUnpaid":TotalAmountUnpaid
    }
    return render(request, "billing.html",context)





def charts(request):
    totalCases = Clients.objects.all().count()
    activeCases = Clients.objects.filter(status='ongoing').count()
    closedCases = Clients.objects.filter(status='case closed').count()

    unpaid = Clients.objects.filter(payment_status='unpaid')[:5]
    paid = Clients.objects.filter(payment_status='paid')[:5]
    proBono = Clients.objects.filter(payment_status='pro Bono')[:5]
    TotalAmountPaid = Clients.objects.filter(payment_status='paid').aggregate(Sum('billing'))['billing__sum'] or 0
    TotalAmountUnpaid = Clients.objects.filter(payment_status='unpaid').aggregate(Sum('billing'))['billing__sum'] or 0

    # Calculate percentages
    if totalCases > 0:
        activeCasesPercentage = (activeCases / totalCases) * 100
        closedCasesPercentage = (closedCases / totalCases) * 100
    else:
        activeCasesPercentage = 0
        closedCasesPercentage = 0

    # Get dispute counts
    criminal_disputes = Clients.objects.filter(dispute='criminal').count()
    civil_disputes = Clients.objects.filter(dispute='civil').count()
    other_disputes = Clients.objects.filter(dispute='other').count()

    context = {
        'totalCases': totalCases,
        'activeCases': activeCases,
        'closedCases': closedCases,
        'activeCasesPercentage': activeCasesPercentage,
        'closedCasesPercentage': closedCasesPercentage,
        'unpaid': unpaid,
        'paid': paid,
        'proBono': proBono,
        'TotalAmountPaid': TotalAmountPaid,
        'TotalAmountUnpaid': TotalAmountUnpaid,
        'criminal_disputes': criminal_disputes,
        'civil_disputes': civil_disputes,
        'other_disputes': other_disputes,
    }
    
    return render(request, 'charts.html', context)








def signout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect("signin")
