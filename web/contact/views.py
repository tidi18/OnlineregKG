from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import ContactsForm

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

