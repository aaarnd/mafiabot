from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    ## token  
    bot_token : SecretStr
    
    ## настройки. определение файла окружения и его формата
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    
config = Settings()
