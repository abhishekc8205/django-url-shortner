"""Views for creating, viewing, and redirecting short links."""
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import ClickEvent, ShortURL
from .serializers import ShortURLSerializer
from .services import create_short_url


def home(request):
    """Show the browser page for creating short links."""
    return render(request, "shortener/home.html")


@api_view(["POST"])
def create_link(request):
    """Create a link from {\"original_url\": \"https://example.com\"}."""
    serializer = ShortURLSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    link = create_short_url(serializer.validated_data["original_url"])
    response_serializer = ShortURLSerializer(link, context={"request": request})
    return Response(response_serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def link_detail(request, code):
    """Return one short link and its click count."""
    link = get_object_or_404(ShortURL, code=code)
    return Response(ShortURLSerializer(link, context={"request": request}).data)


@api_view(["GET"])
def link_analytics(request, code):
    """Return the total number of clicks and the latest 20 clicks."""
    link = get_object_or_404(ShortURL, code=code)
    recent_clicks = list(link.click_events.all()[:20])
    return Response({
        "code": link.code,
        "original_url": link.original_url,
        "total_clicks": link.click_events.count(),
        "last_clicked_at": recent_clicks[0].clicked_at if recent_clicks else None,
        "recent_clicks": [
            {
                "clicked_at": click.clicked_at,
                "referrer": click.referrer,
                "user_agent": click.user_agent,
            }
            for click in recent_clicks
        ],
    })


def redirect_to_original(request, code):
    """Save this visit, then redirect to the original URL."""
    link = get_object_or_404(ShortURL, code=code)
    ClickEvent.objects.create(
        short_url=link,
        referrer=request.META.get("HTTP_REFERER", "")[:2048],
        user_agent=request.META.get("HTTP_USER_AGENT", ""),
    )
    return HttpResponseRedirect(link.original_url)
