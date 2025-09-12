from django.db import models
from django.urls import reverse

class Book(models.Model):
    GENRE_CHOICES = [
        ('FIC', 'Fiction'),
        ('HIS', 'History'),
        ('SCI', 'Science'),
    ]
    title = models.CharField(max_length=50)
    picture = models.ImageField(upload_to="book_pics/", blank=True, null=True)
    author = models.ManyToManyField('Author', blank=True, related_name='books')
    publisher = models.CharField(max_length=50, null=True, blank=True)
    publish_date = models.DateTimeField(null=True, blank=True)
    genre = models.CharField(max_length=3, choices=GENRE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'<Book {self.title} by {self.author}>'

    def get_price(self):
        return f"{self.price} $"

    def get_absolute_url(self):
        return reverse("book-detail", kwargs={"pk": self.pk})

    def get_authors(self):
        return ", ".join(str(author) for author in self.author.all())

class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def __repr__(self):
        return f'<Author {self.first_name} {self.last_name}>'

    def get_absolute_url(self):
        return reverse("author-detail", kwargs={"pk": self.pk})
