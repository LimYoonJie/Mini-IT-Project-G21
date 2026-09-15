from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("marketplace", "0006_alter_product_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="marketplaceprofile",
            name="profile_picture",
            field=models.ImageField(blank=True, null=True, upload_to="profile_pictures/"),
        ),
    ]
