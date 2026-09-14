from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("marketplace", "0003_product_seller_chatmessage")]

    operations = [
        migrations.AddField(
            model_name="product",
            name="condition",
            field=models.CharField(
                choices=[
                    ("Brand New", "Brand New"),
                    ("Like New", "Like New"),
                    ("Lightly Used", "Lightly Used"),
                    ("Well Used", "Well Used"),
                    ("Heavily Used", "Heavily Used"),
                ],
                default="Lightly Used",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]