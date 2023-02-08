from abstract.abstract_parser import AbstractParser
from abstract.db_operations import DbOperations
from abstract.runnable import Runnable


class ProgramFlowController(Runnable):
    def __init__(self, parser: AbstractParser, ops: DbOperations):
        self.ops = ops
        self.parser = parser

    def run(self):
        entity_list = self.parser.parse()
        self.ops.recreate()
#        self.ops.clear()
        self.ops.add_many(entity_list)

        self.ops.add_totals()

#        totals check sql query
#        select id, company, cat_date, is_fact_or_forecast, value, cat_name
#        from parsed
#        order by is_fact_or_forecast, id, company, cat_date, cat_name;
