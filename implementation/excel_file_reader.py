import xlrd
from xlrd.sheet import Sheet
from abstract.excel_reader import ExcelReader


class ExcelFileReader(ExcelReader):

    @staticmethod
    def get_excel_sheet(filename, index: int = 0) -> Sheet:
        workbook = xlrd.open_workbook(filename)
        return workbook.sheet_by_index(index)
