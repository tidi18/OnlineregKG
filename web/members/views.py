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
            form.save()
            return render(request, 'members/member_success.html')
    else:
        form = MemberForm()
    return render(request, 'members/members_registration.html', {'form': form})

