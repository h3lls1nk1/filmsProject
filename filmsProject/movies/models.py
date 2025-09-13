from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

import uuid

# Create your models here.

class Genre (models.Model):
    """ Géneros cinematográficos """

    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Country (models.Model):
    """ Países """

    name = models.CharField(max_length=100, unique=True)
    iso_code = models.CharField(max_length=2, unique=True) 
    flag_emoji = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f'{self.name} ({self.iso_code})'
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Countries'

class Language (models.Model):
    """ Idiomas """

    name = models.CharField(max_length=100, unique=True)
    iso_code = models.CharField(max_length=5, unique=True)
    native_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class ProductionCompany (models.Model):
    """ Productoras/Estudios """

    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)    
    description = models.TextField(blank=True)
    logo_url = models.URLField(max_length=500, blank=True)
    website = models.URLField(max_length=500, blank=True)
    founded_year = models.PositiveIntegerField(null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Production Companies'

class Movie (models.Model):
    # Identificador único
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    imdb_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    tmdb_id = models.IntegerField(unique=True, null=True, blank=True)

    # Información básica
    title = models.CharField(max_length=500, db_index=True)
    original_title = models.CharField(max_length=500, blank=True)
    alternative_titles = models.JSONField(default=list, blank=True) # Para títulos alternativos (Argentina, Australia...)

    # Fechas
    release_date = models.DateField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True, db_index=True)

    # Duración y formato
    runtime = models.IntegerField(null=True, blank=True) # En minutos

    # Descripción y contenido
    synopsis = models.TextField(blank=True)
    plot_summary = models.TextField(blank=True)
    tagLine = models.CharField(max_length=500, blank=True)

    # Géneros y clasificaciones
    genres = models.ManyToManyField(Genre, blank=True)
    age_rating = models.CharField(max_length=10, blank=True)
    content_warnings = models.JSONField(default=list, blank=True)

    # Idiomas
    production_countries = models.ManyToManyField(Country, blank=True, related_name='movies')
    spoken_languages = models.ManyToManyField(Language, blank=True, related_name='movies')
    original_language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, blank=True, related_name='original_movies')

    # Compañías y producción
    production_companies = models.ManyToManyField(ProductionCompany, blank=True)
    
    def __str__(self):
        return self.title