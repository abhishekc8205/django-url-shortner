"""Functions used by the views."""
from django.db import IntegrityError, transaction

from .models import ShortURL, generate_short_code


def create_short_url(original_url):
    """Create and return a ShortURL for the given destination."""
    # Random codes can theoretically repeat. The database rejects duplicates,
    # so try a new code if that rare case happens.
    for attempt in range(5):
        try:
            with transaction.atomic():
                return ShortURL.objects.create(
                    original_url=original_url,
                    code=generate_short_code(),
                )
        except IntegrityError:
            if attempt == 4:
                raise RuntimeError("Could not create a unique short code. Please try again.")
