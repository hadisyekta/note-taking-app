from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from django.contrib.auth.models import User
from notes.models import Notes
from notes.api_views import NotesCreate


class NotesCreateTestCase(APITestCase):
    def test_create_note(self):
        client = APIClient()
        client.login(username='oto', password="%oTo*123")
        initial_note_count = Notes.objects.count()
        note_attrs = {
            'title': 'New Note - Test',
            'body': 'Awesome note',
        }
        response = self.client.post('/notes/new', note_attrs)
        if response.status_code != 201:
            print(response.data)
        self.assertEqual(
            Notes.objects.count(),
            initial_note_count + 1,
        )
        for attr, expected_value in note_attrs.items():
            self.assertEqual(response.data[attr], expected_value)
        self.assertEqual(response.data['private'], True)

    
class NotestListTestCase(APITestCase):
    def test_list_notes(self):
        notes_count = Notes.objects.count()
        response = self.client.get('')
        self.assertIsNone(response.data['next'])
        self.assertIsNone(response.data['previous'])
        self.assertEqual(response.data['count'], notes_count)
        self.assertEqual(len(response.data['results']), notes_count)


class NotesDestroyTestCase(APITestCase):
    def test_delete_note(self):
        initial_note_count = Notes.objects.count()
        print("helllooooooooooooooooooooo   ", Notes.objects.first())
        note_id = Notes.objects.first().id
        self.client.delete('/notes/{}/'.format(note_id))
        self.assertEqual(
            Notes.objects.count(),
            initial_note_count - 1,
        )
        self.assertRaises(
            Notes.DoesNotExist,
            Notes.objects.get, id=note_id,
        )