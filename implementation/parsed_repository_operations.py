from abstract.db_connection_operations import DBConnectionOperations
from abstract.db_operations import DbOperations
from abstract.table_named_repository import TableNamedRepository
from parsed_entity import Parsed


class ParsedRepositoryOperations(TableNamedRepository, DbOperations):
    def __init__(self, db: DBConnectionOperations, table: str):
        self.db = db
        self.table = table

    def get_table_name(self) -> str:
        return self.table

    def recreate(self):
        sql: str = f'DROP TABLE IF EXISTS public.{self.get_table_name()};' \
                   f'CREATE TABLE IF NOT EXISTS public.{self.get_table_name()}' \
                   '(' \
                   'cat_name text COLLATE pg_catalog."default",' \
                   'company text COLLATE pg_catalog."default",' \
                   'is_fact_or_forecast boolean NOT NULL DEFAULT false,' \
                   'value integer,' \
                   'cat_date text COLLATE pg_catalog."default",' \
                   'rec_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),' \
                   'id integer NOT NULL' \
                   ')' \
                   'TABLESPACE pg_default;' \
                   f'ALTER TABLE IF EXISTS public.{self.get_table_name()} ' \
                   'OWNER to postgres;'
        return self.db.exec(sql)

    def get_all(self):
        return self.db.fetch_one(f"SELECT * from {self.get_table_name()}")

    def get_one(self, e: Parsed):
        return self.db.fetch_one(
            f"SELECT * from {self.get_table_name()} where id={e.id} and company=''{e.company}'' limit 1")

    def clear(self):
        return self.db.exec(f"truncate table {self.get_table_name()}")

    def add_one(self, e: Parsed):
        sql = f"insert into {self.get_table_name()}(id, company, value, cat_name, cat_date, is_fact_or_forecast)" \
              f"values({e.id}, '{e.company}', {e.value}, '{e.cat_name}', '{e.cat_date}', " \
              f"{False if not e.is_fact_or_forecast else True})"
        self.db.exec(sql)

    def add_many(self, elist: list[Parsed]):
        sql = ""
        for e in elist:
            sql += f"insert into {self.get_table_name()}(id, company, value, cat_name, cat_date, is_fact_or_forecast)" \
                   f"values({e.id}, '{e.company}', {e.value}, '{e.cat_name}', '{e.cat_date}', " \
                   f"{False if not e.is_fact_or_forecast else True});\n"
        self.db.exec(sql)

    def add_totals(self):
        sql = f"delete from {self.get_table_name()} where cat_name='Total';" \
              f"insert into {self.get_table_name()}(id, company, cat_date, is_fact_or_forecast, value, cat_name)" \
              f"SELECT id, company, cat_date,is_fact_or_forecast, sum(value) as value, 'Total' as cat_name " \
              f"FROM public.{self.get_table_name()} " \
              f"group by id, company, cat_date,is_fact_or_forecast"
        self.db.exec(sql)
