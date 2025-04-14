from itertools import chain

from django.db.models import Q, Count, FilteredRelation
from django.views.generic import TemplateView, DetailView, ListView
from django.urls import reverse_lazy

from story.models import Story
from job.models import Job
from user_account.models import User
from base.scripts import pick_random_image


class HomeView(TemplateView):
    template_name = 'home/home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_stories = Story.objects.select_related('by').all()
        all_jobs = Job.objects.select_related('by').all()
        asks = all_stories.filter(title__startswith="Ask HN")
        shows = all_stories.filter(title__startswith="Show HN")
        stories = all_stories.filter(~Q(title__startswith="Ask HN") & ~Q(title__startswith="Show HN"))
        context['ask_stories'] = asks[5:20]
        context['show_stories'] = shows[5:20]
        context['stories'] = stories[5:20]
        context['jobs'] = all_jobs[5:25]
        context['slide_items'] = chain(asks[:5], shows[:5], stories[:5], all_jobs[:5])
        context['slide_image'] = lambda: pick_random_image('slides')  # change to use AI to generate image
        context['post_landscape'] = lambda: pick_random_image('post-landscapes')
        context['person'] = lambda: pick_random_image('persons')
        return context


class _BaseDetailView(DetailView):
    template_name = 'home/item_detail.html'
    model = Story
    context_object_name = 'item'
    queryset_filter = Q()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['comments'] = self.object.comments.all()
        context['slide_image'] = lambda: pick_random_image('slides')
        context['post_landscape'] = lambda: pick_random_image('post-landscapes')
        context['person'] = lambda: pick_random_image('persons')
        context['comment_image'] = lambda: pick_random_image('comments')
        qs = self.get_queryset()
        context['recent'] = qs.order_by('-last_update', '-time')[:5]
        return context

    def get_queryset(self):
        return self.model.objects.filter(self.queryset_filter).select_related('by').all()


class StoryDetailView(_BaseDetailView):
    ...

class JobDetailView(_BaseDetailView):
    model = Job


class BaseListView(ListView):
    template_name = "home/category.html"
    context_object_name = "items"
    paginate_by = 6
    category = "Story"
    queryset_filter = Q()
    user_related_name = "stories"
    ordering = ("-score",)
    url = reverse_lazy("stories")

    def post(self, request, *args, **kwargs):
        # a way to handle post request in a get view
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # access the GET
        query = self.request.GET.get("query")
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        page = context['page_obj']
        context['pages'] = page.paginator.get_elided_page_range(page.number)
        context['blog'] = lambda: pick_random_image('blogs')
        context['post_landscape'] = lambda: pick_random_image('post-landscapes')
        context['person'] = lambda: pick_random_image('persons')
        queryset = self.get_queryset()
        context['recent'] = queryset.order_by('-last_update', '-time')[:5]
        context['star_user'] = self.set_star_user()
        context['url'] = self.url
        if query:
            queryset = self.get_queryset()
            search_result = queryset.filter(Q(title__icontains=query) | Q(text__icontains=query))[:5]
            context["query"] = query
            context["search_result"] = search_result
        return context

    def set_star_user(self):
        # Prefetch doesn't work
        # qs = self.get_queryset()
        # star_user = (User.objects.prefetch_related(Prefetch(self.user_related_name, queryset=qs))
        #                         .annotate(entry_count=Count(self.user_related_name)).order_by('-entry_count').first())
        
        star_user = (User.objects.annotate(entries=FilteredRelation(self.user_related_name,
                                                                   condition=self.queryset_filter))
                     .annotate(entry_count=Count('entries')).order_by('-entry_count').first())
        return star_user


class AskStoriesView(BaseListView):
    category = 'Ask HN'
    queryset_filter = Q(stories__title__startswith='Ask HN')
    queryset = Story.objects.filter(title__startswith='Ask HN')
    url = reverse_lazy('ask-stories')


class ShowStoriesView(BaseListView):
    category = 'Show HN'
    queryset_filter = Q(stories__title__startswith='Show HN')
    queryset = Story.objects.filter(title__startswith='Show HN')
    url = reverse_lazy('show-stories')


class JobsView(BaseListView):
    category = 'Jobs'
    user_related_name = 'jobs'
    queryset = Job.objects.all()
    url = reverse_lazy('jobs')


class StoriesView(BaseListView):
    queryset = Story.objects.filter(~Q(title__startswith='Show HN') & ~Q(title__startswith='Ask HN'))
    queryset_filter = ~Q(stories__title__startswith='Show HN') & ~Q(stories__title__startswith='Ask HN')
    url = reverse_lazy('stories')
