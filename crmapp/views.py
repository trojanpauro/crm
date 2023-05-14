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
from .forms import SignInForm,SignUpForm,CustomerForm,LeadForm,SaleForm,TicketForm,NotificationForm
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
		messages = Message.objects.all().order_by('date_added').reverse()[:3]
	except IndexError:
		messages = Message.objects.all().order_by('date_added')


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

def get_session_key(request):
	session_key=request.session.session_key
	if session_key is not None:
		return session_key
	else :
		session=request.session.cycle_key()
		sek=request.session.session_key
		return sek







def check_for_mine(request,conversation_key):


	if request.user.is_authenticated:
		user = request.user
		agent = Agent.objects.get(user_id=user.id)
		messages = Message.objects.filter(status='sent',conversation__session_key=conversation_key)
		persona = agent
	else:
		session_key = get_session_key(request)
		messages = Message.objects.filter(status='sent',conversation__session_key=session_key)
		if(messages):
			persona = messages[0].conversation.conversation_customer
	message_list = messages
	data_list=[]
	for message in message_list:
		time=naturaltime(message.date_added)
		data_list.append({'user':message.message_from.first_name,
						'message':message.body,
						'time':time})

		if message.message_from.id == persona.id:

			print("is persona")
			return JsonResponse({'data':[]})

		else:
			message.status='read'
			message.save(update_fields=['status'])
			print(persona)
			print(message.message_from)
			print("not persona")
	
	data ={'data':data_list}
	print(data)
	return JsonResponse(data)


def get_unread(session_key):
	messages = Message.objects.filter(conversation__session_key=session_key)		
	data_list=[]
	for message in messages:
		time=naturaltime(message.date_added)
		data_list.append({'user':message.message_from.first_name+" "+message.message_from.last_name,
						'message':message.body,
						'time':time})

		
	
	data ={'data':data_list}
	return data

def testbed(request,conversation_id):
	#new message 
	template=loader.get_template('crmapp/testbed.html')
	if (conversation_id == 'new'):
		session_key =get_session_key(request)
		messages = Message.objects.filter(conversation__session_key=session_key)
		if (len(messages)>=1):
			is_new =False
		else :
			is_new = True
		context ={'is_new':is_new,'messages':messages}
		return HttpResponse(template.render(context,request))  


	#json endpoint to recieve messages 

	elif(conversation_id.endswith('recieve')):
		conversation_id =conversation_id.replace('recieve','')
		my_response = check_for_mine(request,conversation_id)
		return my_response


	#tesbed load 
	else :
		if request.user.is_authenticated:
			messages = Message.objects.filter(conversation__session_key=conversation_id)
			context={'message_list':messages}
			agent = Agent.objects.get(user=request.user)
			print(agent)
			context['agent'] = agent
			print("hi")
		else:
			messages = Message.objects.filter(conversation__session_key=conversation_id)
			context={'message_list':messages}
	
	customer_form = CustomerForm()
	lead_form = LeadForm()
	ticket_form = TicketForm()
	sale_form = SaleForm()
	notification_form  = NotificationForm()
	context['sale_form'] = sale_form
	context['lead_form'] = lead_form
	context['ticket_form'] = ticket_form
	context['customer_form'] = customer_form
	context['conversation_id'] = conversation_id
	context['notification_form'] = notification_form
	my_conversation=Conversation.objects.get(session_key=conversation_id)
	context['conversation'] = my_conversation
	return HttpResponse(template.render(context,request))   



