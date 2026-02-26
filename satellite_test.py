from sentinelhub import SHConfig
import os
from dotenv import load_dotenv

load_dotenv()

config = SHConfig()

config.sh_client_id = os.getenv("SH_CLIENT_ID")
config.sh_client_secret = os.getenv("SH_CLIENT_SECRET")

if config.sh_client_id and config.sh_client_secret:
    print("Sentinel Hub credentials configured successfully!")
else:
    print("Error loading Sentinel credentials.")