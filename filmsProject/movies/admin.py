from django.contrib import admin

from .models import Movie, Country, Genre, Language, ProductionCompany

# Register your models here.

admin.site.register([Movie, Country, Genre, Language, ProductionCompany])
