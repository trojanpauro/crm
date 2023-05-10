from django.contrib import admin

from .models import Conversation,Customer,Agent
from .models import Message,Lead,Intrest,Department,Product,Sale
from .models import Notification,Ticket


# Register your models here.


admin.site.register(Conversation)
admin.site.register(Customer)
admin.site.register(Agent)
admin.site.register(Message)
admin.site.register(Intrest)
admin.site.register(Lead)
admin.site.register(Department)
admin.site.register(Product)
admin.site.register(Notification)
admin.site.register(Ticket)
admin.site.register(Sale)
