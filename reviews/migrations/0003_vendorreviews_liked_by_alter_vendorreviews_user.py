# Generated by Django 4.1.4 on 2023-02-11 10:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0002_vendorreviews_rating_given'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendorreviews',
            name='liked_by',
            field=models.ManyToManyField(blank=True, related_name='review_liked_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='vendorreviews',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='writer_of_the_review', to=settings.AUTH_USER_MODEL),
        ),
    ]
