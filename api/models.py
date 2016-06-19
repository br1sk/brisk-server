from django.db import models


class Authorization(models.Model):
    token = models.CharField(max_length=100, db_index=True)
    cookie = models.TextField()
    create_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.token


class Product(models.Model):
    identifier = models.CharField(max_length=50, db_index=True)
    name = models.CharField(max_length=100)
    apple_id = models.CharField(max_length=100)
    category = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Classification(models.Model):
    identifier = models.CharField(max_length=50, db_index=True)
    apple_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Reproducibility(models.Model):
    identifier = models.CharField(max_length=50, db_index=True)
    apple_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'reproducibilities'


class Area(models.Model):
    identifier = models.CharField(max_length=50, db_index=True)
    apple_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name
