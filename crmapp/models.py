from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.




lead_states=[
('prospect','prospect'),
('qualified_lead','qualified_lead'),
('pitch','pitch'),
('closing','closing'),
('nurturing','nurturing')

]


customer_categories=[
('first_contact','first contact'),
('multiple_contact','multiple contact'),
('purchased','purchased'),
('unsubscribed','unsubscribed'),
]

staff_roles = [
	('contact_center','contact_center'),
	('markerting','markerting'),
	('sales','sales'),
	('management','management'),
	('field_service','field service')
]

notification_severity = [
	('low','low'),
	('medium','medium'),
	('high','high'),

]

conversation_category = [
('know_more','i want to know more'),
('sales','sales enquiry'),
('technical_fault','technical fault'),
('billing issue','billing issue'),
('other','other'),

]

message_status = [
('sent','sent'),
('read','read'),
('replied','replied')
]


conversation_status = [
('unread','unread'),
('open','open'),
('closed','closed'),
('escalated','escalated'),
]

ticket_status = [
('to_do','to do'),
('in_progress','in progress'),
('done','done')

]



class Department(models.Model):
	name = models.CharField(max_length=50)


	def __str__(self):
			return  self.name



class Product(models.Model):
	name = models.CharField(max_length=50)
	department = models.ForeignKey(Department, on_delete=models.PROTECT)


	def get_absolute_url(self):
		return reverse('product_detail', kwargs={'pk': self.pk})



	def __str__(self):
			return self.name

class Persona(models.Model):
	"""docstring for ClassName"""
	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)
	email = models.CharField(max_length=200)
	phone = models.CharField(max_length=200)
	date_added = models.DateTimeField(auto_now=True)


	def __str__(self):
			return self.first_name +" "+ self.last_name



class Intrest(models.Model):
	tittle = models.CharField(max_length = 100)
	department = models.CharField(choices= staff_roles,max_length=100)

	def __str__(self):
			return self.tittle



	
class Customer(Persona):
	category = models.CharField(choices=customer_categories,max_length=100)
	intrests = models.ManyToManyField(Intrest)


	def get_absolute_url(self):
		return reverse('customer_detail', kwargs={'pk': self.pk})



class Agent(Persona):
	user = models.ForeignKey(User , on_delete = models.CASCADE)
	staff_roles = models.CharField(choices = staff_roles,max_length=100,default='contact_center')
	department = models.ForeignKey(Department, on_delete=models.PROTECT)


	def get_absolute_url(self):
		return reverse('agent_detail', kwargs={'pk': self.pk})

class Ticket(models.Model):
	date_added = models.DateTimeField(auto_now=True)
	tittle = models.CharField(max_length=20)
	agents = models.ManyToManyField(Agent)
	status =models.CharField(choices=ticket_status,max_length=20)
	department = models.ManyToManyField(Department)
	ticket_customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


	def __str__(self):
			return self.tittle


	def get_absolute_url(self):
		return reverse('ticket_detail', kwargs={'pk': self.pk})



class Conversation(models.Model):

	date_added = models.DateTimeField(auto_now = True)
	agents = models.ManyToManyField(Agent)
	conversation_customer = models.ForeignKey(Customer, on_delete = models.PROTECT)
	category = models.CharField(choices = conversation_category,max_length=50)
	status = models.CharField(choices = conversation_status,max_length=50)
	rating = models.IntegerField(null=True)
	session_key = models.CharField(max_length=200)

	def __str__(self):
			return self.conversation_customer.first_name


	def get_absolute_url(self):
		return reverse('conversation_details', kwargs={'pk': self.pk})


class Lead(models.Model):
	note = models.CharField(max_length=100)
	lead_customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
	conversations = models.ForeignKey(Conversation,on_delete=models.PROTECT)
	elevator = models.ForeignKey(Agent, on_delete = models.PROTECT)
	intrested_in = models.ManyToManyField(Product)
	date_added = models.DateTimeField(auto_now=True)
	state = models.CharField(choices=lead_states,max_length=30)

	def __str__(self):
			return self.note + str(self.elevator)


	def get_absolute_url(self):
		return reverse('lead_detail', kwargs={'pk': self.pk})


class Notification(models.Model):
	date_added =models.DateTimeField(auto_now=True)
	notification = models.CharField(max_length=300)
	serverity = models.CharField(choices = notification_severity,max_length=20)
	departments = models.ManyToManyField(Department)
	agents = models.ManyToManyField(Agent)
	conversation = models.ForeignKey(Conversation, on_delete=models.PROTECT)
	ticket = models.ForeignKey(Ticket,on_delete=models.PROTECT)
	lead = models.ForeignKey(Lead, on_delete=models.PROTECT)

	def __str__(self):
			return "to:" +str(self.departments) +" message:"+ self.notification


	def get_absolute_url(self):
		return reverse('notification_detail', kwargs={'pk': self.pk})

class Subscriptions(models.Model):
	subscription_customer = models.ForeignKey(Customer, on_delete = models.PROTECT)
	date_added = models.DateTimeField(auto_now=True)

	def get_absolute_url(self):
		return reverse('subscription_detail', kwargs={'pk': self.pk})


class Message(models.Model):
	date_added = models.DateTimeField(auto_now=True)
	conversation = models.ForeignKey(Conversation,on_delete= models.PROTECT)
	message_to = models.ForeignKey(Persona, on_delete = models.PROTECT ,related_name='message_to',null=True)
	message_from = models.ForeignKey(Persona, on_delete = models.PROTECT,related_name='message_from')
	status = models.CharField(choices = message_status,max_length=50,default='sent')
	body = models.CharField(max_length=200)

	def __str__(self):
			return self.conversation.conversation_customer.first_name + "message: " +self.body


	def get_absolute_url(self):
		return reverse('message_detail', kwargs={'pk': self.pk})










	
		


class Sale(models.Model):
	transaction_date = models.DateField()
	date_added = models.DateTimeField(auto_now=True)
	sale_customer = models.ForeignKey(Customer, on_delete = models.PROTECT)
	product = models.ForeignKey(Product, on_delete= models.PROTECT)


	def get_absolute_url(self):
		return reverse('sale_detail', kwargs={'pk': self.pk})


	def __str__(self):
			return "Product:" +self.product.name +"   Customer:"+str(self.sale_customer)







class Installation(models.Model):
	pass

class Complaint(models.Model):
	conversations = models.ManyToManyField(Conversation)

class Inspection(models.Model):
	pass



	
		
		


