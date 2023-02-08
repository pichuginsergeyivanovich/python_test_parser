from implementation.db_connection import DBConnection
from implementation.providers.excel_metadata_provider import ExcelMetadataProvider
from implementation.excel_file_reader import ExcelFileReader
from implementation.entity_parser import EntityParser
from implementation.parsed_repository_operations import ParsedRepositoryOperations
from implementation.program_flow_controller import ProgramFlowController
from implementation.providers.db_settings_from_code_provider import SettingsDbFromCodeProvider
from implementation.providers.excel_settings_from_code_provider import ExcelSettingsFromCodeProvider

settings = {
    "DB_HOST": 'host.docker.internal',
    "DB_PORT": 49153,
    "DB_NAME": "postgres",
    "DB_USER": "postgres",
    "DB_PASSWORD": "postgrespw",
    "FILE_TO_IMPORT": r"C:\Users\pichugin\Downloads\Приложение_к_заданию_бек_разработчика.xlsx",
    "leafs_level_row": 2,
    "data_offset_row": 3,
}

if __name__ == '__main__':

    ProgramFlowController(
        EntityParser(
            ExcelMetadataProvider(
                ExcelFileReader(),
                ExcelSettingsFromCodeProvider(settings)
            )),
        ParsedRepositoryOperations(
            DBConnection(SettingsDbFromCodeProvider(settings)),
            "parsed"
        )
    ).run()

