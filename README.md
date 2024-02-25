# Simple Generative AI for Django

This is a Django utility app, suitable for building larger systems, that manages third-party generative AI APIs and services and exposes those features to other Django components (such as [Django Dialog Engine](https://github.com/audacious-software/Django-Dialog-Engine)) in a consistent and controlled manner.

*This is a **early** version of this software and it is still under **active development**. Use at your own risk!*

The package consists of two main model classes: `GenerativeAIModel` and `GenerativeAIModelRequest`. `GenerativeAIModel` is a wrapper object around a third party service that holds the configuration details (such as API key and model type) for use by the service. `GenerativeAIModelRequest` is a log of each request and response between the system and the third-party API service for the purposes of auditing and troubleshooting.

`GenerativeAIModel` objects are configured with a specific model type (e.g. *OpenAI Chat*) which is associated with a model type identifier (e.g. `openai_chat`). When the model is run, it looks in each Django package for a submodule named `.simple_generative_ai.model_type`, where `model_type` is replaced with the model type identifier specified by the object. The module path for the OpenAI Chat model is [`.simple_generative_ai.openai_chat`](simple_generative_ai/openai_chat.py).

This reflection-based approach allows system builders to add new model types and services to a project using Simple Generative AI to provide the management and auditing services. This approach also allows system builders to override the implementations provided with this package, should a more specialized solution be required.

Currently, this package supports the following models and services:

* [OpenAI Text Generation](https://platform.openai.com/docs/guides/text-generation)

The development roadmap includes plans to implement the following models and services:

* [OpenAI Image Generation](https://platform.openai.com/docs/guides/images)
* [Azure OpenAI Services](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
* [PaLM 2 Text](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/text) and [PaLM 2 Chat](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/text-chat)

As new models and services become available, these lists will expand to include new entrants.

## Installing Simple Generative AI for Django

To install Simple Generative AI, clone this repository into your existing Django project:

```
$ git clone https://github.com/audacious-software/Simple-Generative-AI-Django.git simple_generative_ai
```

Add `simple_generative_ai` to `settings.INSTALLED_APPS`. 

Optionally, add Simple Generative AI to your project's `urls.py` file to enable support for for other packages:

```
urlpatterns = [
    path('admin/', admin.site.urls),
    url('^accounts/', include('django.contrib.auth.urls')),
    ...
    url(r'^generative-ai/', include('simple_generative_ai.urls')),
]
```

Each service implementation uses Django's build-in self-inspection system to provide guidance about the next setup steps required to configure a model. Check your progress by running the `check` management command:

```
$ ./manage.py check
System check identified some issues:

WARNINGS:
?: (simple_generative_ai.openai_chat.W001) Model "Chat test (openai_chat)" is not properly configured
	HINT: Add valid "openai_api_key" parameter to model or add "simple_generative_ai.openai_chat.W001" to SILENCED_SYSTEM_CHECKS.
?: (simple_generative_ai.openai_chat.W001) Model "Chat test (openai_chat)" is not properly configured
	HINT: Specify "openai_model" type parameter for model (see https://platform.openai.com/docs/models) or add "simple_generative_ai.openai_chat.W001" to SILENCED_SYSTEM_CHECKS.

System check identified 2 issues (0 silenced).
$ 
```

In this case, you would open the *Chat test* model in the Django administrative interface and update the model parameters:

```
{
"openai_api_key": "YOUR-KEY-HERE",
"openai_model": "gpt-3.5-turbo"
}
```

Re-running the `check` command will indicate that setup is complete:

```
$ ./manage.py check
System check identified no issues (0 silenced).
$
```

For additional information about parameters supported by the service implementation, refer [to the appropriate implementation file](/simple_generative_ai).

## Questions?

If you have any questions or need assistance, please e-mail [chris@audacious-softare.com](mailto:chris@audacious-software.com). This is still a project under active development, so there will still be rough spots as this project develops.

## License and Other Project Information

Copyright 2024 Audacious Software

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
