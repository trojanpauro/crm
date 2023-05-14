from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
	path('accounts/login/',views.login_page,name='login'),
	path('accounts/authentication/',views.authentication,name='authentication'),
    path('logout/',views.logout_view,name='logout'),
    path('signup/',views.signup,name='sign_up'),
    path('accounts/register/',views.register,name='register'),
    path('chat/testbed/<str:conversation_id>',views.testbed,name='testbed'),
    path('message/endpoint/',views.message_endpoint,name='message_endpoint'),
    path('create/customer/json',views.customer_create_json,name='create_customer_json'),
    path('chat/customers/',views.chat,name='user_chat'),
    path('chat/customers/recieve',views.check_for_mine,name='check_for_mine'),



	path('customers/<str:slug>/' ,views.Customerhandler,name='customer_list'),
	path('customers/details/<str:pk>', views.CustomerDetailView.as_view(),name='customer_detail'),
	path('customers/delete/<str:pk>' ,views.CustomerDeleteView.as_view(),name='customer_delete'),
	path('customers/update/<str:pk>', views.CustomerUpdateView.as_view(),name='customer_update'),
	path('customers/create', views.CustomerCreateView.as_view(),name='customer_create'),



	path('tickets/<str:slug>/' ,views.Tickethandler,name='ticket_list'),
	path('ticket/details/<str:pk>', views.TicketDetailView.as_view(),name='ticket_detail'),
	path('ticket/delete/<str:pk>' ,views.TicketDeleteView.as_view(),name='ticket_delete'),
	path('ticket/update/<str:pk>', views.TicketUpdateView.as_view(),name='ticket_update'),
	path('ticket/create', views.TicketCreateView.as_view(),name='ticket_create'),
	path('tickets/customer/<str:pk>',views.CustomerTicketListView.as_view(), name='customer_ticket_list'),
	path('tickets/category/<str:pk>',views.CategoryTicketListView.as_view(), name='category_ticket_list'),






	
	path('message/details/<str:pk>', views.MessageDetailView.as_view(),name='message_detail'),
	path('message/delete/<str:pk>' ,views.MessageDeleteView.as_view(),name='message_delete'),
	path('message/update/<str:pk>', views.MessageUpdateView.as_view(),name='message_update'),
	path('message/create', views.MessageCreateView.as_view(),name='message_create'),
	path('messages/customer/<str:pk>',views.CustomerMessageListView.as_view(), name='customer_message_list'),

	path('leads/<str:slug>/' ,views.Leadhandler,name='lead_list'),
	path('lead/details/<str:pk>', views.LeadDetailView.as_view(),name='lead_detail'),
	path('lead/delete/<str:pk>' ,views.LeadDeleteView.as_view(),name='lead_delete'),
	path('lead/update/<str:pk>', views.LeadUpdateView.as_view(),name='lead_update'),
	path('lead/create', views.LeadCreateView.as_view(),name='lead_create'),




	path('sales/<str:slug>/' ,views.Salehandler,name='sale_list'),
	path('sale/details/<str:pk>', views.SaleDetailView.as_view(),name='sale_detail'),
	path('sale/delete/<str:pk>' ,views.SaleDeleteView.as_view(),name='sale_delete'),
	path('sale/update/<str:pk>', views.SaleUpdateView.as_view(),name='sale_update'),
	path('sale/create', views.SaleCreateView.as_view(),name='sale_create'),
	
	path('conversations/<str:slug>/' ,views.Conversationhandler,name='conversation_list'),
	path('conversation/details/<str:pk>', views.ConversationDetailView.as_view(),name='conversation_detail'),
	path('conversation/delete/<str:pk>' ,views.ConversationDeleteView.as_view(),name='conversation_delete'),
	path('conversation/update/<str:pk>', views.ConversationUpdateView.as_view(),name='conversation_update'),
	path('conversation/create', views.ConversationCreateView.as_view(),name='conversation_create'),
#	path('conversation/chat/<str:conversation_id>', views.conversation_chat,name='conversation_chat'),
	path('notification/create', views.NotificationCreateView.as_view(),name='notification_create'),
	path('notification/details/<str:pk>', views.NotificationDetailView.as_view(),name='notification_detail'),
	path('notification /update/<str:pk>', views.NotificationUpdateView.as_view(),name='notification_update'),


]