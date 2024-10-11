import os
import shutil
from pathlib import Path
import time
from colorama import init, Fore, Style
import humanize

init(autoreset=True)  # Initialize colorama

def copy_documents_to_usb():
    start_time = time.time()
    usb_path = Path(__file__).parent
    documents_path = Path.home() / "Documents"

    if not documents_path.exists():
        print(f"{Fore.RED}Documents folder not found at {documents_path}")
        return

    backup_folder = usb_path / "Documents_Backup"
    backup_folder.mkdir(exist_ok=True)

    # Count total files and calculate total size
    total_files = sum(1 for _ in documents_path.rglob("*") if _.is_file())
    total_size = sum(_.stat().st_size for _ in documents_path.rglob("*") if _.is_file())

    print(f"{Fore.CYAN}Starting backup of {total_files} files ({humanize.naturalsize(total_size)})")

    copied_files = 0
    copied_size = 0

    for item in documents_path.rglob("*"):
        if item.is_file():
            relative_path = item.relative_to(documents_path)
            destination = backup_folder / relative_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, destination)
            
            copied_files += 1
            file_size = item.stat().st_size
            copied_size += file_size
            
            progress = (copied_size / total_size) * 100
            print(f"\r{Fore.GREEN}[{copied_files}/{total_files}] {progress:.2f}% | "
                  f"Copied: {humanize.naturalsize(copied_size)}/{humanize.naturalsize(total_size)} | "
                  f"{Fore.YELLOW}{item.name}", end="")

    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n\n{Fore.CYAN}Backup complete!")
    print(f"{Fore.CYAN}Total time: {duration:.2f} seconds")
    print(f"{Fore.CYAN}Total files copied: {copied_files}")
    print(f"{Fore.CYAN}Total size copied: {humanize.naturalsize(copied_size)}")

if __name__ == "__main__":
    copy_documents_to_usb()
