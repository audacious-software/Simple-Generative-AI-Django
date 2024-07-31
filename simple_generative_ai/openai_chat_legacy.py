# pylint: disable=line-too-long

import requests

def run_model(model_obj, prompt, user='openai_user', extras=None):
    if extras is None:
        extras = {}

    parameters = model_obj.fetch_parameters()

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

    response = requests.post('https://api.openai.com/v1/chat/completions',
          headers = {
              'Content-Type': 'application/json',
              'Authorization': 'Bearer %s' % parameters.get('openai_api_key', '')
          },
          json={
              'model': parameters.get('openai_model', 'gpt-3.5-turbo'),
              'messages': messages,
              'max_tokens': 500
          }, timeout=60)

    response_json = response.json()

    model_obj.log_request(request_obj, response_json, True)

    return response_json.get('choices', [])[0].get('message', {}).get('content', '(No content returned.)')


def validate_model(model_obj):
    parameters = model_obj.fetch_parameters()

    issues = []

    parameters = model_obj.fetch_parameters()

    if parameters.get('openai_api_key', None) is None:
        issues.append('Add valid "openai_api_key" parameter to model')

    if parameters.get('openai_model', None) is None:
        issues.append('Specify "openai_model" type parameter for model (see https://platform.openai.com/docs/models)')

    return issues
