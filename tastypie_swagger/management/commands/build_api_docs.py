#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import json
import shutil

from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.conf import settings

import tastypie_swagger


class Command(BaseCommand):
    help = 'Collect swagger-ui static file and compile index.html.'

    socialbase_docs_dir = os.path.join(settings.BASE_DIR, 'docs')
    dest_dir = os.path.join(socialbase_docs_dir, 'swagger_api_docs')
    swagger_static_dir = os.path.join(tastypie_swagger.__path__[0], 'static')

    def _compile_index(self):
        self.stdout.write('Compiling index.html, please wait patiently.')
        context = {
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
        ignore_pattern = shutil.ignore_patterns('.DS_Store')
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
