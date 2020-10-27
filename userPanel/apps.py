from django.apps import AppConfig


class UserpanelConfig(AppConfig):
    name = 'userPanel'

    def ready(self):
        from . import scraper
        scraper.start()
