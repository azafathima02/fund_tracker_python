from django.db import models

class Transaction(models.Model):
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=255)
    date = models.DateField()
    image = models.ImageField(upload_to='transaction_images/', blank=True, null=True)

    def __str__(self):
        return self.title
