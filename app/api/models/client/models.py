from django.db import models

    
class Client(models.Model):
    user = models.ForeignKey('api.User', on_delete=models.CASCADE, related_name='clients')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20)
    siren = models.CharField(max_length=9) 

    class Meta: 
        verbose_name = "client"
        verbose_name_plural = "clients"

    def __str__(self):
        return self.name