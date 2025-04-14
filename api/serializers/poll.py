from rest_framework import serializers

from poll.models import Poll


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ('title', 'text', 'by', 'time', 'item_id', 'score', 'descendants', 'options')
