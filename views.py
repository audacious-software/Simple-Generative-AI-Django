# pylint: disable=no-member, line-too-long

import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import GenerativeAIModel

@csrf_exempt
def models_json(request): # pylint: disable=unused-argument
    models_list = []

    for gen_ai_model in GenerativeAIModel.objects.filter(enabled=True).order_by('model_name'):
        models_list.append(gen_ai_model.to_json())

    return HttpResponse(json.dumps(models_list, indent=2), content_type='application/json', status=200)
