from rest_framework import serializers

from .models import ShortURL


class ShortURLSerializer(serializers.ModelSerializer):
    """Validate incoming URLs and format ShortURL objects as JSON."""
    short_url = serializers.SerializerMethodField()
    total_clicks = serializers.SerializerMethodField()

    class Meta:
        model = ShortURL
        fields = ["id", "original_url", "code", "short_url", "created_at", "total_clicks"]
        read_only_fields = ["id", "code", "short_url", "created_at", "total_clicks"]

    def get_short_url(self, obj):
        """Build the redirect URL returned to the API caller."""
        request = self.context.get("request")
        relative_url = f"/{obj.code}/"
        return request.build_absolute_uri(relative_url) if request else relative_url

    def get_total_clicks(self, obj):
        """Return the number of recorded visits for this link."""
        return obj.click_events.count()
