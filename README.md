# File Processor

File Processor is a Python application that automates the process of unzipping, modifying, and re-zipping files in a specified directory. It provides both a command-line interface and a graphical user interface for ease of use.

## Features

- Unzip all ZIP files in a specified directory
- Find and replace text in files
- Replace entire files
- Re-zip processed directories
- Logging of all operations
- User-friendly GUI

## Requirements

- Python 3.11.4+
- tkinter (usually comes pre-installed with Python)

## Configuration

The application requires three JSON configuration files:

1. `config.json`: Main configuration file
2. `replace_rows.json`: Configuration for text replacement within files
3. `replace_files.json`: Configuration for file replacement

### config.json

This file contains the main configuration for the application. It should be structured as follows:

```json
{
    "root_path": "<path_to_directory_to_process>",
    "line_replacement_config_path": "<path_to_replace_rows.json>",
    "file_replacement_config_path": "<path_to_replace_files.json>"
}
```

### path_to_replace_rows.json

This file contains the logic to what lines to replace with what in all files that can be read as text

```json
{
    "text_to_find1": "text_to_replace_with1",
    "text_to_find2": "text_to_replace_with2"
}
```

### path_to_replace_files.json

This file contains the logic to what files to replace with what, in all directories. Please make sure to only work with copies of files to avoid any mishaps

```json
{
    "file_to_replace1": "path_to_replacement_file1",
    "file_to_replace2": "path_to_replacement_file2"
}
```

## Note:

The application can be easily compiled into an executable. Just run `compile.bat`.