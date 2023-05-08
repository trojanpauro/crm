from django.shortcuts import render
from django.template import loader
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate,login,logout
from django.db import IntegrityError
from django.db.models import Sum
from django.http import HttpResponse,JsonResponse
from .forms import SignInForm,SignUpForm,CustomerForm
from django.contrib import messages
from django.shortcuts import render ,redirect,get_object_or_404
from django.contrib.auth.models import User 
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import DetailView ,ListView
from .models import Customer,Ticket,Message,Lead,Sale,Conversation,Agent,Ticket,Notification


@login_required()
def index(request):
	template=loader.get_template('crmapp/index.html')
	try:
		messages = Message.objects.all().reverse()[:5]
	except IndexError:
		messages = Message.objects.all()


	try:
		tickets = Ticket.objects.all().reverse()[:5]
	except IndexError:
		tickets = Ticket.objects.all()

	try:
		notifications = Notification.objects.all().reverse()[5]

	except IndexError:
		notifications =Notification.objects.all()






	
	
	context={'messages':messages,'notifications':notifications,'tickets':tickets}
	return HttpResponse(template.render(context,request))	



def testbed(request,conversation_id):
	template=loader.get_template('crmapp/dummy.html')
	customer_form = CustomerForm()
	context={'customer_form':customer_form}

	return HttpResponse(template.render(context,request))   

def get_session_key(request):
	session_key=request.session.session_key
	if session_key is not None:
		return session_key
	else :
		session=request.session.cycle_key()
		sek=request.session.session_key
		return sek

def message_endpoint(request):

	session_key=get_session_key(request)
	message = request.POST['message']
	try:
	   conversation = Conversation.objects.get(session_key=session_key)

	except ObjectDoesNotExist:
		print("no coversation")


	
	
	if request.user.is_authenticated:
		agent = Agent.objects.get(user=request.user)
		reply = True
	else:
		reply = False
 
	if reply:

		message = Message(conversation=conversation,
							message_to=conversation.customer,
							message_from=agent,
							body=message)

	else:
		message = Message(conversation=conversation,
						message_from=conversation.customer,
						body=message)
		
	message.save()
	data={} 
	data['time']=naturaltime(message.date_added)
	data['user']=str(message.message_from)
	data['message'] = message.body

	return JsonResponse(data)
  

def customer_create_json(request):

	session_key=get_session_key(request)
	print(session_key)
	form = CustomerForm(request.POST)
	if form.is_valid():
	  customer=form.save()

	else :
		print(form.errors())
	
	data={} 

	try:
	   conversation = Conversation.objects.get(session_key=session_key)
	except ObjectDoesNotExist:
		conversation = Conversation(customer=customer,session_key=session_key)
		conversation.save()
	data['message'] = customer.first_name	
	another = request.build_absolute_uri('/')
	another = another+'chat/testbed/'+session_key
	data['url']=another
	return JsonResponse(data)



def login_page(request):

	template = loader.get_template('crmapp/login.html')
	context = {}
	return HttpResponse(template.render(context, request))


def signup(request):

	template = loader.get_template('crmapp/signup.html')
	context = {}
	return HttpResponse(template.render(context, request))
@login_required
def logout_view(request):
	logout(request)
	messages.add_message(request, messages.INFO, 'Logged out')
	return redirect("index")




def register(request):

	
	form = SignUpForm(request.POST)
	if form.is_valid():
		name=form.cleaned_data['name']
		surname=form.cleaned_data['surname']
		email=form.cleaned_data['email']
		password=form.cleaned_data['password']
		confirm_password=form.cleaned_data['confirm_password']
	  
	else:
		print(form.errors)
		messages.add_message(request, messages.ERROR, 'There was an error please try again')
		return redirect('login')
		
	


	try:
		user = User.objects.create_user(email, email, password)
		user.first_name=name
		user.last_name=surname
		user.save()
		return redirect('login')



	except IntegrityError:
		messages.add_message(request, messages.ERROR, 'Email Is already in use reset password if you forgot')
		return redirect('login')
