# pylint: disable=no-member, line-too-long, fixme

import importlib
import json
import logging
import traceback

from django.conf import settings

from django_dialog_engine.dialog import BaseNode, DialogTransition, fetch_default_logger

from .models import GenerativeAIModel, GenerativeAIException

class GenerativeAITextNode(BaseNode):
    @staticmethod
    def parse(dialog_def):
        if dialog_def['type'] == 'simple-generative-ai-text':
            try:
                text_node = GenerativeAITextNode(dialog_def['id'], dialog_def['next_id'], dialog_def.get('error_id', None), dialog_def['model_id'], dialog_def['prompt'], dialog_def['key'])

                return text_node
            except KeyError:
                traceback.print_exc()

        return None

    def __init__(self, node_id, next_node_id, error_node_id, model_id, prompt, key):# pylint: disable=too-many-arguments
        super(GenerativeAITextNode, self).__init__(node_id, node_id) # pylint: disable=super-with-arguments

        self.next_node_id = next_node_id
        self.error_node_id = error_node_id
        self.model_id = model_id
        self.prompt = prompt
        self.key = key

        if self.error_node_id is None:
            logging.error('"error_id" is empty for GenerativeAITextNode with id "%s".', self.node_id)

    def node_type(self):
        return 'simple-generative-ai-text'

    def str(self):
        definition = {
            'id': self.node_id,
            'next_id': self.next_node_id,
            'error_id': self.error_node_id,
            'model_id': self.model_id,
            'prompt': self.prompt,
            'key': self.key,
        }

        return json.dumps(definition, indent=2)

    def evaluate(self, dialog, response=None, last_transition=None, extras=None, logger=None): # pylint: disable=too-many-arguments, too-many-locals, too-many-branches, too-many-statements, unused-argument
        prompt_variables = {}

        if dialog.metadata is not None:
            prompt_variables.update(dialog.metadata)

        if extras is not None:
            prompt_variables.update(extras)

        if logger is None:
            logger = fetch_default_logger()

        try:
            model = GenerativeAIModel.objects.filter(model_id=self.model_id).first()

            if model is None:
                raise GenerativeAIException('Model with ID "%s" not found.' % self.model_id)

            rendered_prompt = None

            for app in settings.INSTALLED_APPS:
                try:
                    gen_ai_module = importlib.import_module('.simple_generative_ai', package=app)

                    rendered_prompt = gen_ai_module.render_prompt(self.prompt, prompt_variables)
                except ImportError:
                    pass
                except AttributeError:
                    pass

            response = model.run(rendered_prompt, extras)

            transition = DialogTransition(new_state_id=self.next_node_id)

            transition.metadata['reason'] = 'set-variable-generative-ai-text'
            transition.metadata['exit_actions'] = [{
                'type': 'store-value',
                'key': self.key,
                'value': response
            }]

            return transition

        except GenerativeAIException:
            transition = DialogTransition(new_state_id=self.error_node_id)

            transition.metadata['reason'] = 'generative-ai-error'
            transition.metadata['exit_actions'] = []
            transition.metadata['stacktrace'] = traceback.format_exc()

            return transition

    def actions(self):
        return []

    def next_nodes(self):
        nodes = [
            (self.next_id, 'Success',),
            (self.error_id, 'Error',),
        ]

        return nodes


def dialog_builder_cards():
    return [
        ('Generative AI Text', 'simple-generative-ai-text',),
    ]


def identify_script_issues(script): # pylint: disable=too-many-locals, too-many-branches
    issues = []

    for node in script.definition: # pylint: disable=too-many-nested-blocks
        if node['type'] == 'simple-generative-ai-text':
            model_id = node.get('model_id', None)

            model = GenerativeAIModel.objects.filter(model_id=model_id).first()

            if model is None:
                issues.append(('error', 'Unable to locate generative AI model with ID %s' % model_id))
            else:
                if model.enabled is False:
                    issues.append(('error', 'Generative AI model "%s" is currently disabled.' % model))

    return issues
