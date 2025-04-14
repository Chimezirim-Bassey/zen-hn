from django.db import models
from django.utils.timezone import now
from django.urls import reverse
# from django.contrib.auth import get_user_model
# from django.conf import settings


class ItemType(models.TextChoices):
    job = 'job'
    story = 'story'
    comment = 'comment'
    poll = 'poll'
    pollopt = 'pollopt'


class Item(models.Model):
    item_id = models.BigIntegerField(primary_key=True)
    time = models.DateTimeField(default=now)
    last_update = models.DateTimeField(auto_now=True, blank=True)
    deleted = models.BooleanField(default=False, blank=True)
    # can use get_user_model()
    # but settings.AUTH_USER_MODEL is the right choice here
    # by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='items')
    dead = models.BooleanField(default=False, blank=True)
    type = models.CharField(max_length=10, choices=ItemType)
    text = models.TextField(default="")
    score = models.IntegerField(default=0, blank=True)
    descendants = models.IntegerField(default=0, blank=True)

    class Meta:
        abstract = True
        ordering = ('-time', '-score')
        indexes = [
            models.Index(fields=["type"])
        ]

    def __str__(self):
        return f'{self.item_id}'

    def get_absolute_url(self):
        return reverse(f'{self.type}-detail', kwargs={'pk': self.pk})

    def get_update_url(self):
        return reverse(f'{self.type}-update', kwargs={'pk': self.pk})
