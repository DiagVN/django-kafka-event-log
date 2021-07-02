from rest_framework import serializers


class SampleSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    created_at = serializers.DateTimeField()
