import json
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User,Group
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate   
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_users
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from myApp.models import Ticket
from .forms import TicketForm

# Create your views here.

@login_required
def home(request):
    role = None
    if('User' in request.user.groups.all()):
        role = 'User'
    elif('Admin' in request.user.groups.all()):
        role = 'Admin'
    return render(request,'myApp/home.html',{'role':role})

@login_required
@allowed_users(['Admin'])
def dashboard(request):
    role = request.user.groups.all()[0].name
    ticketStats = None
    tickets =  None
    try:
        tickets = Ticket.objects.filter(deleted=False).order_by('-created_datetime')
        ticketStats  = {
            'total': Ticket.objects.filter(deleted=False).count(),
            'accepted': Ticket.objects.filter(deleted=False,status='Accepted').count(),
            'pending': Ticket.objects.filter(deleted=False,status='Pending').count(),
            'rejected': Ticket.objects.filter(deleted=False,status='Rejected').count(),
        }
    except Ticket.DoesNotExist as e:
        print(e)
    return render(request,'myApp/dashboard.html',{'role':role,'ticketStats':ticketStats,'tickets':tickets})

@login_required
def tickets(request):
    print(request.user.groups.all())
    role = request.user.groups.all()[0].name
    if(role == 'User'):
        tickets = Ticket.objects.filter(user=request.user,deleted=False).order_by('-id')
    elif(role == 'Admin'):
        tickets = Ticket.objects.filter(deleted=False).order_by('-created_datetime')
    return render(request,'myApp/tickets-table.html',{'tickets':tickets,'role':role})


@login_required
@allowed_users(['User'])
def raiseticket(request, id=None):
    form = TicketForm()
    try:
        ticket  = Ticket.objects.get(pk=id,user=request.user,deleted=False)
    except Ticket.DoesNotExist:
        ticket = None
    if request.method =='POST':
        if id is not None:
            form = TicketForm(request.POST,request.FILES,instance=ticket)
        else:
            form = TicketForm(request.POST,request.FILES)
        if form.is_valid():            
            new_ticket = form.save(commit=False)
            new_ticket.user = request.user
            new_ticket.save()
            return redirect('tickets')
        else:
            print("error =============")
            print(form.errors)
    else:        
        return render(request,'myApp/raise-ticket-form.html',{'form':form, 'ticket':ticket})



@login_required
def viewticket(request,id):
    role = request.user.groups.all()[0].name
    if(request.method == 'GET'):
        try:
            ticket  = Ticket.objects.get(pk=id)
            if (role == 'Admin' or request.user == ticket.user):
                return render(request, 'myApp/view-ticket.html',{'ticket':ticket})
            else:
                return redirect('forbidden')
        except Ticket.DoesNotExist as e:
            return redirect('notfound')
 

@unauthenticated_user
def signupuser(request):
    if(request.method == 'GET'):
        return render(request,'myApp/signup.html')
    else:
        #create new user
        if(request.POST['username']=='' or request.POST['email']=='' or request.POST['password1']=='' or request.POST['password2']==''):
            return render(request,'myApp/signup.html',{'error':'Enter all fields'})
        
        if(request.POST['password1'] == request.POST['password2']):
            try:
                user =  User.objects.create_user(username=request.POST['username'], email=request.POST['email'], password=request.POST['password1'])
                group = Group.objects.get(name='User')
                user.groups.add(group)
                user.save()
                login(request,user)
                return redirect('home')
            except IntegrityError:
                return render(request,'myApp/signup.html',{'error':'Username already exists'})
                
        else:
            return render(request,'myApp/signup.html',{'error':'Passwords do not match'})

@unauthenticated_user
def loginuser(request):
    if(request.method == 'GET'):
        return render(request,'myApp/login.html')
    else:
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request,'myApp/login.html',{'error':'Username and password do not match'})
        else:
            login(request,user)
            return redirect('home')

@login_required
def logoutuser(request):
    if(request.method == 'POST'):
        logout(request)
        return redirect('loginuser')

@login_required
def deleteticket(request):
    print(request.POST)
    try:
        ticket = Ticket.objects.get(user=request.user,pk=request.POST['id'],deleted="False")
        ticket.deleted = True
        ticket.save()
        return JsonResponse(status=200,data={'status':1})
    except Exception as e:  
        return JsonResponse(status=200,data={'status':0})

@login_required
def changestatus(request):   
    print(request.POST)
    id = request.POST.get('id')
    status = request.POST.get('status')
    
    try:
        ticket = Ticket.objects.get(pk=id,deleted="False")
        if(status == '1'):
            ticket.status = "Accepted"
        else:
            ticket.status = "Rejected"
        ticket.save()
        return JsonResponse(status=200,data={'status':1})
    except Exception as e:
        return JsonResponse(status=200,data={'status':0,'error':e})

from django.db.models.functions import TruncMonth
from django.db.models import Count

@login_required
def getsummary(request):

    total = Ticket.objects.filter(created_datetime__year='2022').values_list('created_datetime__month').annotate(total_item=Count('id'))
    accepted = Ticket.objects.filter(created_datetime__year='2022',status="Accepted").values_list('created_datetime__month').annotate(total_item=Count('id'))
    pending = Ticket.objects.filter(created_datetime__year='2022',status="Pending").values_list('created_datetime__month').annotate(total_item=Count('id'))
    rejected = Ticket.objects.filter(created_datetime__year='2022',status="Rejected").values_list('created_datetime__month').annotate(total_item=Count('id'))

    total_tickets = [0]*12
    accepted_tickets = [0]*12
    rejected_tickets = [0]*12
    pending_tickets = [0]*12
    
    for i in total:
        total_tickets[i[0]-1] = i[1]
    
    for i in accepted:
        accepted_tickets[i[0]-1] = i[1]
    
    for i in pending:
        pending_tickets[i[0]-1] = i[1]
    
    for i in rejected:
        rejected_tickets[i[0]-1] = i[1]

    ticketStats  = {
            'total_tickets':total_tickets,
            'accepted_tickets':accepted_tickets,
            'pending_tickets':pending_tickets,
            'rejected_tickets':rejected_tickets,
            'total': Ticket.objects.filter(deleted=False).count(),
            'accepted': Ticket.objects.filter(deleted=False,status='Accepted').count(),
            'pending': Ticket.objects.filter(deleted=False,status='Pending').count(),
            'rejected': Ticket.objects.filter(deleted=False,status='Rejected').count(),
        }

    return JsonResponse(ticketStats)


def forbidden(request):
    return render(request,'myApp/error-403-forbidden.html')

def notfound(request,exception):
    return render(request,'myApp/error-404-notfound.html')

