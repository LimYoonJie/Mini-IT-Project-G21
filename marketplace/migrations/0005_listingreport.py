from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("marketplace", "0004_product_condition_product_created_at"),
    ]

    operations = [
        migrations.CreateModel(
            name="ListingReport",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("reason", models.CharField(choices=[
                    ("offensive", "Offensive behavior/content"),
                    ("suspicious", "Suspicious account"),
                    ("counterfeit", "Selling counterfeit items"),
                    ("duplicate", "Duplicate posts"),
                    ("prohibited", "Selling prohibited item"),
                    ("mispriced", "Mispriced listing"),
                    ("category", "Item wrongly categorized"),
                    ("keywords", "Irrelevant keywords"),
                    ("other", "Other"),
                ], max_length=20)),
                ("details", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reports", to="marketplace.product")),
                ("reporter", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="listing_reports", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]