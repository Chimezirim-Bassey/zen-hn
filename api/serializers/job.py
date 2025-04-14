from rest_framework import serializers

from job.models import Job


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ('title', 'url', 'text', 'by', 'time', 'item_id', 'score')
