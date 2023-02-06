from django.shortcuts import render

# Create your views here.

from django.shortcuts import render

from notes.models import Notes

def noteList(request):
    context = {
        'notes': Notes.objects.all(),
    }
    return render(request, 'notes/notes_list.html', context)

def noteDetails(request, id):
    context = {
        'note': Notes.objects.get(id=id),
    }
    return render(request, 'notes/note.html', context)
