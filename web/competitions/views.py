from .models import Competition
from users.views import BlockedUserMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from .forms import CompetitionsForm


class CompetitionCreateView(BlockedUserMixin, CreateView):
    model = Competition
    form_class = CompetitionsForm
    template_name = 'competitions/competition.html'
    success_url = reverse_lazy('editor')

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

    def form_invalid(self, form):
        if 'organizer_phone' in form.errors or 'organizer_telegram' in form.errors or 'organizer_whatsapp' in form.errors:
            form.add_error(None, 'Необходимо заполнить хотя бы одно из полей "Номер телефона организатора", "Telegram организатора" или "WhatsApp организатора".')
        return super().form_invalid(form)


