# Generated by Django 4.0.2 on 2022-02-23 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0004_alter_produto_imagem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='imagem',
            field=models.ImageField(default='teste/Novas_imagens.png', upload_to='imagens/%Y/%m'),
        ),
    ]
