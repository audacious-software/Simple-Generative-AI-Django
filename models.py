# pylint: disable=line-too-long, no-member, too-few-public-methods

import importlib
import json

import django

from django.conf import settings
from django.core.checks import Warning, register # pylint: disable=redefined-builtin
from django.db import models
from django.utils import timezone

MODEL_TYPES = (
    ('openai_chat', 'OpenAI Chat'),
    ('openai_chat_legacy', 'OpenAI Chat (Legacy HTTP Only)'),
    ('openai_images', 'OpenAI Images'), # Not yet implemented.
)

# Custom exception for problems with generative AIs
class GenerativeAIException(Exception):
    pass

class GenerativeAIModel(models.Model):
    class Meta:
        verbose_name = 'Generative AI model'
        verbose_name_plural = 'Generative AI models'

    model_type = models.CharField(max_length=128, choices=MODEL_TYPES)

    model_name = models.CharField(max_length=1024)

    model_id = models.SlugField(max_length=128, unique=True, default='new-model')

    enabled = models.BooleanField(default=True)

    model_parameters = models.TextField(max_length=(1024 * 1024), default='{}')

    def __str__(self):
        return '%s (%s)' % (self.model_name, self.model_type)

    def run(self, prompt, extras=None):
        if extras is None:
            extras = {}

        for app in settings.INSTALLED_APPS:
            try:
                gen_ai_module = importlib.import_module('.simple_generative_ai.%s' % self.model_type, package=app)

                return gen_ai_module.run_model(self, prompt, extras=extras)
            except ImportError:
                pass
            except AttributeError:
                pass

        raise GenerativeAIException('Could not find simple_generative_ai.%s.run_model implementation for %s. Prompt: %s' % (self.model_type, self, prompt))

    def fetch_parameters(self):
        return json.loads(self.model_parameters)

    def update_parameters(self, updates):
        parameters = self.fetch_parameters()

        parameters.update(updates)

        self.model_parameters = json.dumps(parameters, indent=2)
        self.save()

    def to_json(self):
        return {
            'name': self.model_name,
            'id': self.model_id
        }

    def fetch_issues(self):
        for app in settings.INSTALLED_APPS:
            try:
                gen_ai_module = importlib.import_module('.simple_generative_ai.%s' % self.model_type, package=app)

                return gen_ai_module.validate_model(self)
            except ImportError:
                pass
            except AttributeError:
                pass

        return ['Locate implementation for model type "%s"' % self.model_type]


    def log_request(self, request_obj, response_obj, successful):
        return GenerativeAIModelRequest.objects.create(model=self, requested=timezone.now(), request=json.dumps(request_obj, indent=2), response=json.dumps(response_obj, indent=2), successful=successful)

class GenerativeAIModelRequest(models.Model):
    class Meta:
        verbose_name = 'Generative AI model request log'
        verbose_name_plural = 'Generative AI request logs'

    def __str__(self):
        return '%s - %s' % (self.model, self.requested)

    model = models.ForeignKey(GenerativeAIModel, related_name='requests', on_delete=models.CASCADE)

    requested = models.DateTimeField()

    request = models.TextField(max_length=(1024*1024)) # pylint: disable=superfluous-parens
    response = models.TextField(max_length=(1024*1024), null=True, blank=True) # pylint: disable=superfluous-parens

    successful = models.BooleanField(default=True)

@register()
def validate_model_configurations(app_configs, **kwargs): # pylint: disable=unused-argument, invalid-name
    errors = []

    if 'simple_generative_ai.W001' in settings.SILENCED_SYSTEM_CHECKS:
        return errors

    try:
        for model in GenerativeAIModel.objects.filter(enabled=True):
            for issue in model.fetch_issues():
                warning_id = 'simple_generative_ai.%s.W001' % model.model_type

                if (warning_id in settings.SILENCED_SYSTEM_CHECKS) is False:
                    warning = Warning('Model "%s" is not properly configured' % model, hint='%s or add "%s" to SILENCED_SYSTEM_CHECKS.' % (issue, warning_id), obj=None, id=warning_id) # pylint: disable=consider-using-f-string

                    errors.append(warning)
    except django.db.utils.ProgrammingError: # Thrown if contents not yet migrated.
        pass

    return errors
