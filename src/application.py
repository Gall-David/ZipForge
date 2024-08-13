from src.file_processor import FileProcessor

class Application:
    @staticmethod
    def run(config_path: str) -> None:
        """
        Wrapper function to run the application
        Parameters:
            config_path: str: The path to the main configuration file
        Returns:
            None
        """
        try:
            processor = FileProcessor(config_path)
            processor.process_directory()
            print("Processing completed successfully. Check the log file for details.")
        except Exception as e:
            print(f"An error occurred: {str(e)}. Check the log file for details.")