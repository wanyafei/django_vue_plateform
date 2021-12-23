from rest_framework import serializers
from apps.demo.models import Book

class demoserializers(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields=('id','book_name','add_time')