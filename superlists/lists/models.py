from django.db import models

class List(models.Model):
    pass

class Item(models.Model):
    text = models.TextField()
    list = models.ForeignKey(List)

    class Meta:
        ordering = ('id',)
        unique_together = ('list', 'text')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.text
