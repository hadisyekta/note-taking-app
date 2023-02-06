from rest_framework import serializers

from notes.models import Notes, Tags


class TagsSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=30)

    class Meta:
        model = Tags


class NotesSerializer(serializers.ModelSerializer):
    title = serializers.CharField(min_length=2, max_length=100)
    tag = TagsSerializer(read_only=True, many=True)
    body = serializers.CharField(min_length=2, max_length=500)
    private = serializers.BooleanField()

    class Meta:
        model = Notes
        fields = ('id', 'title', 'tag', 'body', 'private')
