from rest_framework import serializers

from notes.models import Notes, Tags


class TagsSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=30)

    class Meta:
        model = Tags
        fields = '__all__'


class NotesSerializer(serializers.ModelSerializer):
    title = serializers.CharField(min_length=2, max_length=100)
    tags = TagsSerializer(read_only=True, many=True)
    tags_id = serializers.PrimaryKeyRelatedField(queryset=Tags.objects.all(), write_only=True,many=True)
    body = serializers.CharField(min_length=2, max_length=500)
    private = serializers.BooleanField()
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Notes
        fields = ('id', 'author', 'title', 'body', 'tags', 'tags_id', 'private', 'created_at','updated_at',)
        read_only_fields = ('id', 'author', 'tags_id', 'created_at','updated_at',)

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request:
            validated_data['author'] = request.user
        print(validated_data)
        tags = validated_data.pop('tags_id')
        note = Notes.objects.create(**validated_data)
        for tag in tags:
            note.tags.add(tag)
        # or : note.tags.add(*tags)

        return note
