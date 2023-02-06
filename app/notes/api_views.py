from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend



from notes.serializers import TagsSerializer, NotesSerializer
from notes.models import Notes, Tags


class NotesPagination(LimitOffsetPagination):
    default_limit = 2
    max_limit = 2


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
class NotesList(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Notes.objects.all()
    serializer_class = NotesSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('id', 'tags')
    search_fields = ('title', 'body')
    pagination_class = NotesPagination



class NotesRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Notes.objects.all()
    lookup_field = 'id'
    serializer_class = NotesSerializer

    def delete(self, request, *args, **kwargs):
        note_id = request.data.get('id')
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 204:
            from django.core.cache import cache
            cache.delete('notes_data_{}'.format(note_id))
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            from django.core.cache import cache
            note = response.data
            cache.set('notes_data_{}'.format(note['id']), {
                'title': note['title'],
                'body': note['body'],
                'private': note['private']
            })
        return response