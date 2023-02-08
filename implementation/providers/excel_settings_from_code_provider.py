from abstract.settings_provider import SettingsProvider
from excel_settings import SettingsExcel


class ExcelSettingsFromCodeProvider(SettingsProvider):
    data: dict

    def __init__(self, data: dict):
        self.data = data

    def get_settings(self) -> SettingsExcel:
        settings = SettingsExcel()
        settings.filename = self.data.get("FILE_TO_IMPORT")
        settings.data_offset_row = self.data.get("data_offset_row")
        settings.leafs_level_row = self.data.get("leafs_level_row")
        return settings
