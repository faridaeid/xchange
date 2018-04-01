from django.db import models


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=20, unique=True, null=False)
    password = models.CharField(max_length=30, null=False)
    email_address = models.EmailField(unique=True)
    user_type = models.CharField(max_length=2, null=False)
    phone_number = models.IntegerField()

    class Meta:
        db_table = 'user'
