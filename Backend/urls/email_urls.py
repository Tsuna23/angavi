from django.urls import path
from Backend.views.contact_message_view import send_contact_email

urlpatterns = [
    path("contact/", send_contact_email, name="send_contact_email"),
]
