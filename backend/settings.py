from pydantic_settings import BaseSettings, SettingsConfigDict

class DBSettings(BaseSettings):
    db_username: str
    db_password: str
    db_name: str
    db_port: int
    db_host: str
    # set extra='ignore' to ignore extra unknown env variables
    model_config = SettingsConfigDict(env_file='.env',
                                      env_file_encoding='utf-8',
                                      extra='ignore')

    @property
    def database_url(self) -> str:
        return f"mysql+pymysql://{self.db_username}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


settings = DBSettings()
print(f"Data base URL from Settings.py: {settings.database_url}")
