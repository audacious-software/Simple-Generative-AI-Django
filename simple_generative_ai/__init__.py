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
