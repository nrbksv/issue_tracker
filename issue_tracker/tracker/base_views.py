from django.views.generic import ListView, DeleteView
from django.utils.http import urlencode
from django.shortcuts import get_object_or_404, redirect


from tracker.forms import SearchForm


class SearchView(ListView):

    def get(self, request, **kwargs):
        self.form = SearchForm(request.GET)
        self.search_value = self.get_search_value()
        return super().get(request, **kwargs)

    def get_query(self):
        pass

    def get_queryset(self):
        queryset = super().get_queryset().filter(project__is_deleted=False)
        if self.search_value:
            query = self.get_query()
            if query:
                queryset = queryset.filter(query).filter(project__is_deleted=False)
            else:
                queryset = queryset.filter(project__is_deleted=False)
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


class SoftDeleteView(DeleteView):
    success_url = None

    def delete(self, request, *args, **kwargs):
        object = get_object_or_404(self.model, id=self.kwargs.get('pk'))
        object.is_deleted = True
        object.save()
        return redirect(self.success_url)