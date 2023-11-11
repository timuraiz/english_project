from dotenv import load_dotenv
import os

env_file = f'{os.path.dirname(os.path.abspath(__file__))}/.env'


class EnvLoader:
    def __init__(self):
        self.env_file = env_file

    def load(self):
        if os.path.exists(self.env_file):
            load_dotenv(self.env_file)
            print(f"Environment variables loaded from {self.env_file}")
        else:
            print(f"Warning: {self.env_file} not found. No environment variables loaded.")


class Config:
    def __init__(self):
        env_loader = EnvLoader()
        env_loader.load()

        self.BOT_TOKEN = os.environ.get("BOT_TOKEN")
        self.API_KEY = os.environ.get("API_KEY")


config = Config()
