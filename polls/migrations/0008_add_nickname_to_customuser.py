from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_product_created_at_product_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='nickname',
            field=models.CharField(max_length=30, blank=True),
        ),
    ]
