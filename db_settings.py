from abstract.abstract_settings import AbstractSettings


class SettingsDb(AbstractSettings):
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str

    def get(self, name: str):
        return self.__dict__.get(name)