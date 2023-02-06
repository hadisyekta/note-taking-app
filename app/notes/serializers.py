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
    body = serializers.CharField(min_length=2, max_length=500)
    private = serializers.BooleanField()
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Notes
        fields = '__all__'
        # exclude = ['author', ]

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request:
            validated_data['author'] = request.user
        print(validated_data)

        return Notes.objects.create(**validated_data)
