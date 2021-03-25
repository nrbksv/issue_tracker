from django.views.generic import ListView
from django.utils.http import urlencode


from tracker.forms import SearchForm


class SearchView(ListView):

    def get(self, request, **kwargs):
        self.form = SearchForm(request.GET)
        self.search_value = self.get_search_value()
        return super().get(request, **kwargs)

    def get_query(self):
        pass

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = self.get_query()
            if query:
                queryset = queryset.filter(query)
            else:
                queryset = queryset.filter()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.form

        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None
