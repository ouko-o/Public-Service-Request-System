from django.contrib import admin

from .models import Category, ServiceRequest


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "category", "citizen", "location", "status", "created_at")
    list_filter = ("status", "category")
    search_fields = ("location", "description", "citizen__username")