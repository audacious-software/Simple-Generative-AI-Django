# pylint: disable=line-too-long, no-member

import csv
import io
import os
import tempfile
import zipfile

import pytz
import zipstream

from django.conf import settings
from django.db.models import Q

from .models import GenerativeAIModel

def export_data_sources(params=None):  # pylint: disable=unused-argument
    data_sources = []

    for model in GenerativeAIModel.objects.all().order_by('model_name'):
        data_sources.append((model.model_id, model.model_name, 'Simple Generative AI',))

    return data_sources

def export_data_types():
    return [
        ('simple_generative_ai.request_logs', 'Generative AI Request Logs',),
    ]

def compile_data_export(data_type, data_sources, start_time=None, end_time=None, custom_parameters=None): # pylint: disable=unused-argument, too-many-locals
    here_tz = pytz.timezone(settings.TIME_ZONE)

    if data_type == 'simple_generative_ai.request_logs':
        sources_suffix = data_sources[0]

        if data_sources[-1] != data_sources[0]:
            sources_suffix = '%s_%s' % (sources_suffix, data_sources[-1])

        base_filename = 'simple_generative_ai.request_logs__%s.zip' % sources_suffix

        filename = '%s%s%s' % (tempfile.gettempdir(), os.path.sep, base_filename)

        with io.open(filename, 'wb') as final_output_file:
            with zipstream.ZipFile(mode='w', compression=zipfile.ZIP_DEFLATED, allowZip64=True) as export_stream: # pylint: disable=line-too-long
                for source in data_sources:
                    print('source: %s' % source)

                    model = GenerativeAIModel.objects.filter(model_id=source).first()

                    if model is None:
                        continue

                    with io.StringIO() as outfile:
                        writer = csv.writer(outfile, delimiter='\t')

                        writer.writerow([
                            'Model Identifier',
                            'Model Name',
                            'Model Type',
                            'Request Timestamp',
                            'Successful',
                            'Request Body',
                            'Response Body',
                        ])

                        query = Q(pk__gte=0)

                        if start_time is not None:
                            query = query & Q(requested__gte=start_time)

                        if end_time is not None:
                            query = query & Q(requested__lte=end_time)

                        for request in model.requests.filter(query).order_by('requested'):
                            writer.writerow([
                                request.model.model_id,
                                request.model.model_name,
                                request.model.model_type,
                                request.requested.astimezone(here_tz).isoformat(),
                                request.successful,
                                request.request,
                                request.response,
                            ])

                        source_filename = 'simple_generative_ai_request_logs/%s.txt' % source

                        export_stream.writestr(source_filename, outfile.getvalue().encode('utf-8'))

                for data in export_stream:
                    final_output_file.write(data)

        return filename

    return None
