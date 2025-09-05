# File Organizer

A Python script that automatically organizes files in your Downloads folder by moving them into categorized folders based on their file extensions.

## Features

- **Automatic File Organization**: Sorts files into predefined categories (images, documents, videos, audio, installers, other)
- **Real-time Monitoring**: Watches the Downloads folder and automatically organizes new files as they arrive
- **Smart File Handling**: Waits for files to finish downloading before moving them
- **Duplicate Management**: Automatically renames files if duplicates exist in destination folders
- **Flexible Operation**: Choose to organize existing files, monitor only, or restore files back to Downloads
- **Cross-platform Compatibility**: Works on Windows, macOS, and Linux
- **Comprehensive Logging**: Detailed logging of all file operations

## Requirements

- Python 3.6 or higher
- `watchdog` library for file system monitoring

## Installation

1. Clone or download this script to your computer
2. Install the required dependency:
```bash
pip install watchdog
```

## File Categories

The script organizes files into the following categories:

- **Images**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`, `.svg`, `.webp`
- **Documents**: `.pdf`, `.doc`, `.docx`, `.txt`, `.xls`, `.xlsx`, `.ppt`, `.pptx`, `.rtf`, `.odt`
- **Videos**: `.mp4`, `.avi`, `.mov`, `.mkv`, `.flv`, `.wmv`, `.webm`, `.m4v`
- **Audio**: `.mp3`, `.wav`, `.aac`, `.flac`, `.ogg`, `.wma`, `.m4a`
- **Installers**: `.exe`, `.msi`, `.dmg`, `.pkg`, `.deb`, `.rpm`, `.appimage`
- **Other**: Any file type not listed above

## Folder Structure

The script creates the following folder structure in your home directory:

```
~/FileOrganizer/
├── images/
├── documents/
├── videos/
├── audio/
├── installers/
└── other/
```

## Usage

Run the script:
```bash
python file_organizer.py
```

You'll be presented with four options:

1. **Organize existing files and start monitoring**: Moves all current files from Downloads to appropriate folders, then starts monitoring for new files
2. **Only start monitoring**: Starts monitoring without touching existing files
3. **Move all organized files back to Downloads**: Restores all previously organized files back to the Downloads folder
4. **Exit**: Quits the program

### Monitoring Mode

When monitoring is active:
- The script will automatically detect new files in your Downloads folder
- Files are moved to appropriate categorized folders based on their extensions
- Press `Ctrl+C` to stop monitoring

## How It Works

1. **File Detection**: Uses the `watchdog` library to monitor the Downloads folder for new files
2. **File Readiness Check**: Waits for files to finish downloading by monitoring file size stability
3. **Categorization**: Determines the appropriate folder based on file extension
4. **Safe Moving**: Moves files with error handling and duplicate name resolution
5. **Logging**: Records all operations for debugging and tracking

## Safety Features

- **File Readiness Verification**: Ensures files are completely downloaded before moving
- **Duplicate Handling**: Automatically renames files if a file with the same name already exists
- **Error Handling**: Comprehensive error handling with detailed logging
- **Restore Function**: Ability to move all files back to Downloads if needed

## Customization

You can easily customize the script by:

1. **Adding New File Types**: Modify the `extension_map` dictionary to include new file extensions
2. **Creating New Categories**: Add new folders and update the extension mapping
3. **Changing Destination Path**: Modify `base_organizer_path` to change where organized files are stored
4. **Adjusting Wait Times**: Modify the `max_wait_time` parameter in `is_file_ready()` function

Example of adding a new category:
```python
# Add to folder creation
archive_folder = base_organizer_path / "archives"

# Add to extension_map
extension_map['archives'] = ['.zip', '.rar', '.7z', '.tar', '.gz']

# Update get_destination_folder function
elif file_ext in extension_map['archives']:
    return archive_folder
```

## Logging

The script provides detailed logging information including:
- File detection and movement operations
- Error messages and warnings
- Folder creation confirmations
- Start/stop monitoring status

Log messages are displayed in the console with timestamps and severity levels.

## Troubleshooting

**Script doesn't detect new files**: 
- Ensure the Downloads folder path is correct for your system
- Check that you have read/write permissions for both Downloads and FileOrganizer folders

**Files aren't moving**: 
- The script waits for files to finish downloading - be patient with large files
- Check the console for error messages
- Ensure destination folders have write permissions

**Want to stop monitoring**: 
- Press `Ctrl+C` in the terminal to stop the monitoring process

## License

This script is provided as-is for personal use. Feel free to modify and distribute according to your needs.

## Contributing

If you find bugs or want to suggest improvements, feel free to modify the script for your specific needs.
