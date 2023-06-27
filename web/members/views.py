from datetime import datetime
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from .models import Member
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import MemberForm
from users.views import BlockedUserMixin


class MemberViews(BlockedUserMixin, CreateView):
    model = Member
    form_class = MemberForm
    template_name = 'members/members_registration.html'
    success_url = reverse_lazy('index')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name='editors').exists():
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('contact')

    def form_valid(self, form):
        date_of_birth = form.cleaned_data['date_of_birth']
        gender = form.cleaned_data['gender']
        date_of_birth_str = str(date_of_birth)
        date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
        current_year = datetime.now().year
        birth_year = date_of_birth.year
        calculated_age = current_year - birth_year
        group = f'{calculated_age}{gender}'

        # Заполнение поля age_group формы автоматически
        form.instance.age_group = group

        return super().form_valid(form)
