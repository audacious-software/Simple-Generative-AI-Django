# pylint: disable=line-too-long

import traceback

from ..models import GenerativeAIException

from . import prepare_messages

def run_model(model_obj, prompt, user='openai_user', extras=None):
    if extras is None:
        extras = {}

    parameters = model_obj.fetch_parameters()

    messages = prepare_messages(model_obj, prompt, extras)

    try:
        import openai # pylint: disable=import-outside-toplevel, import-error

        if parameters.get('openai_api_key', None) is not None:
            client = openai.OpenAI(api_key=parameters.get('openai_api_key', '')) # pylint: disable=no-member

            request_obj = {
                'model': parameters.get('openai_model', 'gpt-3.5-turbo'),
                'user': user,
                'messages': messages,
            }

            model_parameters = parameters.get('model_parameters', {})
            request_obj.update(model_parameters)

            try:
                chat_completion = client.chat.completions.create(**request_obj)

                model_obj.log_request(request_obj, chat_completion.model_dump(mode='json'), True)

                return chat_completion.choices[0].message.content
            except openai.APIStatusError as bad_request:
                model_obj.log_request(request_obj, bad_request.response.json(), False)

                raise GenerativeAIException('Error encountered running OpenAI.chat.completions.create.') from bad_request

        if parameters.get('azure_openai_api_key', None) is not None:
            client = openai.AzureOpenAI(api_key=parameters.get('azure_openai_api_key', ''), api_version="2024-07-01-preview", azure_endpoint=parameters.get('azure_openai_endpoint', '')) # pylint: disable=no-member

            request_obj = {
                'model': parameters.get('azure_deployment_name', ''),
                'user': user,
                'messages': messages,
            }

            model_parameters = parameters.get('model_parameters', {})
            request_obj.update(model_parameters)

            try:
                chat_completion = client.chat.completions.create(**request_obj)

                model_obj.log_request(request_obj, chat_completion.model_dump(mode='json'), True)

                return chat_completion.choices[0].message.content
            except openai.APIStatusError as bad_request:
                model_obj.log_request(request_obj, bad_request.response.json(), False)

                raise GenerativeAIException('Error encountered running OpenAI.chat.completions.create.') from bad_request

    except Exception as error:
        response_obj = {
            'stacktrace': traceback.format_exc()
        }

        model_obj.log_request(request_obj, response_obj, False)

        raise GenerativeAIException('Error encountered running OpenAI.chat.completions.create.') from error

    return None

def validate_model(model_obj):
    parameters = model_obj.fetch_parameters()

    issues = []

    parameters = model_obj.fetch_parameters()

    if parameters.get('openai_api_key', None) is None:
        issues.append('Add valid "openai_api_key" or "azure_openai_api_key" parameter to model')

    if parameters.get('openai_model', None) is None:
        issues.append('Specify "openai_model" type parameter for model (see https://platform.openai.com/docs/models)')

    if parameters.get('azure_openai_api_key', None) is not None:
        issues = []

        if parameters.get('azure_openai_endpoint', None) is None:
            issues.append('Specify "azure_openai_endpoint" type parameter for model (see https://github.com/openai/openai-python/tree/main?tab=readme-ov-file#microsoft-azure-openai)')

        if parameters.get('azure_deployment_name', None) is None:
            issues.append('Specify "azure_deployment_name" type parameter for model (see https://github.com/openai/openai-python/tree/main?tab=readme-ov-file#microsoft-azure-openai)')

    return issues
