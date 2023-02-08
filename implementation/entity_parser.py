from abstract.abstract_parser import AbstractParser
from abstract.metadata_provider import MetadataProvider
from parsed_entity import Parsed


class EntityParser(AbstractParser):

    def __init__(self, meta_provider: MetadataProvider):
        self.meta_provider = meta_provider

    @staticmethod
    def get_column_object(row, name: str):
        if not row:
            raise ValueError("None row object")
        for col in row.get("columns"):
            if col["direct_value"] == name:
                return col
            if col["level_1_value"]["text"] == name:
                return col
            if col["level_0_value"]["text"] == name:
                return col
            if col["value"]:
                return col
            raise ValueError("Error getting column by name")

    @staticmethod
    def parse_id(data: dict):
        if data and data.get("columns"):
            for col in data.get("columns"):
                if col.get("level_0_value") and col.get("level_0_value")["text"] == "id":
                    return col.get("value").value

    @staticmethod
    def parse_company(data: dict):
        if data and data.get("columns"):
            for col in data.get("columns"):
                if col.get("level_0_value") and col.get("level_0_value")["text"] == "company":
                    return col.get("value").value

    @staticmethod
    def parse_value(data: dict):
        if data and data.get("value"):
            return data.get("value").value

    @staticmethod
    def parse_cat_name(data: dict):
        if data and  data.get("level_1_value"):
            return data.get("level_1_value")["text"]

    @staticmethod
    def parse_cat_date(data: dict):
        if data and data.get("direct_value"):
            return data.get("direct_value")

    @staticmethod
    def parse_is_fact_or_forecast(data: dict):
        if data and data.get("level_0_value"):
            if data.get("level_0_value")["text"] == "forecast":
                return True
            elif data.get("level_0_value")["text"] == "fact":
                return False
        raise ValueError("Error parsing value for is_fact_or_forecast")

    def parse(self) -> list[Parsed]:
        info = self.meta_provider.read_metadata()

        res = []
        for row in info.get("rows"):
            row_cols: list = row["columns"]
            obj_id = self.parse_id(row)
            obj_company = self.parse_company(row)

            for col in row_cols:
                print(col)
                entity = Parsed()
                entity.id = obj_id
                entity.company = obj_company
                entity.value = self.parse_value(col)
                entity.cat_date = self.parse_cat_date(col)
                entity.cat_name = self.parse_cat_name(col)
                try:
                    entity.is_fact_or_forecast = self.parse_is_fact_or_forecast(col)
                except ValueError:
                    continue
                res.append(entity)

        return res
