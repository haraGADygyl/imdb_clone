from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

GENRE_CHOICES = (
    ("Action", "Action"),
    ("Drama", "Drama"),
    ("Comedy", "Comedy"),
    ("Horror", "Horror"),
    ("Sci-Fi", "Sci-Fi"),
)

RATING_CHOICES = (
    (1, "1 - Very bad"),
    (2, "2"),
    (3, "3"),
    (4, "4"),
    (5, "5"),
    (6, "6"),
    (7, "7"),
    (8, "8"),
    (9, "9"),
    (10, "10 - Very good"),
)


class Movie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    year = models.IntegerField()
    actors = models.TextField()
    genre = models.CharField(choices=GENRE_CHOICES, max_length=30)
    photo = models.ImageField(upload_to="posters")
    trailer = models.URLField()

    class Meta:
        ordering = ["title"]

    def ratings_count(self):
        ratings = Rating.objects.filter(movie=self)
        return len(ratings)

    def avg_rating(self):
        average_rating = 0
        ratings = Rating.objects.filter(movie=self)

        for rate in ratings:
            average_rating += int(rate.rate)
        if len(ratings) > 0:
            return average_rating / len(ratings)
        return 0

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rate = models.IntegerField(default=0, choices=RATING_CHOICES)

    class Meta:
        unique_together = [["user", "movie"]]

    def __str__(self):
        return self.movie.title
