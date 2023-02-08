from xlrd.sheet import Sheet

from abstract.abstract_settings import AbstractSettings
from abstract.excel_reader import ExcelReader
from abstract.metadata_provider import MetadataProvider
from abstract.settings_provider import SettingsProvider


class ExcelMetadataProvider(MetadataProvider):
    excel_reader: ExcelReader
    settings_provider: SettingsProvider
    settings: AbstractSettings

    def __init__(self, reader: ExcelReader, settings_provider: SettingsProvider):
        self.excel_reader = reader
        self.settings = settings_provider.get_settings()

    @staticmethod
    def get_cell_text(sh: Sheet, row, col):
        res = {"text": ""}
        for mc in sh.merged_cells:
            if mc[0] <= row < mc[1] and mc[2] <= col < mc[3]:
                res["text"] = sh.row(mc[0])[mc[2]].value
                res.update({"row": mc[0], "col": mc[2]})
                break
        return res

    @staticmethod
    def get_col_name(sh: Sheet, col, leafs_level_row) -> dict:
        result = {}
        col_name = ""
        for header_row in range(0, leafs_level_row, 1):
            ct = ExcelMetadataProvider.get_cell_text(sh, header_row, col)
            if ct:
                result.update({f'level_{header_row}_value': ct})
                col_name += f"{ct}."
        result.update({f'direct_value': sh.row(leafs_level_row)[col].value})
        return result

    def read_metadata(self):
        sh: Sheet = self.excel_reader.get_excel_sheet(self.settings.get('filename'))
        obj_info = {"rows": []}
        for row in range(self.settings.get('data_offset_row'), sh.nrows):
            row_tags = {"columns": []}
            for col in range(0, sh.ncols):
                column_tags = {}
                column_tags.update(ExcelMetadataProvider.get_col_name(sh, col, self.settings.get('leafs_level_row')))
                column_tags.update({"value": sh.row(row)[col], "row": row, "col": col})
                row_tags.get("columns").append(column_tags)
            obj_info.get("rows").append(row_tags)
        return obj_info
