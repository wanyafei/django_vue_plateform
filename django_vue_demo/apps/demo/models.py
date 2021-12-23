from django.db import models
class Book(models.Model):
    book_name = models.CharField(max_length=130)
    add_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.book_name

