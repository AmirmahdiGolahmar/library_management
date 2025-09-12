import random
from datetime import timedelta, date

from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from library.models import Author, Book
import os

from library_management import settings


class Command(BaseCommand):
    help = "Seed the database with Authors and Books."

    def add_arguments(self, parser):
        parser.add_argument("--authors", type=int, default=15, help="Number of authors to create")
        parser.add_argument("--books", type=int, default=40, help="Number of books to create")
        parser.add_argument("--clear", action="store_true", help="Delete existing Authors/Books first")

    def handle(self, *args, **opts):
        fake = Faker()
        num_authors = opts["authors"]
        num_books = opts["books"]

        if opts["clear"]:
            self.stdout.write(self.style.WARNING("Clearing existing data..."))
            Book.objects.all().delete()
            Author.objects.all().delete()

        # --- Authors ---
        self.stdout.write(f"Creating {num_authors} authors...")
        authors = []
        for _ in range(num_authors):
            first = fake.first_name()
            last = fake.last_name()
            email = f"{first}.{last}@example.com".lower()
            birth = fake.date_between_dates(
                date_start=date(1940, 1, 1), date_end=date(2000, 12, 31)
            )
            bio = fake.paragraph(nb_sentences=3)  # 🔹 متن کوتاه برای بیوگرافی
            authors.append(
                Author(
                    first_name=first,
                    last_name=last,
                    email=email,
                    birth_date=birth,
                    bio=bio
                )
            )
        Author.objects.bulk_create(authors)
        authors = list(Author.objects.all())

        # --- Books ---
        def random_publish_datetime():
            end = timezone.now()
            start = end - timedelta(days=40 * 365)
            naive = fake.date_time_between(start_date=start, end_date=end)
            return (
                timezone.make_aware(naive, timezone.get_current_timezone())
                if timezone.is_naive(naive)
                else naive
            )

        GENRE_CODES = [choice[0] for choice in Book.GENRE_CHOICES]

        self.stdout.write(f"Creating {num_books} books...")
        books = []

        IMAGE_DIR = os.path.join(settings.MEDIA_ROOT, "book_pics")
        image_files = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
        BASE_PIC = "book_pics"

        for _ in range(num_books):
            title = fake.sentence(nb_words=4).rstrip(".")
            publisher = fake.company()[:50]
            publish_dt = random_publish_datetime()
            genre = random.choice(GENRE_CODES)
            pic = f"{BASE_PIC}/{random.choice(image_files)}"

            price = fake.pyfloat(left_digits=2, right_digits=2, positive=True, min_value=5, max_value=100)

            books.append(
                Book(
                    title=title[:50],
                    publisher=publisher,
                    publish_date=publish_dt,
                    genre=genre,
                    picture=pic,
                    price=price,
                )
            )

        Book.objects.bulk_create(books)

        # --- M2M assignments (بعد از ذخیره Books)
        books = list(Book.objects.all())
        for b in books:
            count = random.randint(1, min(3, len(authors)))
            b.author.set(random.sample(authors, count))

        self.stdout.write(
            self.style.SUCCESS(
                f"Done! Authors: {Author.objects.count()}, Books: {Book.objects.count()}"
            )
        )
