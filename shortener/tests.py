from django.test import TestCase
from django.urls import reverse

from .models import ShortURL


class URLShortenerTests(TestCase):
    def test_create_link_and_redirect_tracks_click(self):
        response = self.client.post(
            reverse("create-link"),
            data={"original_url": "https://example.com/page"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        code = response.json()["code"]

        redirect_response = self.client.get(f"/{code}/")
        self.assertEqual(redirect_response.status_code, 302)
        self.assertEqual(redirect_response["Location"], "https://example.com/page")
        self.assertEqual(ShortURL.objects.get(code=code).click_events.count(), 1)

    def test_analytics_reports_total_clicks(self):
        link = ShortURL.objects.create(original_url="https://example.com", code="example1")
        self.client.get(f"/{link.code}/")

        response = self.client.get(reverse("link-analytics", args=[link.code]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["total_clicks"], 1)
