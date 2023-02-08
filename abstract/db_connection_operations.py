class DBConnectionOperations(object):

    def begin_exec(self, settings: any) -> object:
        pass

    def end_exec(self, conn):
        pass

    def exec(self, sql: str):
        pass

    def fetch_one(self, sql: str):
        pass

    def fetch_all(self, sql: str):
        pass

