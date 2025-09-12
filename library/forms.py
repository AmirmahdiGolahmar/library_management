from django import forms
from .models import Book, Author

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ["first_name", "last_name", "email", "birth_date", "bio"]
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
            "bio": forms.Textarea(attrs={"rows": 4}),
        }

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            "title",
            "picture",
            "author",
            "price",
            "publisher",
            "publish_date",
            "genre",
        ]
        widgets = {
            "author": forms.SelectMultiple(attrs={"size": 8}),
            "publish_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    # Optional: clean publish_date from HTML5 datetime-local (no TZ)
    def clean_publish_date(self):
        dt = self.cleaned_data.get("publish_date")
        return dt
