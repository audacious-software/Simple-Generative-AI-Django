# pylint: disable=line-too-long

import importlib
import logging

from django.conf import settings
from django.template import Template, Context
from django.template.exceptions import TemplateSyntaxError

def render_prompt(prompt, context_dict):
    prefix = ''

    try:
        for template_load in settings.SIMPLE_GENERATIVE_AI_TEMPLATE_LOADS:
            prefix += '{%% load %s %%}' % template_load
    except AttributeError:
        pass

    try:
        template = Template('%s{%% autoescape off %%}%s{%% endautoescape %%}' % (prefix, prompt))
        context = Context(context_dict)

        return template.render(context)
    except TemplateSyntaxError as ex:
        logging.error('Exception in rendering generative AI template prompt: %s', prompt)
        logging.exception(ex)

        return 'Generative AI prompt parse error: template = "%s", error = %s' % (prompt, ex)

def prepare_messages(model_obj, prompt, extras):
    parameters = model_obj.fetch_parameters()

    system_prompt = parameters.get('system_prompt', '')

    system_prompt_position = parameters.get('system_prompt_position', 'append') # 'append', 'prepend', 'bookend'

    for app in settings.INSTALLED_APPS:
        try:
            gen_ai_module = importlib.import_module('.simple_generative_ai', package=app)

            prompt = gen_ai_module.update_extras_and_prompt(model_obj, prompt, extras)
        except ImportError:
            pass
        except AttributeError:
            pass

    messages = extras.get('messages', [])

    if prompt is not None:
        messages.append({
            'role': 'user',
            'content': prompt
        })

    if system_prompt_position in ('prepend', 'bookend',):
        messages.insert(0, {
            'role': 'system',
            'content': system_prompt
        })

    if system_prompt_position in ('append', 'bookend',):
        messages.append({
            'role': 'system',
            'content': system_prompt
        })

    return messages
