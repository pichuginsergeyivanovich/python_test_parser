from abstract.abstract_settings import AbstractSettings


class SettingsExcel(AbstractSettings):
    filename: str
    leafs_level_row: int
    data_offset_row: int

    def get(self, name: str):
        return self.__dict__.get(name)
