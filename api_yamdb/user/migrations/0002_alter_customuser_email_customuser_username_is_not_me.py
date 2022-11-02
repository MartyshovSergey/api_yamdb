# Generated by Django 4.1.3 on 2022-11-02 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Email'),
        ),
        migrations.AddConstraint(
            model_name='customuser',
            constraint=models.CheckConstraint(check=models.Q(('username__iexact', 'me'), _negated=True), name='username_is_not_me'),
        ),
    ]
