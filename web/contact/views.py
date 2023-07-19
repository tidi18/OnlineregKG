from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import ContactsForm
from users.views import check_blocked

@login_required
def contacts(request):
    if request.method == 'POST':
        form = ContactsForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'contact/Thank_you.html')
    else:
        form = ContactsForm()
    return render(request, 'contact/contacts.html', {'form': form})

@check_blocked
@login_required
def become_an_editor(request):
    return render(request, 'contact/message_become_an_editor')