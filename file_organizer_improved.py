import os
import shutil
from pathlib import Path
import logging
from time import sleep
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Gets the Path to the Downloads folder
downloads_path = Path.home() / "Downloads"

# Define destination folders (using Path for cross-platform compatibility)
base_organizer_path = Path.home() / "FileOrganizer"
img_folder = base_organizer_path / "images"
document_folder = base_organizer_path / "documents"
video_folder = base_organizer_path / "videos"
audio_folder = base_organizer_path / "audio"
installer_folder = base_organizer_path / "installers"
other_folder = base_organizer_path / "other"

# Create folders if they don't exist
def create_folders():
    folders = [img_folder, document_folder, video_folder, audio_folder, installer_folder, other_folder]
    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created/verified folder: {folder}")

# Dictionary to map extensions to folders
extension_map = {
    'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp'],
    'documents': ['.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx', '.ppt', '.pptx', '.rtf', '.odt'],
    'videos': ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm', '.m4v'],
    'audio': ['.mp3', '.wav', '.aac', '.flac', '.ogg', '.wma', '.m4a'],
    'installers': ['.exe', '.msi', '.dmg', '.pkg', '.deb', '.rpm', '.appimage']
}

def get_destination_folder(file_extension):
    """Return the appropriate destination folder based on file extension"""
    file_ext = file_extension.lower()
    if file_ext in extension_map['images']:
        return img_folder
    elif file_ext in extension_map['documents']:
        return document_folder
    elif file_ext in extension_map['videos']:
        return video_folder
    elif file_ext in extension_map['audio']:
        return audio_folder
    elif file_ext in extension_map['installers']:
        return installer_folder
    else:
        return other_folder

def is_file_ready(file_path, max_wait_time=30):
    """Check if file is completely downloaded/ready to move"""
    file_path = Path(file_path)
    if not file_path.exists():
        return False
    
    # Wait for file to be stable (not changing in size)
    initial_size = -1
    wait_time = 0
    
    while wait_time < max_wait_time:
        try:
            current_size = file_path.stat().st_size
            if current_size == initial_size and current_size > 0:
                return True
            initial_size = current_size
            sleep(1)
            wait_time += 1
        except (OSError, FileNotFoundError):
            sleep(1)
            wait_time += 1
    
    return False

def move_file(file_path, dest_folder):
    """Move file to destination folder with error handling"""
    try:
        file_path = Path(file_path)
        dest_folder = Path(dest_folder)
        
        # Check if file is ready to move
        if not is_file_ready(file_path):
            logger.warning(f"File {file_path.name} may not be ready to move")
            return False
        
        dest_file = dest_folder / file_path.name
        
        # Handle duplicate names
        counter = 1
        while dest_file.exists():
            name_parts = file_path.stem, counter, file_path.suffix
            dest_file = dest_folder / f"{name_parts[0]}_{name_parts[1]}{name_parts[2]}"
            counter += 1
        
        shutil.move(str(file_path), str(dest_file))
        logger.info(f'Moved: {file_path.name} to {dest_folder}')
        return True
        
    except Exception as e:
        logger.error(f'Error moving {file_path}: {e}')
        return False

def move_back(file_path, downloads_path):
    """Move file back to Downloads folder"""
    try:
        file_path = Path(file_path)
        downloads_path = Path(downloads_path)
        
        dest_file = downloads_path / file_path.name
        
        # Handle duplicate names
        counter = 1
        while dest_file.exists():
            name_parts = file_path.stem, counter, file_path.suffix
            dest_file = downloads_path / f"{name_parts[0]}_{name_parts[1]}{name_parts[2]}"
            counter += 1
            
        shutil.move(str(file_path), str(dest_file))
        logger.info(f'Moved back: {file_path.name} to Downloads')
        return True
        
    except Exception as e:
        logger.error(f'Error moving back {file_path}: {e}')
        return False

def move_all_back():
    """Move all files back to the Downloads folder"""
    folders = [img_folder, document_folder, video_folder, audio_folder, installer_folder, other_folder]
    
    for folder in folders:
        if folder.exists():
            for item in folder.iterdir():
                if item.is_file():
                    move_back(item, downloads_path)

def organize_existing_files():
    """Organize files that are already in the Downloads folder"""
    logger.info("Organizing existing files in Downloads folder...")
    
    if not downloads_path.exists():
        logger.error(f"Downloads folder not found: {downloads_path}")
        return
    
    for item in downloads_path.iterdir():
        if item.is_file():
            ext = item.suffix.lower()
            dest_folder = get_destination_folder(ext)
            move_file(item, dest_folder)
        elif item.is_dir():
            logger.info(f'Skipping directory: {item.name}')

class FileOrganizerEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            file_path = Path(event.src_path)
            logger.info(f"New file detected: {file_path.name}")
            
            # Wait a bit for the file to be completely written
            sleep(2)
            
            if file_path.exists():
                ext = file_path.suffix.lower()
                dest_folder = get_destination_folder(ext)
                move_file(file_path, dest_folder)

def main():
    """Main function to run the file organizer"""
    logger.info("Starting File Organizer...")
    
    # Create necessary folders
    create_folders()
    
    # Ask user what they want to do
    print("\nFile Organizer Options:")
    print("1. Organize existing files and start monitoring")
    print("2. Only start monitoring (don't organize existing files)")
    print("3. Move all organized files back to Downloads")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == '1':
        organize_existing_files()
        start_monitoring()
    elif choice == '2':
        start_monitoring()
    elif choice == '3':
        move_all_back()
        print("All files moved back to Downloads folder.")
    elif choice == '4':
        print("Exiting...")
        return
    else:
        print("Invalid choice. Exiting...")

def start_monitoring():
    """Start monitoring the Downloads folder"""
    logger.info(f"Starting to monitor: {downloads_path}")
    
    event_handler = FileOrganizerEventHandler()
    observer = Observer()
    observer.schedule(event_handler, str(downloads_path), recursive=False)
    observer.start()
    
    print(f"\nMonitoring {downloads_path} for new files...")
    print("Press Ctrl+C to stop monitoring")
    
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        logger.info("Stopping file organizer...")
        observer.stop()
    
    observer.join()
    logger.info("File organizer stopped.")

if __name__ == "__main__":
    main()