import json
import logging
import os
import shutil
from typing import Dict
import zipfile


class FileProcessor:
    def __init__(self, config_path: str) -> None:
        """
        Constructor of the FileProcessor class
        Parameters:
            config_path: str: The path to the main JSON configuration file
        Returns:
            None
        """
        self.config = self.load_config(config_path)
        self.root_path = self.config['root_path']
        self.replacements = self.load_config(self.config['line_replacement_config_path'])
        self.file_replacements = self.load_config(self.config['file_replacement_config_path'])
        self.extracted_dirs = set()  # Store the directories extracted from zip files
        self.stop_processor = False

        # Set up logging
        logging.basicConfig(filename='file_processor.log', level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def load_config(self, config_path: str) -> Dict[str, str]:
        """
        Load a JSON configuration file
        Parameters:
            config_path: str: The path to the JSON configuration file
        Returns:
            Dict[str, str]: A dictionary containing the configuration data
        """
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logging.error(f"Configuration file not found: {config_path}")
            raise
        except json.JSONDecodeError:
            logging.error(f"Invalid JSON in configuration file: {config_path}")
            raise

    def process_directory(self) -> None:
        """
        Process the root directory
        Parameters:
            None
        Returns:
            None
        """
        if self.stop_processor is False:
            try:
                self.unzip_all()
                self.find_and_replace()
                self.replace_files()
                self.zip_extracted()
                logging.info("Directory processing completed successfully.")
            except Exception as e:
                logging.error(f"An error occurred while processing the directory: {str(e)}")
                raise

    def unzip_all(self) -> None:
        """
        Unzip all zip files in the root directory
        Parameters:
            None
        Returns:
            None
        """
        for root, _, files in os.walk(self.root_path):
            for file in files:
                if file.endswith('.zip'):
                    zip_path = os.path.join(root, file)
                    extract_path = os.path.splitext(zip_path)[0]
                    try:
                        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                            zip_ref.extractall(extract_path)
                        os.remove(zip_path)
                        self.extracted_dirs.add(extract_path)
                        logging.info(f"Unzipped and removed: {zip_path}")
                        print(f"Unzipped {zip_path}")
                    except zipfile.BadZipFile:
                        logging.error(f"Bad zip file: {zip_path}")
                    except PermissionError:
                        logging.error(f"Permission denied when trying to remove: {zip_path}")

    def find_and_replace(self) -> None:
        """
        Find and replace text in all files in the root directory
        Parameters:
            None
        Returns:
            None
        """
        for root, _, files in os.walk(self.root_path):
            for file in files:
                file_path = os.path.join(root, file)
                self.process_file(file_path)

    def process_file(self, file_path: str) -> None:
        """
        Process a file by replacing text
        Parameters:
            file_path: str: The path to the file
        Returns:
            None
        """
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            for old_line, new_line in self.replacements.items():
                content = content.replace(old_line, new_line)
            with open(file_path, 'w') as f:
                f.write(content)
            logging.info(f"Processed file: {file_path}")
        except IOError as e:
                logging.error(f"Error processing file {file_path}: {str(e)}")
        except (PermissionError, UnicodeDecodeError):
            pass

    def replace_files(self) -> None:
        """
        Replace files in the root directory
        Parameters:
            None
        Returns:
            None
        """
        for root, _, files in os.walk(self.root_path):
            for file in files:
                if file in self.file_replacements:
                    old_file_path = os.path.join(root, file)
                    replacement_file_path = self.file_replacements[file]
                    try:
                        # Create a copy of the replacement file
                        replacement_file_copy = os.path.join(root, f"temp_{file}")
                        shutil.copy2(replacement_file_path, replacement_file_copy)
                        # Replace the old file with the copy
                        os.remove(old_file_path)
                        os.rename(replacement_file_copy, old_file_path)
                        logging.info(f"Replaced file: {old_file_path}")
                        print(f"Replaced file {old_file_path} with {replacement_file_path}")
                    except IOError as e:
                        logging.error(f"Error replacing file {old_file_path}: {str(e)}")

    def zip_extracted(self) -> None:
        """
        Zip all extracted directories
        Parameters:
            None
        Returns:
            None
        """
        for dir_path in self.extracted_dirs:
            zip_path = dir_path + '.zip'
            try:
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root, _, files in os.walk(dir_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, dir_path)
                            zipf.write(file_path, arcname)
                shutil.rmtree(dir_path)
                logging.info(f"Created zip file: {zip_path}")
                print(f"Created zip file {zip_path}")
            except IOError as e:
                logging.error(f"Error creating zip file {zip_path}: {str(e)}")