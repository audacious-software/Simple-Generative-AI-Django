from django.contrib import admin
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from .models import GenerativeAIModel, GenerativeAIModelRequest

@admin.register(GenerativeAIModel)
class GenerativeAIModelAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'model_type', 'enabled')

    list_filter = ('enabled', 'model_type',)

    search_fields = ('model_name', 'model_type', 'model_parameters',)

    readonly_fields = ('help_text',)

    def help_text(self, instance):
        context = {
            'model': instance,
        }

        return mark_safe(render_to_string('admin/simple_generative_ai_model__help_text.html', context))

@admin.register(GenerativeAIModelRequest)
class GenerativeAIModelRequestAdmin(admin.ModelAdmin):
    list_display = ('model', 'requested', 'successful',)

    list_filter = ('successful', 'requested', 'model',)

    search_fields = ('request', 'response',)
