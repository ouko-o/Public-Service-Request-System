from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .analytics import get_category_breakdown, get_request_stats
from .decorators import staff_required
from .forms import RegistrationForm, ServiceRequestForm, StatusUpdateForm
from .models import Category, ServiceRequest
from .notifications import send_status_update_email

DASHBOARD_PAGE_SIZE = 10


def home(request):
    return render(request, "requests_app/home.html")


def register(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome! Your account has been created.")
            return redirect("home")
    else:
        form = RegistrationForm()

    return render(request, "registration/register.html", {"form": form})


@login_required
def submit_request(request):
    if request.method == "POST":
        form = ServiceRequestForm(request.POST, request.FILES)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.citizen = request.user
            service_request.save()
            messages.success(request, "Your request has been submitted.")
            return redirect("my_requests")
    else:
        form = ServiceRequestForm()

    return render(request, "requests_app/submit_request.html", {"form": form})


@login_required
def my_requests(request):
    service_requests = request.user.requests.select_related("category")
    return render(
        request,
        "requests_app/my_requests.html",
        {"service_requests": service_requests},
    )


@staff_required
def dashboard(request):
    service_requests = ServiceRequest.objects.select_related("category", "citizen")

    search_query = request.GET.get("q", "").strip()
    selected_status = request.GET.get("status", "")
    selected_category = request.GET.get("category", "")

    if search_query:
        service_requests = service_requests.filter(
            Q(location__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(citizen__username__icontains=search_query)
        )
    if selected_status in ServiceRequest.Status.values:
        service_requests = service_requests.filter(status=selected_status)
    if selected_category.isdigit():
        service_requests = service_requests.filter(category_id=selected_category)

    paginator = Paginator(service_requests, DASHBOARD_PAGE_SIZE)
    page_obj = paginator.get_page(request.GET.get("page"))

    params = request.GET.copy()
    params.pop("page", None)

    context = {
        "page_obj": page_obj,
        "query_string": params.urlencode(),
        "categories": Category.objects.all(),
        "status_choices": ServiceRequest.Status.choices,
        "search_query": search_query,
        "selected_status": selected_status,
        "selected_category": selected_category,
        "stats": get_request_stats(),
        "category_breakdown": get_category_breakdown(),
    }
    return render(request, "requests_app/dashboard.html", context)


@staff_required
@require_POST
def update_status(request, pk):
    service_request = get_object_or_404(
        ServiceRequest.objects.select_related("citizen", "category"), pk=pk
    )
    old_status = service_request.status
    form = StatusUpdateForm(request.POST, instance=service_request)

    if form.is_valid():
        form.save()
        if service_request.status != old_status:
            send_status_update_email(service_request)
        messages.success(
            request,
            f"Request #{pk} is now {service_request.get_status_display()}.",
        )
    else:
        messages.error(request, "Invalid status value.")

    next_url = request.POST.get("next", "")
    if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return redirect(next_url)
    return redirect("dashboard")