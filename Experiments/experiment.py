# test_env.py
from pathlib import Path
from dotenv import load_dotenv
import os

# Load .env
env_path = Path('.env')
print(f"Looking for .env at: {env_path.absolute()}")
print(f"File exists: {env_path.exists()}")

load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    print(f"✅ API Key found: {api_key[:10]}...{api_key[-4:]}")
else:
    print("❌ API Key not found")