def authentication(request):
	if request.method == 'POST':
		form = SignInForm(request.POST)
		if form.is_valid():
			username=form.cleaned_data['username']
			password=form.cleaned_data['password']      
			user = authenticate(username=username, password=password)
		if user is not None:
			login(request,user)
			return redirect("/")
		else:
			messages.add_message(request, messages.ERROR, 'Invalid Email or Password')
			return redirect("login")


def Customerhandler(request,slug):
	template=loader.get_template('crmapp/customer_list.html')
	if slug == "all":
		customer_list=Customer.objects.all()
	else:
		customer_list = Customer.objects.filter(category=slug)
	context = {'customer_list':customer_list}
	return HttpResponse(template.render(context,request))  

	

class CustomerDeleteView(DeleteView):
	model = Customer 
	success_url='/customers/'


class CustomerCreateView(CreateView):
	model = Customer
	fields = ['first_name','last_name','email','phone','intrests']
	

class CustomerUpdateView(UpdateView):
	model = Customer 
	fields = ['first_name','last_name','email','phone','intrests','category']

class CustomerDetailView(DetailView):
	model = Customer



def Tickethandler(request,slug):
	template=loader.get_template('crmapp/ticket_list.html')

	if slug == "all":
		ticket_list=Ticket.objects.all()
	else:
		ticket_list = Ticket.objects.filter(status=slug)
	context = {'ticket_list':ticket_list}


	




	return HttpResponse(template.render(context,request)) 



class CustomerTicketListView(ListView):
	model = Ticket


class CategoryTicketListView(ListView):
	model = Ticket
	

class TicketDeleteView(DeleteView):
	model = Ticket 
	success_url='/tickets/'


class TicketCreateView(CreateView):
	model = Ticket
	fields =[
		'tittle',
		'agents',
		'department'

	]
	

class TicketUpdateView(UpdateView):
	model = Ticket 

	fields =[
		'tittle',
		'agents',
		'department',
		'status'

	]

class TicketDetailView(DetailView):
	model = Ticket



class CustomerMessageListView(ListView):
	model = Message


class CategoryMessageListView(ListView):
	model = Message


	

class MessageDeleteView(DeleteView):
	model = Message 
	success_url='/messages/'


class MessageCreateView(CreateView):
	model = Message
	

class MessageUpdateView(UpdateView):
	model = Message 

class MessageDetailView(DetailView):
	model = Lead


def Leadhandler(request,slug):

	template=loader.get_template('crmapp/lead_list.html')
	lead_list = Lead.objects.all()
	context = {'lead_list':lead_list}
	return HttpResponse(template.render(context,request)) 
	

class LeadDeleteView(DeleteView):
	model = Lead 
	success_url='/leads/'


class LeadCreateView(CreateView):
	model = Lead
	fields = ['note','customer','intrested_in','conversations','elevator' ,'state']
	

class LeadUpdateView(UpdateView):
	model = Lead 
	fields = ['note','customer','intrested_in','conversations','elevator' ,'state']

class LeadDetailView(DetailView):
	model = Lead



def Salehandler(request,slug):
	template=loader.get_template('crmapp/sale_list.html')
	sale_list = Sale.objects.all()
	context = {'sale_list':sale_list}
	return HttpResponse(template.render(context,request)) 

class SaleDeleteView(DeleteView):
	model = Sale 
	success_url='/sales/'


class SaleCreateView(CreateView):
	model = Sale
	fields =['transaction_date','product','customer']
	

class SaleUpdateView(UpdateView):
	model = Sale 
	fields =['transaction_date','product','customer']

class SaleDetailView(DetailView):
	model = Sale


def Conversationhandler(request,slug):
	template=loader.get_template('crmapp/conversation_list.html')
	conversation_list = Conversation.objects.all()
	context = {'conversation_list':conversation_list}
	return HttpResponse(template.render(context,request)) 

class ConversationDeleteView(DeleteView):
	model = Conversation 
	success_url='/conversations/'


class ConversationCreateView(CreateView):
	model = Conversation
	

class ConversationUpdateView(UpdateView):
	model = Conversation 

class ConversationDetailView(DetailView):
	model = Conversation







		




