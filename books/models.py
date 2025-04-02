from django.db import models

# Create your models here.

from django.core.validators import MinValueValidator, MaxValueValidator

class Book(models.Model):
    title = models.CharField(max_length=255, blank=False)
    author = models.CharField(max_length=255, blank=False)
    genre = models.CharField(max_length=255, blank=False)
    publication_year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    stock_quantity = models.PositiveIntegerField()
    rating = models.FloatField(validators=[MinValueValidator(1.0), MaxValueValidator(5.0)])

    def __str__(self):
        return f"{self.title} by {self.author}"
