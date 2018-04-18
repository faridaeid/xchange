from django.db import models
#
# ACCOUNT_TYPES = (
#     ('S', 'Seller'),
#     ('B', 'Buyer'),
#     ('BS', 'Both'),
# )
#
#
# class User(models.Model):
#     user_id = models.AutoField(primary_key=True)
#     first_name = models.CharField(max_length=30, null=True)
#     last_name = models.CharField(max_length=30, null=True)
#     username = models.CharField(max_length=20, unique=True, null=False)
#     password = models.CharField(max_length=30, null=False)
#     email_address = models.EmailField(unique=True, null=True)
#
#     class Meta:
#         db_table = 'user'


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    username = models.CharField(unique=True, max_length=20)
    password = models.CharField(max_length=30)
    email_address = models.CharField(unique=True, max_length=254, blank=True, null=True)

    class Meta:
        db_table = 'user'