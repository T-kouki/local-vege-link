# polls/migrations/0007_product_created_at_product_user.py

from django.db import migrations, models
from django.conf import settings

def set_default_user(apps, schema_editor):
    Product = apps.get_model('polls', 'Product')
    CustomUser = apps.get_model('polls', 'CustomUser')
    default_user = CustomUser.objects.first()  # とりあえず最初のユーザー
    for product in Product.objects.all():
        product.user = default_user
        product.save()

class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='user',
            field=models.ForeignKey(
                to=settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE,
                related_name='products',
                null=True,  # 一時的に null を許可
            ),
        ),
        migrations.RunPython(set_default_user),
        migrations.AlterField(
            model_name='product',
            name='user',
            field=models.ForeignKey(
                to=settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE,
                related_name='products',
            ),
        ),
    ]
