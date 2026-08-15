# Generated manually to keep the starter project immediately runnable.
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ShortURL",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("original_url", models.URLField(max_length=2048)),
                ("code", models.CharField(db_index=True, max_length=12, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="ClickEvent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("clicked_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("referrer", models.URLField(blank=True, max_length=2048)),
                ("user_agent", models.TextField(blank=True)),
                ("short_url", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="click_events", to="shortener.shorturl")),
            ],
            options={"ordering": ["-clicked_at"]},
        ),
        migrations.AddIndex(
            model_name="clickevent",
            index=models.Index(fields=["short_url", "clicked_at"], name="shortener_c_short_u_3b32dd_idx"),
        ),
    ]
