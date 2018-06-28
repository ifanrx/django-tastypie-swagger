#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import os
import shutil

from django.conf import settings
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string

import tastypie_swagger


class Command(BaseCommand):
    help = 'Collect swagger-ui static file and compile index.html.'
    dest_dir = getattr(settings, 'TASTYPIE_SWAGGER_DOCS_DIR')
    swagger_static_dir = os.path.join(tastypie_swagger.__path__[0], 'static')

    def _compile_index(self):
        self.stdout.write('Compiling index.html, please wait patiently.')
        context = {
            'index_title': getattr(settings, 'TASTYPIE_SWAGGER_INDEX_TITLE',
                              'Swagger UI'),
            'STATIC_URL': './',
            'json_spec': json.dumps(
                tastypie_swagger.mapping.build_openapi_spec()),
        }
        return render_to_string('tastypie_swagger/index.html', context)

    def _copy_index(self):
        index_path = os.path.join(self.dest_dir, 'index.html')
        self.stdout.write('Copy index.html to {}.'.format(index_path))
        with open(index_path, 'w') as f:
            f.write(self._compile_index())

    def _copy_static_file(self):
        ignore_pattern_list = getattr(settings,
                                      'TASTYPIE_SWAGGER_IGNORE_PATTERN_LIST',
                                      None)
        if ignore_pattern_list:
            ignore_pattern = shutil.ignore_patterns(*ignore_pattern_list)
        else:
            ignore_pattern = None
        self.stdout.write('Copy static files to {}.'.format(self.dest_dir))
        shutil.copytree(self.swagger_static_dir, self.dest_dir,
                        ignore=ignore_pattern)

    def _remove_outdated_docs(self):
        if os.path.exists(self.dest_dir):
            self.stdout.write(
                'Remove outdated api docs:{}.'.format(self.dest_dir))
            shutil.rmtree(self.dest_dir)

    def handle(self, *args, **options):
        self._remove_outdated_docs()
        self._copy_static_file()
        self._copy_index()
        self.stdout.write('Done!')
