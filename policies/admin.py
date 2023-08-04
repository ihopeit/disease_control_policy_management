from django.contrib import admin


from .models import Policy, DiseaseType

admin.site.register(Policy)
admin.site.register(DiseaseType)