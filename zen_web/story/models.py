from django.db import models
from django.contrib.auth import get_user_model

from base.models import Item

class Story(Item):
    by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='stories')
    title = models.TextField()
    url = models.URLField(blank=True, default="https://news.ycombinator.com/")
    text = models.TextField(blank=True, default="")

    class Meta(Item.Meta):
        permissions = [
            ("can_edit", "can edit a story"),
        ]
        db_table = 'stories'
        indexes = [
            models.Index(fields=["title"], name="story_title_idx"),
        ]

    def __str__(self):
        return self.title


class Comment(Item):
    by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments')
    story = models.ForeignKey(Story, on_delete=models.SET_NULL, related_name='comments', null=True)
    # some comments are replies to other comments. This is a recursive many-to-many relationship
    reply = models.ManyToManyField('self', related_name='replies', symmetrical=False, blank=True)

    def __str__(self):
        return f"by_{self.by.username}"

    class Meta(Item.Meta):
        permissions = [
            ("can_edit", "can edit a comment"),
        ]
        db_table = 'comments'
