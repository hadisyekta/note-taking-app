from rest_framework.generics import ListAPIView


from notes.serializers import TagsSerializer, NotesSerializer
from notes.models import Notes, Tags




class NotesList(ListAPIView):
    queryset = Notes.objects.all()
    serializer_class = NotesSerializer

