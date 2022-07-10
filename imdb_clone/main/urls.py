from django.urls import path

from imdb_clone.main.views import (
    MovieList,
    MovieDetails,
    HomeView,
    MovieCreate,
    MovieEdit,
    MovieDelete,
    MyMovies,
    MovieSearch,
    MovieRate,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("movies/", MovieList.as_view(), name="movie_list"),
    path("movies/<int:pk>/", MovieDetails.as_view(), name="movie_detail"),
    path("movies/add/", MovieCreate.as_view(), name="movie_create"),
    path("movies/edit/<int:pk>/", MovieEdit.as_view(), name="movie_edit"),
    path("movies/delete/<int:pk>/", MovieDelete.as_view(), name="movie_delete"),
    path("movies/rate/<int:pk>/", MovieRate.as_view(), name="movie_rate"),
    path("movies/my-movies/", MyMovies.as_view(), name="my_movies"),
    path("movies/search/", MovieSearch.as_view(), name="movie_search"),
]
