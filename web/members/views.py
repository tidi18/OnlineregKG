import ast
from datetime import datetime
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from .models import Member
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import MemberForm
from users.views import BlockedUserMixin, check_blocked
from .models import Competition


@check_blocked
@login_required
def member_success(request):
    return render(request, 'members/member_success.html')


class MemberViews(BlockedUserMixin, CreateView):
    model = Member
    form_class = MemberForm
    template_name = 'members/members_registration.html'
    success_url = reverse_lazy('member_success')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name='editors').exists():
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('contact')

    def form_valid(self, form):
        abc_group = form.cleaned_data.get('abcd_group')
        competition_data = form.cleaned_data['competition']
        competition = Competition.objects.get(id=competition_data.id)
        competition_age_group = competition.age_groups_of_participants
        age_group_list = []
        age_group_list.append(competition_age_group)
        data_list = ast.literal_eval(age_group_list[0])
        age_groups = []
        for sublist in data_list:
            sublist = ast.literal_eval(sublist)
            age_groups.extend(sublist)
        age_groups = list(map(str, age_groups))
        date_of_birth = form.cleaned_data['date_of_birth']
        gender = form.cleaned_data['gender']
        date_of_birth_str = str(date_of_birth)
        date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
        current_year = datetime.now().year
        birth_year = date_of_birth.year
        calculated_age = current_year - birth_year

        if abc_group == None:
            if str(calculated_age) in age_groups:
                group = f'{calculated_age}{gender}'
                form.instance.age_group = group
                return super().form_valid(form)

        else:
            if 'A' in age_groups or 'B' in age_groups or 'C' in age_groups or 'D' in age_groups:
                group = f'{abc_group}'
                form.instance.age_group = group
                return super().form_valid(form)




