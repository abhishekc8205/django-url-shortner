"""Database models for short links and their click events."""
import secrets
import string

from django.db import models


def generate_short_code(length=7):
    """Return a URL-safe, human-friendly code.

    Uniqueness is also enforced by the database. The view retries if the very
    unlikely event of a random collision occurs.
    """
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


class ShortURL(models.Model):
    original_url = models.URLField(max_length=2048)
    code = models.CharField(max_length=12, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.code} -> {self.original_url}"


class ClickEvent(models.Model):
    """A single redirect request, stored separately for useful analytics."""
    short_url = models.ForeignKey(ShortURL, related_name="click_events", on_delete=models.CASCADE)
    clicked_at = models.DateTimeField(auto_now_add=True, db_index=True)
    referrer = models.URLField(max_length=2048, blank=True)
    user_agent = models.TextField(blank=True)

    class Meta:
        ordering = ["-clicked_at"]
        indexes = [models.Index(fields=["short_url", "clicked_at"])]
