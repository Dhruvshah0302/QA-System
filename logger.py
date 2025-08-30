import logging
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}".log

# Create the folder/file in current working directory with filename == logs
log_path = os.path.join(os.getcwd(), "logs")

# Create Directory
os.makedirs(log_path, exist_ok= True)

             # Join Folder + Filename
LOG_FILEPATH = os .path.join(log_path, LOG_FILE)

# Feeding the logs in the file 
logging.basicConfig(level=logging.INFO,  # level --> Error / Warning / Information / Debugging ......................
                    filename=LOG_FILEPATH,
                    format = "[%(asctime)s]%(lineno)d %(name)s - %(levelname)s - %(message)s")