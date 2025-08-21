from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)


def home(request):
    return render(request, "main/index.html")


def about(request):
    return render(request, "main/about.html")


def projects(request):
    return render(request, "main/projects.html")


def contact(request):
    # Debug: Print request method and all POST data
    print(f"=== CONTACT VIEW DEBUG ===")
    print(f"Request method: {request.method}")
    print(f"All POST data: {dict(request.POST)}")
    print(f"All GET data: {dict(request.GET)}")
    print(f"Request META (partial): {request.META.get('HTTP_USER_AGENT', 'Unknown')}")

    if request.method == "POST":
        # Get form data
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        subject = request.POST.get("subject", "").strip()
        message = request.POST.get("message", "").strip()

        # Debug: Print each field
        print(f"=== FORM DATA DEBUG ===")
        print(f"Name: '{name}' (length: {len(name)})")
        print(f"Email: '{email}' (length: {len(email)})")
        print(f"Subject: '{subject}' (length: {len(subject)})")
        print(f"Message: '{message}' (length: {len(message)})")

        # Check for empty fields
        missing_fields = []
        if not name:
            missing_fields.append("name")
        if not email:
            missing_fields.append("email")
        if not subject:
            missing_fields.append("subject")
        if not message:
            missing_fields.append("message")

        if missing_fields:
            error_msg = f"Missing required fields: {', '.join(missing_fields)}"
            print(f"ERROR: {error_msg}")
            messages.error(request, error_msg)
            return redirect("contact")

        # Create email content
        full_message = f"""
New message from your portfolio website:

Name: {name}
Email: {email}
Subject: {subject}

Message: 
{message}

---
This message was sent from your portfolio contact form.
Timestamp: {request.META.get('HTTP_HOST', 'Unknown')} at {request.META.get('HTTP_USER_AGENT', 'Unknown')}
        """

        try:
            print("=== ATTEMPTING TO SEND EMAIL ===")
            print(f"From: {settings.EMAIL_HOST_USER}")
            print(f"To: iamalihasnainn@gmail.com")
            print(f"Subject: Portfolio Contact: {subject}")

            send_mail(
                subject=f"Portfolio Contact: {subject}",
                message=full_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=["iamalihasnainn@gmail.com"],
                fail_silently=False,
            )

            print("✅ EMAIL SENT SUCCESSFULLY!")
            messages.success(request,
                             "Thank you! Your message has been sent successfully. I'll get back to you within 24 hours.")

            # Optional: Return a simple success page instead of redirect to see if redirect is the issue
            # return HttpResponse("Email sent successfully! Check your console for debug info.")

        except Exception as e:
            error_message = f"Error sending email: {str(e)}"
            print(f"❌ EMAIL SEND ERROR: {error_message}")
            logger.error(error_message)
            messages.error(request,
                           "Sorry, there was an error sending your message. Please try again or contact me directly at iamalihasnainn@gmail.com")

        print("=== REDIRECTING TO CONTACT PAGE ===")
        return redirect("contact")

    else:
        print("=== GET REQUEST - SHOWING CONTACT FORM ===")

    return render(request, "main/contact.html")