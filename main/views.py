from django.views.generic import TemplateView


class MainTemplateView(TemplateView):
    """Контроллер главной страницы."""

    template_name = 'main/index.html'
