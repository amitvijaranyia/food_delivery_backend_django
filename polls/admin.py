from polls.models import Choice, Question
from django.contrib import admin

# Register your models here.
admin.site.register(Question)
admin.site.register(Choice)