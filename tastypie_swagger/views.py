# _*_ coding:utf-8 _*_
import json

from django.views.generic import TemplateView

from .mapping import build_openapi_spec


class SwaggerView(TemplateView):
    """
    Display the swagger-ui page
    """

    template_name = 'tastypie_swagger/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(SwaggerView, self).get_context_data(*args, **kwargs)
        server_url = self.request.build_absolute_uri('/')
        context.update({
            'json_spec': json.dumps(build_openapi_spec(server_url=server_url)),
        })
        return context
