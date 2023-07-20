from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from .forms import NewsForm
from .models import News
from users.views import BlockedUserMixin


class NewsView(BlockedUserMixin, CreateView):
    model = News
    form_class = NewsForm
    template_name = 'news/news.html'
    success_url = reverse_lazy('editor')

    @method_decorator(login_required, name='get')
    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name='editors').exists():
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('contact')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)





