from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Note
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Q
from datetime import date
from django.shortcuts import render


@login_required
def note_list(request):
    query = request.GET.get('q')

    if query:
        notes = Note.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query),
            user=request.user
        )
    else:
        notes = Note.objects.filter(user=request.user)

    return render(request, 'notes/notes_list.html', {'notes': notes, 'query': query})


@login_required
def add_note(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        Note.objects.create(
            title=title,
            content=content,
            user=request.user
        )
        return redirect('note_list')
    return render(request, 'notes/add_note.html')

@login_required
def edit_note(request, id):
    note = get_object_or_404(Note, id=id, user=request.user)
    if request.method == 'POST':
        note.title = request.POST.get('title')
        note.content = request.POST.get('content')
        note.save()
        return redirect('note_list')
    return render(request, 'notes/edit_note.html', {'note': note})

@login_required
def delete_note(request, id):
    note = get_object_or_404(Note, id=id, user=request.user)
    note.delete()
    return redirect('note_list')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)   # auto login after signup
            return redirect('note_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

