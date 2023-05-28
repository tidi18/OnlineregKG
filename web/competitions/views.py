from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from .forms import CompetitionsForm
from .models import Competition
from django.views.generic.edit import CreateView
from users.views import BlockedUserMixin


class CompetitionCreateView(BlockedUserMixin, CreateView):
    model = Competition
    form_class = CompetitionsForm
    template_name = 'competitions/competition.html'
    success_url = reverse_lazy('index')

    @method_decorator(login_required, name='get')
    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name='editors').exists():
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('contact')

    def form_valid(self, form):
        competition = form.save(commit=False)
        competition.author = self.request.user
        competition.save()
        return super().form_valid(form)