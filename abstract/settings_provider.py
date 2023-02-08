from abstract.abstract_settings import AbstractSettings


class SettingsProvider(object):
    def get_settings(self) -> AbstractSettings:
        pass
