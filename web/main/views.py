from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from competitions.models import Competition
from django.views.generic.edit import FormMixin
from competitions.forms import CommentForm
from competitions.forms import CompetitionsForm
from news.models import News
from news.forms import NewsForm
from users.models import Profile
from users.views import check_blocked, BlockedUserMixin
from users.forms import PhotoForm


def index(request):
    active_link = 'competitions'
    competitions_data = Competition.objects.order_by('-create_date')
    return render(request, "main/index.html", {'active_link': active_link, 'competitions': competitions_data})


def news(request):
    active_link = 'news'
    news_data = News.objects.all()
    return render(request, "main/index.html", {'active_link': active_link, 'news': news_data})


def profile(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)

        context = {
            'profile': profile,
        }
        return render(request, 'main/profile.html', context)


def change_photo(request):
    if request.method == 'POST':
        # Получите новую фотографию из запроса и выполните необходимые действия
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            profile = request.user.profile
            profile.photo = form.cleaned_data['photo']
            profile.save()
            # Перенаправьте пользователя на страницу профиля после изменения фотографии
            return redirect('profile')
    else:
        form = PhotoForm()
    return render(request, 'main/photo.html', {'form': form})


def blocked_view(request):
    return render(request, 'main/blocked.html')


class CompetitionDetailView(BlockedUserMixin, FormMixin, DetailView):
    model = Competition
    template_name = 'main/competition_detail.html'
    form_class = CommentForm
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    @method_decorator(login_required, name='get')
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def has_profanity(self, text):
        profanities = ['хуй', 'пизда', 'иди на хуй', 'заволи ебало', 'ебать', 'блять', 'пиздец', 'соси']
        lowercase_text = text.lower()

        for profanity in profanities:
            if profanity in lowercase_text:
                return True

        return False

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Получаем объект Competition
        form = CommentForm(request.POST)
        comment_text = request.POST.get('text', '')
        has_profanity = self.has_profanity(comment_text)

        if form.is_valid() and not has_profanity:
            comment = form.save(commit=False)
            comment.competition = self.object
            comment.author = self.request.user
            comment.save()
            return redirect('competition_detail', slug=self.object.slug)
        else:
            if has_profanity:
                form.add_error('text', 'Комментарий содержит недопустимые слова.')
                user = request.user
                profile = Profile.objects.get(user=user)
                profile.is_blocked = True
                profile.save()
                return redirect('blocked')
            return self.render_to_response(self.get_context_data(form=form))


def in_editor_group(user):
    return user.groups.filter(name='editors').exists()


@check_blocked
def editors_page(request):
    user = request.user
    editor_group = Group.objects.get(name='editors')
    is_editor = editor_group in user.groups.all()

    if not is_editor:
        return redirect('contact')

    competitions = Competition.objects.filter(author=user)
    news = News.objects.filter(author=user)
    context = {
        'is_editor': is_editor,
        'competitions': competitions,
        'news': news,
    }

    return render(request, 'main/editor.html', context)


@check_blocked
@user_passes_test(in_editor_group)
def editor_update_competitions(request, slug):
    get_competitions = Competition.objects.get(slug=slug)

    if get_competitions.author != request.user:
        return redirect('contact')

    if request.method == 'POST':
        form = CompetitionsForm(request.POST, instance=get_competitions)
        if form.is_valid():
            form.save()
            return redirect('editor')

    else:
        form = CompetitionsForm(instance=get_competitions, initial={'date': get_competitions.date})

    context = {
        'form': form,
        'get_competitions': get_competitions,
        'update': True,
        'title': 'Форма редактирования соревнований'
    }
    return render(request, 'main/editor.html', context)


@check_blocked
@user_passes_test(in_editor_group)
def editor_delete_competitions(request, pk):
    get_competitions = Competition.objects.get(pk=pk)
    get_competitions.delete()
    return redirect('editor')


@check_blocked
@user_passes_test(in_editor_group)
def editor_update_news(request, slug):
    get_news = News.objects.get(slug=slug)

    if get_news.author != request.user:
        return redirect('contact')

    if request.method == 'POST':
        form = NewsForm(request.POST, instance=get_news)
        if form.is_valid():
            form.save()
            return redirect('editor')
    else:
        form = NewsForm(instance=get_news, initial={'date': get_news.date})
    context = {
        'form': form,
        'get_news': get_news,
        'update': True,
        'title': 'Форма редактирования новостей'
    }
    return render(request, 'main/editor.html', context)


@check_blocked
@user_passes_test(in_editor_group)
def editor_delete_news(request, pk):
    get_news = News.objects.get(pk=pk)
    get_news.delete()
    return redirect('editor')


@check_blocked
def about(request):
    return render(request, "main/about.html")





