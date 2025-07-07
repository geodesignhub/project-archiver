import os
import zipfile
import logging
OUTPUT_DIR = "output"  # Change this if your output directory is different

@dataclass
class ProjectDetails:
    

class ScriptLogger:
    def __init__(self):
        self.log_file_name = "logs/latest.log"
        self.path = os.getcwd()
        self.logpath = os.path.join(self.path, "logs")
        self.outputpath = os.path.join(self.path, "output")
        if not os.path.exists(self.logpath):
            os.mkdir(self.logpath)
        if not os.path.exists(self.outputpath):
            os.mkdir(self.outputpath)
        self.logging_level = logging.INFO
        # set TimedRotatingFileHandler for root
        self.formatter = logging.Formatter(
            "%(asctime)s %(name)s %(levelname)s %(message)s"
        )
        # use very short interval for this example, typical 'when' would be 'midnight' and no explicit interval
        self.handler = logging.handlers.TimedRotatingFileHandler(
            self.log_file_name, when="S", interval=30, backupCount=10
        )
        self.handler.setFormatter(self.formatter)
        self.logger = logging.getLogger()  # or pass string to give it a name
        self.logger.addHandler(self.handler)
        self.logger.setLevel(self.logging_level)

    def get_logger(self):
        return self.logger

def find_zip_files(directory):
    return [f for f in os.listdir(directory) if f.endswith('.zip')]

def unzip_file(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
        return zip_ref.namelist()

def verify_contents(extract_to, expected_files=None):
    actual_files = []
    for root, _, files in os.walk(extract_to):
        for file in files:
            rel_path = os.path.relpath(os.path.join(root, file), extract_to)
            actual_files.append(rel_path)
    if expected_files is not None:
        missing = set(expected_files) - set(actual_files)
        extra = set(actual_files) - set(expected_files)
        return missing, extra
    return actual_files

def main():
    myLogger = ScriptLogger()
    logger = myLogger.get_logger()
    zip_files = find_zip_files(OUTPUT_DIR)
    if not zip_files:
        print("No zip files found in output directory.")
        return

    for zip_file in zip_files:
        zip_path = os.path.join(OUTPUT_DIR, zip_file)
        extract_dir = os.path.join(OUTPUT_DIR, f"unzipped_{os.path.splitext(zip_file)[0]}")
        os.makedirs(extract_dir, exist_ok=True)
        logger.info(f"Unzipping {zip_file} to {extract_dir}...")
        contents = unzip_file(zip_path, extract_dir)
        logger.info("Contents in zip:", contents)
        actual_files = verify_contents(extract_dir)
        logger.info("Extracted files:", actual_files)
        # Check for expected CSV files
        expected_files = [
            "design_syntheses.csv",
            "design_teams.csv",
            "diagrams.csv",
            "project.csv",
            "systems.csv"
        ]
        missing, extra = verify_contents(extract_dir, expected_files)
        logger.info("Missing:", missing, "Extra:", extra)
        if missing:
            logger.error(f"Missing expected files: {missing}")
            sys.exit(1)
        if extra:
            logger.warning(f"Extra files found: {extra}")
            sys.exit(1)
    
    
    # Process each file starting with 'project.csv'
    for file in actual_files:
        if file.startswith("project.csv"):
            project_csv_path = os.path.join(extract_dir, file)
            logger.info(f"Processing file: {project_csv_path}")
            with open(project_csv_path, 'r') as f:


        

if __name__ == "__main__":
    main()