from django.conf import settings
from django.core.mail import send_mail


def send_status_update_email(service_request):
    """Email the citizen when the status of their request changes."""
    citizen = service_request.citizen
    if not citizen.email:
        return

    send_mail(
        subject=f"Update on your request #{service_request.pk}",
        message=(
            f"Hello {citizen.username},\n\n"
            f"Your {service_request.category.name} request at "
            f"{service_request.location} is now: "
            f"{service_request.get_status_display()}.\n\n"
            "Thank you for helping us improve our community.\n"
            "MyHuduma"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[citizen.email],
        fail_silently=True,
    )