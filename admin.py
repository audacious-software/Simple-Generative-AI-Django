from django.contrib import admin

from .models import GenerativeAIModel, GenerativeAIModelRequest

@admin.register(GenerativeAIModel)
class GenerativeAIModelAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'model_type', 'enabled')

    list_filter = ('enabled', 'model_type',)

    search_fields = ('model_name', 'model_type', 'model_parameters',)

@admin.register(GenerativeAIModelRequest)
class GenerativeAIModelRequestAdmin(admin.ModelAdmin):
    list_display = ('model', 'requested', 'successful',)

    list_filter = ('successful', 'requested', 'model',)

    search_fields = ('request', 'response',)
