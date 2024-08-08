# serializers.py

from rest_framework import serializers
from .models import *

class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ['ID', 'data1', 'data2']

  