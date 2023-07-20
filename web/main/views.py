from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404
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
import re


@check_blocked
@login_required
def become_an_editor(request):
    return render(request, 'main/message_become_an_editor.html')

@check_blocked
def index(request):
    active_link = 'competitions'
    competitions_data = Competition.objects.order_by('-create_date')
    return render(request, "main/index.html", {'active_link': active_link, 'competitions': competitions_data})

@check_blocked
def news(request):
    active_link = 'news'
    news_data = News.objects.order_by('-date')
    return render(request, "main/index.html", {'active_link': active_link, 'news': news_data})


@check_blocked
@login_required
def profile(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)

        context = {
            'profile': profile,
        }
        return render(request, 'main/profile.html', context)


def change_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            profile = request.user.profile
            profile.photo = form.cleaned_data['photo']
            profile.save()
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
    login_url = '/login/'
    redirect_field_name = 'next'

    def has_profanity(self, text):
        pattern = r"(?iu)\b((у|[нз]а|(хитро|не)?вз?[ыьъ]|с[ьъ]|(и|ра)[зс]ъ?|(о[тб]|под)[ьъ]?|(.\B)+?[оаеи])?-?([её]б(?!о[рй])|и[пб][ае][тц]).*?|(н[иеа]|([дп]|верт)о|ра[зс]|з?а|с(ме)?|о(т|дно)?|апч)?-?ху([яйиеёю]|ли(?!ган)).*?|(в[зы]|(три|два|четыре)жды|(н|сук)а)?-?бл(я(?!(х|ш[кн]|мб)[ауеыио]).*?|[еэ][дт]ь?)|(ра[сз]|[зн]а|[со]|вы?|п(ере|р[оие]|од)|и[зс]ъ?|[ао]т)?п[иеё]зд.*?|(за)?п[ие]д[аое]?р([оа]м|(ас)?(ну.*?|и(ли)?[нщктл]ь?)?|(о(ч[еи])?|ас)?к(ой)|юг)[ауеы]?|манд([ауеыи](л(и[сзщ])?[ауеиы])?|ой|[ао]вошь?(е?к[ауе])?|юк(ов|[ауи])?)|муд([яаио].*?|е?н([ьюия]|ей))|мля([тд]ь)?|лять|([нз]а|по)х|м[ао]л[ао]фь([яию]|[еёо]й))\b"
        lowercase_text = text.lower()

        if re.search(pattern, lowercase_text):
            return True

        return False

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        comment_text = request.POST.get('text', '')
        has_profanity = self.has_profanity(comment_text)

        if request.user.is_authenticated:
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
        else:
            return redirect('login')


def in_editor_group(user):
    return user.groups.filter(name='editors').exists()


@check_blocked
def editors_page(request):
    user = request.user
    editor_group = Group.objects.get(name='editors')
    is_editor = editor_group in user.groups.all()

    if not is_editor:
        return redirect('become_an_editor')

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
def editor_update_competitions(request, pk):
    get_competitions = get_object_or_404(Competition, pk=pk)

    if request.user != get_competitions.author:
        return redirect('become_an_editor')

    if request.method == 'POST':
        form = CompetitionsForm(request.POST, request.FILES, instance=get_competitions)
        if form.is_valid():
            form.save()
            return redirect('editor')
    else:
        form = CompetitionsForm(instance=get_competitions)

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
def editor_update_news(request, pk):
    get_news = get_object_or_404(News, pk=pk)

    if request.user != get_news.author:
        return redirect('become_an_editor')

    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=get_news)
        if form.is_valid():
            form.save()
            return redirect('editor')
    else:
        form = NewsForm(instance=get_news)

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





