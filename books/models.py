from django.db import models

# Create your models here.

from django.core.validators import MinValueValidator, MaxValueValidator

class Book(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    genre = models.CharField(max_length=255, blank=True, null=True)
    publication_year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()
    rating = models.FloatField(validators=[MinValueValidator(1.0), MaxValueValidator(5.0)])

    def __str__(self):
        return f"{self.title} by {self.author}"
