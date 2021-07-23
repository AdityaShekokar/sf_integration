from django.db import models


class Accounts(models.Model):
    class Meta:
        db_table = "accounts"

    id = models.BigAutoField(primary_key=True, unique=True)
    sf_account_id =models.CharField(null=True, blank=True, max_length=255)
    name = models.CharField(null=True, blank=True, max_length=255)
    phone = models.CharField(null=True, blank=True, max_length=255)


class Users(models.Model):
    class Meta:
        db_table = "users"

    id = models.BigAutoField(primary_key=True, unique=True)
    sf_user_id =models.CharField(null=True, blank=True, max_length=255)
    name = models.CharField(null=True, blank=True, max_length=255)
    phone = models.CharField(null=True, blank=True, max_length=255)


class Contacts(models.Model):
    class Meta:
        db_table = "contacts"

    id = models.BigAutoField(primary_key=True, unique=True)
    sf_contact_id = models.CharField(null=True, blank=True, max_length=255)
    name = models.CharField(null=True, blank=True, max_length=255)
    phone = models.CharField(null=True, blank=True, max_length=255)
