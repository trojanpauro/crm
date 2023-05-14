from django import forms  
from .models import Customer,Lead,Sale,Ticket,Notification
class SignInForm(forms.Form): 
	username = forms.CharField(label='username', max_length=150) 
	password=forms.CharField(label='password', max_length=128)


class SignUpForm(forms.Form):
	name=forms.CharField(label='name', max_length=128)
	surname=forms.CharField(label='surname', max_length=128)
	email=forms.EmailField(label='email', max_length=128)
	password=forms.CharField(label='password', max_length=128)
	phone_number=forms.CharField(label='phone_number', max_length=128)
	confirm_password=forms.CharField(label='confirm_password', max_length=128)
	role=forms.CharField(label='role', max_length=128)
	town=forms.CharField(label='town', max_length=128)



class CustomerForm(forms.ModelForm):
	class Meta:
		model = Customer
		fields = [
			'first_name',
			'last_name',
			'email',
			'phone',
			'intrests']

class LeadForm(forms.ModelForm):
	class Meta:
		model = Lead
		fields = [
			'note',
			'lead_customer',
			'intrested_in',
			'conversations',
			'elevator' ,
			'state'
			]

class TicketForm(forms.ModelForm):
	class Meta:
		model = Ticket
		fields =[
			'tittle',
			'agents',
			'department',
			'status',
			'ticket_customer'
				]

class SaleForm(forms.ModelForm):
	class Meta:
		model = Sale
		fields =[
			'transaction_date',
			'product',
			'sale_customer']


class NotificationForm(forms.ModelForm):
	class Meta:
		model = Notification
		fields =['notification','departments','agents','conversation','ticket','lead']



     