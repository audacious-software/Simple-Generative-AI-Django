# pylint: disable=line-too-long, no-member, import-outside-toplevel

import json
import logging
import traceback

from openai import OpenAI

from django.utils import timezone

def moderate(request, moderator):
    logger = logging.getLogger()

    try:
        from simple_moderation.models import ModerationDecision # pylint: disable=import-error

        if moderator.moderator_id.startswith('open-ai:'):
            model = moderator.metadata.get('openai_model', None)
            api_key = moderator.metadata.get('openai_api_key', None)

            if None in (model, api_key,):
                return (None, None)

            logger.warning('simple_generative_ai.moderate: %s -- %s', request, moderator)

            client = OpenAI(api_key=api_key)

            results = client.moderations.create(model=model, input=request.message).model_dump()

            logger.warning('simple_generative_ai.moderate.open-ai: %s -- %s -- %s', request, moderator, results)

            moderation = results.get('results', [])[0]

            flagged = moderation.get('flagged', None)

            if flagged is not None:
                decision = ModerationDecision(request=request, when=timezone.now())

                decision.approved = flagged is False

                decision.decision_maker = moderator.moderator_id

                decision.metadata = json.dumps(results, indent=2)

                decision.save()
    except: # pylint: disable=bare-except
        logger.error('simple_generative_ai.moderate ERROR: %s', traceback.format_exc())

    return (None, None)
