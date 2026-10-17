from django.db.models import Count, Q

from .models import Category, ServiceRequest

Status = ServiceRequest.Status


def get_request_stats():
    """Return overall counts of service requests by status."""
    stats = ServiceRequest.objects.aggregate(
        total=Count("id"),
        pending=Count("id", filter=Q(status=Status.PENDING)),
        in_progress=Count("id", filter=Q(status=Status.IN_PROGRESS)),
        resolved=Count("id", filter=Q(status=Status.RESOLVED)),
    )
    stats["open"] = stats["pending"] + stats["in_progress"]
    stats["resolution_rate"] = (
        round(stats["resolved"] / stats["total"] * 100) if stats["total"] else 0
    )
    return stats


def get_category_breakdown():
    """Return categories that have requests, with open and resolved counts."""
    return (
        Category.objects.annotate(
            total=Count("requests"),
            open_count=Count(
                "requests",
                filter=Q(requests__status__in=[Status.PENDING, Status.IN_PROGRESS]),
            ),
            resolved_count=Count(
                "requests",
                filter=Q(requests__status=Status.RESOLVED),
            ),
        )
        .filter(total__gt=0)
        .order_by("-total")
    )