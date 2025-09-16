import os 
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s]: %(message)s:"
)
project_name = "networkSecurity"

list_of_dir_and_file = [
    ".github/workflows/main.yaml",
    ".gitignore",
    "README.md",
    "requirements.txt",
    f"{project_name}/__init__.py",
    f"{project_name}/component/__init__.py",
    f"{project_name}/entity/__init__.py",
    f"{project_name}/constant/__init__.py",
    f"{project_name}/logging/__init__.py",
    f"{project_name}/exception/__init__.py",
    f"{project_name}/pipeline/__init__.py",
    f"{project_name}/utils/__init__.py",
    f"{project_name}/cloud/__init__.py",
    "Dockerfile",       # ✅ file at project root
    "setup.py",         # ✅ file at project root
    ".env"
]

for filepath in list_of_dir_and_file:
    new_filepath = Path(filepath)
    filedir,filename = os.path.split(new_filepath)


    if filedir != "" and filedir[-1] == "/":
        os.makedirs(filedir,exist_ok=True)
        logging.info(f"Creating directory {filedir} for file {filename}")

    if (not os.path.exists(new_filepath)) or (os.path.exists(new_filepath) == 0):
        with open(new_filepath,"w") as f:
            pass
            logging.info(f"Creating empty file {new_filepath}")

    else:
        logging.info(f"{new_filepath} already exist")


