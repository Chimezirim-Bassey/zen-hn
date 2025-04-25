from django.conf import settings
from django.db import models
from django.urls import reverse

from base.models import Item


class Job(Item):
    by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='jobs')
    url = models.URLField(blank=True, default="https://news.ycombinator.com/")
    text = models.TextField(blank=True, default="")
    title = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('job-detail', kwargs={'pk': self.pk})

    class Meta(Item.Meta):
        permissions = [
            ("can_edit", "can edit job posting"),
        ]
        db_table = 'jobs'
        indexes = [
            models.Index(fields=["title"], name="job_title_idx"),
        ]
