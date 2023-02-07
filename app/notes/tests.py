from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db.models import Q

from notes.models import Notes, Tags

# TODO: 
# test for filter by tags
# test for search by keyword
class NotestListTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='test',
            password=make_password('Pas$w0rd123'))
        n1 = Notes(title="shared test note", body="public test note",
                   author=self.user, private=False)
        n1.save()

        n2 = Notes(title="pv test note", body="pv test note",
                   author=self.user, private=True)
        n2.save()
        user2 = User.objects.create_user(
            username='test2',
            password=make_password('Pas$w0rd123'))

        n1 = Notes(title="shared test2 note", body="public test2 note",
                   author=user2, private=False)
        n1.save()

        n2 = Notes(title="pv test2 note", body="pv test2 note",
                   author=user2, private=True)
        n2.save()
        
    def test_list_unauthorized_user_notes(self):
        # check if return public notes
        notes_count = Notes.objects.filter(private=False).count()
        response = self.client.get('')
        self.assertIsNone(response.data['next'])
        self.assertIsNone(response.data['previous'])
        self.assertEqual(response.data['count'], notes_count)
        self.assertEqual(len(response.data['results']), notes_count)
    
    def test_list_user_notes(self):
        # check if return public notes + notes created by user
        self.client.force_authenticate(self.user)
        notes_count = Notes.objects.filter(Q(author=self.user) |
                                           Q(private=False)).count()
        response = self.client.get('')
        self.assertIsNone(response.data['next'])
        self.assertIsNone(response.data['previous'])
        self.assertEqual(response.data['count'], notes_count)
        self.assertEqual(len(response.data['results']), notes_count)

     
class NotesCreateTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='test',
            password=make_password('Pas$w0rd123'))
        tag1 = Tags.objects.create(title='Tagtest')
        tag2 = Tags.objects.create(title='Tagtest2')
        tag3 = Tags.objects.create(title='Tagtest3')
        tag1.save()
        tag2.save()
        tag3.save()
        self.tags = [tag1.id, tag2.id, tag3.id]
    
    def test_unauthorized_create_note(self):
        note_attrs = {
            'title': 'New Note - Test',
            'body': 'Awesome note',
        }
        response = self.client.post('/notes/new', note_attrs)
        self.assertEqual(response.json()["detail"],
                         'Authentication credentials were not provided.')
        self.assertEqual(response.status_code, 403)

    def test_create_note(self):
        self.client.force_authenticate(self.user)
        initial_note_count = Notes.objects.count()
        print("\n initial_note_count", initial_note_count, "\n")
        
        note_attrs = {
            'title': 'New Note - Test',
            'body': 'Awesome note',
            'private': True,
            'tags_id': self.tags
        }
        response = self.client.post('/notes/new', note_attrs)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            Notes.objects.count(),
            initial_note_count + 1,
        )
        note_attrs.pop('tags_id')
        for attr, expected_value in note_attrs.items():
            self.assertEqual(response.data[attr], expected_value)
        self.assertEqual(response.data['private'], True)


class NotesDestroyTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='test',
            password=make_password('Pas$w0rd123'))
        tag1 = Tags.objects.create(title='Tagtest')
        tag2 = Tags.objects.create(title='Tagtest2')
        tag3 = Tags.objects.create(title='Tagtest3')
        tag1.save()
        tag2.save()
        tag3.save()
        self.tags = [tag1.id, tag2.id, tag3.id]
        n1 = Notes(title="shared test note", body="public test note",
                   author=self.user, private=False)
        n1.save()
        n1.tags.add(tag1, tag2)
        n2 = Notes(title="pv test note", body="pv test note",
                   author=self.user, private=True)
        n2.save()
        user2 = User.objects.create_user(
            username='test2',
            password=make_password('Pas$w0rd123'))

        n1 = Notes(title="shared test2 note", body="public test2 note",
                   author=user2, private=False)
        n1.save()

        n2 = Notes(title="pv test2 note", body="pv test2 note",
                   author=user2, private=True)
        n2.save()
    
    def test_unauthorized_get_note(self):
        note_id = Notes.objects.first().id
        response = self.client.get('/notes/{}/'.format(note_id))
        self.assertEqual(response.json()["detail"],
                         'Authentication credentials were not provided.')
        self.assertEqual(response.status_code, 403)

    def test_get_note_200(self):
        self.client.force_authenticate(self.user)
        note = Notes.objects.filter(author=self.user).first()
        response = self.client.get('/notes/{}/'.format(note.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], note.title)
    
    def test_get_note_404(self):
        self.client.force_authenticate(self.user)
        note = Notes.objects.exclude(author=self.user).first()
        response = self.client.get('/notes/{}/'.format(note.id))
        self.assertEqual(response.status_code, 404)
    
    def test_unauthorized_delete_note(self):
        note_id = Notes.objects.first().id
        response = self.client.delete('/notes/{}/'.format(note_id))
        self.assertEqual(response.json()["detail"],
                         'Authentication credentials were not provided.')
        self.assertEqual(response.status_code, 403)
    
    def test_delete_note_404(self):
        self.client.force_authenticate(self.user)
        note = Notes.objects.exclude(author=self.user).first()
        response = self.client.delete('/notes/{}/'.format(note.id))
        self.assertEqual(response.status_code, 404)

    def test_delete_note(self):
        self.client.force_authenticate(self.user)
        initial_note_count = Notes.objects.count()
        note_id = Notes.objects.filter(author=self.user).first().id
        response = self.client.delete('/notes/{}/'.format(note_id))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(
            Notes.objects.count(),
            initial_note_count - 1,
        )
        self.assertRaises(
            Notes.DoesNotExist,
            Notes.objects.get, id=note_id,
        )


# class NotesUpdateTestCase(APITestCase):
#     def test_update_Note(self):
#         note = Notes.objects.first()
#         response = self.client.patch(
#             '/notes/{}/'.format(note.id),
#             {
#                 'title': 'New Note',
#                 'body': 'Awesome note',
#             },
#             format='json',
#         )
#         updated = Notes.objects.get(id=note.id)
#         self.assertEqual(updated.title, 'New Note')