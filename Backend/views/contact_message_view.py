from django.core.mail import EmailMessage
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def send_contact_email(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        email = data.get('email')   
        subject = data.get('subject')
        message = data.get('message')

        full_message = f"De: {name} <{email}>\n\n{message}"

        email_message = EmailMessage(
            subject=subject,
            body=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.DEFAULT_FROM_EMAIL],
            reply_to=[email] if email else None
        )

        email_message.send(fail_silently=False)

        return JsonResponse({"status": True, "message": "Email envoyé avec succès."})

    return JsonResponse({"status": False, "message": "Méthode non autorisée."}, status=405)
