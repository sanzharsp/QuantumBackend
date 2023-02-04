# Generated by Django 4.1.5 on 2023-02-03 16:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_jk_alter_user_options_user_date_create_qrcode_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='QrCode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.qrcode', verbose_name='Данные Qr кодов'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='room_number',
            field=models.CharField(db_index=True, max_length=255, unique=True, verbose_name='Пәтер нөмірі'),
        ),
    ]
