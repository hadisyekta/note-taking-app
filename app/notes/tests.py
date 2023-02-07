from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db.models import Q
import json

from notes.models import Notes, Tags


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
        tag1 = Tags.objects.create(title='Tagtest')
        tag1.save()
        n2.tags.add(tag1)
        n3 = Notes(title="mypv search keyword note", body="mypv search note",
                   author=self.user, private=True)
        n3.save()

        user2 = User.objects.create_user(
            username='test2',
            password=make_password('Pas$w0rd123'))

        n1 = Notes(title="shared test2 note", body="public test2 note",
                   author=user2, private=False)
        n1.save()
        n2.tags.add(tag1)

        n2 = Notes(title="pv test2 note", body="pv test2 note",
                   author=user2, private=True)
        n2.save()
        n2.tags.add(tag1)
        n3 = Notes(title="pv search keyword note", body="pv search note",
                   author=user2, private=True)
        n3.save()
        n3 = Notes(title="public search keyword note", body="public search",
                   author=user2, private=True)
        n3.save()
        
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

    def test_list_user_filter_by_tags_notes(self):
        self.client.force_authenticate(self.user)
        tag_id = Tags.objects.filter(title='Tagtest').first().id
        notes_query = Notes.objects.filter(Q(author=self.user) |
                                           Q(private=False))
        notes_count = notes_query.filter(tags__id__exact=tag_id).count()
                                           
        response = self.client.get('/?tags={}'.format(tag_id))
        self.assertEqual(response.data['count'], notes_count)
        self.assertEqual(len(response.data['results']), notes_count)

    def test_list_user_search_by_keyword_notes(self):
        self.client.force_authenticate(self.user)
        notes_query = Notes.objects.filter(Q(author=self.user) |
                                           Q(private=False))
        keyword = 'search'
        notes_count = notes_query.filter(Q(body__icontains=keyword) | 
                                         Q(title__icontains=keyword)).count()
        response = self.client.get('/?search={}'.format(keyword))
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
        response = self.client.post('/mynotes/add', note_attrs)
        self.assertEqual(response.json()["detail"],
                         'Authentication credentials were not provided.')
        self.assertEqual(response.status_code, 403)

    def test_create_note(self):
        self.client.force_authenticate(self.user)
        initial_note_count = Notes.objects.count()        
        note_attrs = {
            'title': 'New Note - Test',
            'body': 'Awesome note',
            'private': True,
            'tags_id': self.tags
        }
        response = self.client.post('/mynotes/add', note_attrs)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            Notes.objects.count(),
            initial_note_count + 1,
        )
        note_attrs.pop('tags_id')
        for attr, expected_value in note_attrs.items():
            self.assertEqual(response.data[attr], expected_value)
        self.assertEqual(response.data['private'], True)
        data = json.loads(json.dumps(response.data))
        # print(data["tags"])
        self.assertEqual([t["id"] for t in data["tags"]], self.tags)


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
        n2.tags.add(tag3)
        # data for other user
        user2 = User.objects.create_user(
            username='test2',
            password=make_password('Pas$w0rd123'))
        # PUBLIC
        n1 = Notes(title="shared test2 note", body="public test2 note",
                   author=user2, private=False)
        n1.save()
        # PRIVTE
        n2 = Notes(title="pv test2 note", body="pv test2 note",
                   author=user2, private=True)
        n2.save()

    # GET testcases
    def test_unauthorized_get_note(self):
        note_id = Notes.objects.first().id
        response = self.client.get('/mynotes/{}/'.format(note_id))
        self.assertEqual(response.json()["detail"],
                         'Authentication credentials were not provided.')
        self.assertEqual(response.status_code, 403)

    def test_get_note_200(self):
        self.client.force_authenticate(self.user)
        note = Notes.objects.filter(author=self.user).first()
        response = self.client.get('/mynotes/{}/'.format(note.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], note.title)
    
    def test_get_note_404(self):
        self.client.force_authenticate(self.user)
        note = Notes.objects.exclude(author=self.user).first()
        response = self.client.get('/mynotes/{}/'.format(note.id))
        self.assertEqual(response.status_code, 404)
    
    # DELETE testcases
    def test_unauthorized_delete_note(self):
        note_id = Notes.objects.first().id
        response = self.client.delete('/mynotes/{}/'.format(note_id))
        self.assertEqual(response.json()["detail"],
                         'Authentication credentials were not provided.')
        self.assertEqual(response.status_code, 403)
    
    def test_delete_note_404(self):
        self.client.force_authenticate(self.user)
        note = Notes.objects.exclude(author=self.user).first()
        response = self.client.delete('/mynotes/{}/'.format(note.id))
        self.assertEqual(response.status_code, 404)

    def test_delete_note(self):
        self.client.force_authenticate(self.user)
        initial_note_count = Notes.objects.count()
        note_id = Notes.objects.filter(author=self.user).first().id
        response = self.client.delete('/mynotes/{}/'.format(note_id))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(
            Notes.objects.count(),
            initial_note_count - 1,
        )
        self.assertRaises(
            Notes.DoesNotExist,
            Notes.objects.get, id=note_id,
        )

    # PATCH testcases
    def test_unauthorized_update_note(self):
        note_id = Notes.objects.first().id
        response = self.client.patch('/mynotes/{}/'.format(note_id))
        self.assertEqual(response.json()["detail"],
                         'Authentication credentials were not provided.')
        self.assertEqual(response.status_code, 403)

    def test_update_Note(self):
        self.client.force_authenticate(self.user)
        note = Notes.objects.filter(author=self.user).first()
        print("", note.id, note.private, note.tags)
        note_new_attr = {
                        'title': 'update Note',
                        'body': 'test update note',
                        'private': False,
                        'tags_id': self.tags
                        }
        self.client.patch(
            '/mynotes/{}/'.format(note.id),
            note_new_attr,
            format='json',
        )
        updated = Notes.objects.get(id=note.id)
        self.assertEqual(updated.title, note_new_attr["title"])
        self.assertEqual(updated.body, note_new_attr["body"])
        self.assertEqual(updated.private, note_new_attr["private"])
        # print(updated.tags.all())
        self.assertEqual([t.id for t in updated.tags.all()], self.tags)

# TODO: Tags Test case
# TODO: User Test case