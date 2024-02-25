# pylint: disable=line-too-long

import traceback

from openai import OpenAI

from ..models import GenerativeAIException

def run_model(model_obj, prompt, user='openai_user', extras=None):
    if extras is None:
        extras = {}

    parameters = model_obj.fetch_parameters()

    client = OpenAI(api_key=parameters.get('openai_api_key', ''))

    messages = extras.get('messages', [])

    messages.append({
        'role': 'user',
        'content': prompt
    })

    request_obj = {
        'model': parameters.get('openai_model', 'gpt-3.5-turbo'),
        'user': user,
        'messages': messages,
    }

    try:
        chat_completion = client.chat.completions.create(**request_obj)

        model_obj.log_request(request_obj, chat_completion.model_dump(mode='json'), True)

        return chat_completion.choices[0].message.content
    except Exception as error:
        response_obj = {
            'stacktrace': traceback.format_exc()
        }

        model_obj.log_request(request_obj, response_obj, False)

        raise GenerativeAIException('Error encountered running OpenAI.chat.completions.create.') from error

def validate_model(model_obj):
    parameters = model_obj.fetch_parameters()

    issues = []

    parameters = model_obj.fetch_parameters()

    if parameters.get('openai_api_key', None) is None:
        issues.append('Add valid "openai_api_key" parameter to model')

    if parameters.get('openai_model', None) is None:
        issues.append('Specify "openai_model" type parameter for model (see https://platform.openai.com/docs/models)')

    return issues
