# Generated by Django 5.0.6 on 2024-06-23 12:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Articles', '0002_entreestock'),
    ]

    operations = [
        migrations.CreateModel(
            name='SortieStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_vente', models.DateField()),
                ('client', models.CharField(max_length=100)),
                ('quantite', models.PositiveIntegerField()),
                ('prix_total', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('nom_article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Articles.article')),
            ],
        ),
    ]