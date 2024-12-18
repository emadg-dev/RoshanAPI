# Generated by Django 5.1.3 on 2024-11-24 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_alter_cart_comment_alter_cart_creator_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='cart',
        ),
        migrations.RenameField(
            model_name='cartitem',
            old_name='creator_user',
            new_name='user',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='comment',
            field=models.TextField(blank=True, default='', max_length=200),
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
    ]
