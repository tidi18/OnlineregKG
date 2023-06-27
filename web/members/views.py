from datetime import datetime
from .models import Member
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import MemberForm
from users.views import check_blocked

@check_blocked
@login_required
def members(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            date_of_birth = form.cleaned_data['date_of_birth']
            date_of_birth_str = str(date_of_birth)  # Преобразование в строку
            date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
            gender = form.cleaned_data['gender']
            current_year = datetime.now().year
            birth_year = date_of_birth.year
            calculated_age = current_year - birth_year
            group = f'{calculated_age}{gender}'
            age_group = form.cleaned_data['age_group'] = group
            form.cleaned_data['age_group'] = age_group
            form.save()
            return render(request, 'members/member_success.html')
    else:
        form = MemberForm()
    return render(request, 'members/members_registration.html', {'form': form})
