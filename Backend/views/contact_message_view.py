from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

@csrf_exempt
def send_contact_email(request):
    if request.method == 'POST':
        try:
            # Parse JSON
            try:
                data = json.loads(request.body.decode("utf-8"))
            except json.JSONDecodeError:
                return JsonResponse(
                    {"status": False, "message": "JSON invalide"},
                    status=400
                )

            # Validation
            name = data.get('name')
            email = data.get('email')   
            subject = data.get('subject')
            message = data.get('message')

            if not all([name, email, subject, message]):
                return JsonResponse(
                    {"status": False, "message": "Tous les champs sont obligatoires"},
                    status=400
                )

            # Construire le message
            full_message = f"De: {name} <{email}>\n\n{message}"
            
            # ✅ UTILISER L'API SENDGRID (pas SMTP !)
            # Récupérer la clé API depuis les variables d'environnement
            sg_api_key = os.environ.get('SENDGRID_API_KEY')
            
            if not sg_api_key:
                # Fallback : utiliser EMAIL_HOST_PASSWORD si SENDGRID_API_KEY n'existe pas
                sg_api_key = getattr(settings, 'EMAIL_HOST_PASSWORD', None)
            
            if not sg_api_key:
                return JsonResponse(
                    {"status": False, "message": "Configuration SendGrid manquante"},
                    status=500
                )
            
            # Initialiser le client SendGrid
            sg = SendGridAPIClient(sg_api_key)
            
            # Créer l'email pour l'API SendGrid
            mail = Mail(
                from_email=settings.DEFAULT_FROM_EMAIL,  # Expéditeur
                to_emails=settings.DEFAULT_FROM_EMAIL,   # Destinataire (toi-même)
                subject=f"Contact Form: {subject}",
                plain_text_content=full_message
            )
            
            # Ajouter l'email de réponse
            mail.reply_to = email
            
            # Envoyer via l'API SendGrid
            response = sg.send(mail)
            
            # Vérifier la réponse
            if response.status_code in [200, 202]:
                return JsonResponse({
                    "status": True, 
                    "message": "Email envoyé avec succès via SendGrid API."
                })
            else:
                # Log l'erreur SendGrid
                print(f"SendGrid API error: {response.status_code} - {response.body}")
                return JsonResponse({
                    "status": False, 
                    "message": f"Erreur SendGrid: {response.status_code}"
                }, status=500)
                
        except Exception as e:
            # Log l'erreur pour debug
            print(f"Error in send_contact_email: {str(e)}")
            return JsonResponse({
                "status": False, 
                "message": f"Erreur interne: {str(e)}"
            }, status=500)
    
    return JsonResponse(
        {"status": False, "message": "Méthode non autorisée"},
        status=405
    )
# from django.core.mail import EmailMessage
# from django.conf import settings
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json

# @csrf_exempt
# def send_contact_email(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body.decode("utf-8"))
#         except json.JSONDecodeError:
#             return JsonResponse(
#                 {"status": False, "message": "JSON invalide"},
#                 status=400
#             )

#         name = data.get('name')
#         email = data.get('email')   
#         subject = data.get('subject')
#         message = data.get('message')

#         if not all([name, email, subject, message]):
#             return JsonResponse(
#                 {"status": False, "message": "Tous les champs sont obligatoires"},
#                 status=400
#             )

#         full_message = f"De: {name} <{email}>\n\n{message}"

#         email_message = EmailMessage(
#             subject=subject,
#             body=full_message,
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             to=[settings.DEFAULT_FROM_EMAIL],
#             reply_to=[email]
#         )

#         email_message.send(fail_silently=False)

#         return JsonResponse({"status": True, "message": "Email envoyé avec succès."})

#     return JsonResponse(
#         {"status": False, "message": "Méthode non autorisée"},
#         status=405
#     )

