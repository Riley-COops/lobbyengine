from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Address (models.Model):
    street = models.CharField(max_length=100)
    address_line = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100)
    country = models.CharField (max_length=100)


class Organisation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=200)
    date_established = models.DateField(auto_now=True)



    def __str__(self):
        return self.name