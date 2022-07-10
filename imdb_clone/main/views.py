from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import (
    DetailView,
    ListView,
    TemplateView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView,
)

from imdb_clone.main.forms import RateForm
from imdb_clone.main.models import Movie, Rating


class HomeView(TemplateView):
    template_name = "index.html"


class MovieDetails(DetailView):
    model = Movie
    fields = ("title", "year", "actors", "genre", "photo", "trailer")
    template_name = "movie_detail.html"


class MovieList(ListView):
    model = Movie
    template_name = "movie_list.html"


class MovieCreate(LoginRequiredMixin, CreateView):
    model = Movie
    # form_class = MovieCreateForm
    fields = ("title", "year", "actors", "genre", "photo", "trailer")
    template_name = "movie_create.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class MovieEdit(LoginRequiredMixin, UpdateView):
    model = Movie
    fields = ("title", "year", "actors", "genre", "photo", "trailer")
    template_name = "movie_edit.html"


class MovieDelete(LoginRequiredMixin, DeleteView):
    model = Movie
    template_name = "movie_delete.html"
    success_url = reverse_lazy("home")


class MyMovies(LoginRequiredMixin, ListView):
    model = Movie
    fields = ("title", "year", "actors", "genre", "photo", "trailer")
    template_name = "my_movies.html"

    def get_queryset(self):
        return Movie.objects.filter(user_id=self.request.user).order_by("title")


class MovieSearch(ListView):
    model = Movie
    template_name = "search_results.html"

    def get_queryset(self):
        query = self.request.GET.get("q")

        object_list = Movie.objects.filter(
            Q(title__icontains=query)
            | Q(year__icontains=query)
            # | Q(avg_rating=query)
            | Q(actors__icontains=query)
            | Q(genre__icontains=query)
        )
        return object_list


class MovieRate(LoginRequiredMixin, FormView):
    model = Rating
    form_class = RateForm
    template_name = "movie_rate.html"
    success_url = reverse_lazy("movie_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.movie_id = self.kwargs["pk"]
        form.save(commit=False)

        try:
            if form.is_valid():
                form.save()
                return super().form_valid(form)
        except IntegrityError:
            return HttpResponse("You already rated this movie.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movie_pk'] = self.kwargs["pk"]
        return context
