# Generated by Django 2.2 on 2022-07-25 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coplate', '0006_review_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.IntegerField(choices=[(1, '*'), (2, '**'), (3, '***'), (4, '****'), (5, '*****')], default=None),
        ),
    ]