def message_endpoint(request):

	session_key=get_session_key(request)
	message = request.POST['message']
	chat_session = request.POST['conversation_id']
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
		conversation = Conversation.objects.get(session_key=chat_session)
		message = Message(conversation=conversation,
							message_to=conversation.conversation_customer,
							message_from=agent,
							body=message)

	else:
		message = Message(conversation=conversation,
						message_from=conversation.conversation_customer,
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
		conversation = Conversation(conversation_customer=customer,session_key=session_key)
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
	success_url='/customers/all'


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
	success_url='/tickets/all'


class TicketCreateView(CreateView):
	model = Ticket
	fields =[
		'tittle',
		'agents',
		'department',
		'ticket_customer'

	]
	

class TicketUpdateView(UpdateView):
	model = Ticket 

	fields =[
		'tittle',
		'agents',
		'department',
		'status',
		'ticket_customer'

	]

class TicketDetailView(DetailView):
	model = Ticket



class CustomerMessageListView(ListView):
	model = Message


class CategoryMessageListView(ListView):
	model = Message


	

class MessageDeleteView(DeleteView):
	model = Message 
	success_url='/messages/all'
class NotificationCreateView(CreateView):
	model = Notification
	fields =['notification','departments','agents','conversation','ticket','lead']


class NotificationUpdateView(UpdateView):
	model = Notification
	fields =['notification','departments','agents','conversation','ticket','lead']

class MessageCreateView(CreateView):
	model = Message
	

class MessageUpdateView(UpdateView):
	model = Message 

class MessageDetailView(DetailView):
	model = Message

class NotificationDetailView(DetailView):
	model = Notification


def Leadhandler(request,slug):

	template=loader.get_template('crmapp/lead_list.html')

	if slug == "all":
		lead_list=Lead.objects.all()
	else:
		lead_list = Lead.objects.filter(state=slug)
	context = {'lead_list':lead_list}

	return HttpResponse(template.render(context,request)) 
	

class LeadDeleteView(DeleteView):
	model = Lead 
	success_url='/leads/all'


class LeadCreateView(CreateView):
	model = Lead
	fields = [
		'note',
		'lead_customer',
		'intrested_in',
		'conversations',
		'elevator' ,
		'state'
			]
	

class LeadUpdateView(UpdateView):
	model = Lead 
	fields = ['note','lead_customer','intrested_in','conversations','elevator' ,'state']

class LeadDetailView(DetailView):
	model = Lead



def Salehandler(request,slug):
	template=loader.get_template('crmapp/sale_list.html')
	sale_list = Sale.objects.all()
	context = {'sale_list':sale_list}
	return HttpResponse(template.render(context,request)) 

class SaleDeleteView(DeleteView):
	model = Sale 
	success_url='/sales/all'


class SaleCreateView(CreateView):
	model = Sale
	fields =['transaction_date','product','sale_customer']
	

class SaleUpdateView(UpdateView):
	model = Sale 
	fields =['transaction_date','product','sale_customer']

class SaleDetailView(DetailView):
	model = Sale


def Conversationhandler(request,slug):
	template=loader.get_template('crmapp/conversation_list.html')
	if slug == "all":
		conversation_list=Conversation.objects.all()
	else:
		conversation_list = Conversation.objects.filter(status=slug)
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




def chat(request):
	template = loader.get_template('crmapp/chat_customer.html')
	context = {}
	return HttpResponse(template.render(context,request)) 


def conversation(request,conversation_id):
	template = loader.get_template('crmapp/chat_customer.html')
	context = {}
	return HttpResponse(template.render(context,request)) 

	
# Import the required modules
import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Define the access token and the verify token for the Facebook app
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
VERIFY_TOKEN = "YOUR_VERIFY_TOKEN"

# Define a function to handle GET requests
@csrf_exempt
def webhook(request):
    # Check if the request is a GET request
    if request.method == "GET":
        # Get the query parameters
        mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")
        # Verify the token and return the challenge
        if mode == "subscribe" and token == VERIFY_TOKEN:
            return HttpResponse(challenge)
        else:
            return HttpResponse("Invalid verification token")
    # Check if the request is a POST request
    elif request.method == "POST":
        # Get the request body as JSON
        data = request.json()
        # Check if the data contains an entry object
        if data.get("object") == "page":
            # Loop through each entry object
            for entry in data.get("entry"):
                # Get the message object
                message = entry.get("messaging")[0]
                # Check if the message contains a sender id and a text
                if message.get("sender") and message.get("message"):
                    # Get the sender id and the text
                    sender_id = message.get("sender").get("id")
                    text = message.get("message").get("text")
                    # Call a function to process the text and generate a reply
                    reply = process_text(text)
                    # Call a function to send the reply to the sender
                    send_message(sender_id, reply)
        return HttpResponse("OK")

# Define a function to process the text and generate a reply
def process_text(text):
    # This is where you can write your own logic to process the text and generate a reply
    # For example, you can use natural language processing, machine learning, or any other technique
    # For simplicity, we will just echo back the text with some modification
    reply = "You said: " + text.upper()
    return reply

# Define a function to send the reply to the sender
def send_message(sender_id, reply):
    # Prepare the payload for the request
    payload = {
        "recipient": {
            "id": sender_id
        },
        "message": {
            "text": reply
        }
    }
    # Prepare the headers for the request
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + ACCESS_TOKEN
    }
    # Send a POST request to the Facebook Graph API
    response = requests.post("https://graph.facebook.com/v12.0/me/messages", json=payload, headers=headers)
    # Check if the response is successful
    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print("Message failed to send")


