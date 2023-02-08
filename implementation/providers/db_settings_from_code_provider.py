from abstract.settings_provider import SettingsProvider
from db_settings import SettingsDb


class SettingsDbFromCodeProvider(SettingsProvider):
    data: dict

    def __init__(self, data: dict):
        self.data = data

    def get_settings(self) -> SettingsDb:
        settings = SettingsDb()
        settings.db_host = self.data.get("DB_HOST")
        settings.db_port = self.data.get("DB_PORT")
        settings.db_name = self.data.get("DB_NAME")
        settings.db_user = self.data.get("DB_USER")
        settings.db_password = self.data.get("DB_PASSWORD")
        return settings
