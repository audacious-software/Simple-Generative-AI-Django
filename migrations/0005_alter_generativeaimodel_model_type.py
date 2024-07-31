# pylint: skip-file
# Generated by Django 3.2.25 on 2024-07-03 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simple_generative_ai', '0004_alter_generativeaimodel_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generativeaimodel',
            name='model_type',
            field=models.CharField(choices=[('openai_chat', 'OpenAI Chat'), ('openai_chat_legacy', 'OpenAI Chat (Legacy HTTP Only)'), ('openai_images', 'OpenAI Images')], max_length=128),
        ),
    ]