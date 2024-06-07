from django.db import models
from bulk_update_or_create import BulkUpdateOrCreateQuerySet


class Currency(models.Model):
    objects = BulkUpdateOrCreateQuerySet.as_manager()
    code = models.CharField(max_length=3, unique=True, default=None)

    def __str__(self):
        return f"{self.code}"


class Country(models.Model):
    objects = BulkUpdateOrCreateQuerySet.as_manager()
    name = models.CharField(max_length=100)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ExchangeRate(models.Model):
    objects = BulkUpdateOrCreateQuerySet.as_manager()
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    date = models.DateField()
    rate = models.DecimalField(max_digits=10, decimal_places=4)

    class Meta:
        unique_together = ('currency', 'date')

    def __str__(self):
        return f"{self.currency} - {self.date}: {self.rate}"


class RelativeChange(models.Model):
    objects = BulkUpdateOrCreateQuerySet.as_manager()
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    date = models.DateField()
    relative_change = models.DecimalField(max_digits=10, decimal_places=4)

    class Meta:
        unique_together = ('currency', 'date')

    def __str__(self):
        return f"{self.currency} - {self.date}: {self.relative_change}"


class BaseDate(models.Model):
    objects = BulkUpdateOrCreateQuerySet.as_manager()
    date = models.DateField(unique=True)

    def __str__(self):
        return str(self.date)
