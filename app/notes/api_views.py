from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView 
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q


from notes.serializers import TagsSerializer, NotesSerializer
from notes.models import Notes, Tags


class NotesPagination(LimitOffsetPagination):
    default_limit = 4
    max_limit = 10


class NotesList(ListAPIView):
    queryset = Notes.objects.filter(private=False)
    serializer_class = NotesSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('id', 'tags')
    search_fields = ('title', 'body')
    pagination_class = NotesPagination

    def get_queryset(self):
        author = self.request.user
        if author.id:
            queryset = Notes.objects.all()
            return queryset.filter(Q(author=author) | Q(private=False))
        return super().get_queryset()


class NotesCreate(CreateAPIView):
    serializer_class = NotesSerializer
    permission_classes = [IsAuthenticated]

# TODO: add permission error 


class NotesRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    serializer_class = NotesSerializer

    def get(self, request, *args, **kwargs):
        user = self.request.user
        self.queryset = Notes.objects.filter(Q(author=user))
        return super().get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        self.queryset = Notes.objects.filter(Q(author=user))
        note_id = request.data.get('id')
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 204:
            from django.core.cache import cache
            cache.delete('notes_data_{}'.format(note_id))
        return response

    def update(self, request, *args, **kwargs):
        user = self.request.user
        self.queryset = Notes.objects.filter(Q(author=user))
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


class TagsPagination(LimitOffsetPagination):
    default_limit = 5
    max_limit = 10


class TagsList(ListAPIView):
    # TODO: change to ListCreateAPIView 
    permission_classes = [IsAuthenticated]
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    pagination_class = TagsPagination


class TagsCreate(CreateAPIView):
    serializer_class = TagsSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)