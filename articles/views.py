from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from articles.forms import ArticleForm
from articles.models import Article


class ArticleView(ListView):
    queryset = Article.objects.order_by('id')
    template_name = 'articles/article.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Articles List'
        return context


class ArticleCreateView(CreateView):
    template_name = 'articles/article_create.html'
    model = Article
    form_class = ArticleForm
    success_url = reverse_lazy('articles')

    def form_valid(self, form):
        return super().form_valid(form)


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('articles')


# TODO: write URL and tests for ArticleDeleteView
# TODO: display form errors in HTML template for Create / Update
# TODO: write ArticleUpdateView
