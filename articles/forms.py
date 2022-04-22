from django.forms import ModelForm

from articles.models import Article


class ArticleForm(ModelForm):

    class Meta:
        model = Article
        fields = ['title', 'text', 'author']

    def clean_title(self):
        return self.cleaned_data.get('title').upper()
