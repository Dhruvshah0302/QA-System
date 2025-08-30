import os 
from pathlib import Path


# _FOLDER_NAME__/ __FILE__NAME__
list_of_files = [
    "QAWithPDF/inint_.py",
    "QAWithPDF/data_injestion.py",
    "QAWithPDF/embedding.py",
    "QAWithPDF/model_api.py",
    "Experiments/experiment.py",
    "StreamlitApp.py",
    "logger.py",
    "exception.py",
    "setup.py"
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir , filename = os.path.split(filepath)
    
    # if the directory(folder) is not present then create it 
    if filedir != "":
        os.makedirs(filedir,exist_ok= True)
    
    # If the folder exists and FILE not present then create the file    
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, 'w') as f:
            pass