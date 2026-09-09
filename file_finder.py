import zipfile
from pathlib import Path
import shutil

def extract_files(zip_path, target_dir):

    # If target_dir doesn't exist, creates it along with any missing parent folders
    target_dir.mkdir(parents=True, exist_ok=True)

    # Only extracting these file types from .zip
    FILE_EXTENSION = {".json", ".cif"}
    extracted_by_job = {}

    # Go through each zip, one job corresponds to one zip
    job_name = zip_path.stem
    job_files = extracted_by_job.setdefault(job_name, [])

    try:

        # Open current zip in read mode and loop
        with zipfile.ZipFile(zip_path, 'r') as archive:

            for contents in archive.infolist():

                # If it is a folder in the .zip, skip only looking for files
                if contents.is_dir():
                    continue

                # Making the file name a Path to evaluate its extension and if not .json or .cif, skipping
                content_path = Path(contents.filename)

                if content_path.suffix.lower() not in FILE_EXTENSION:
                    continue

                # New file path to target_dir (ZipFolderName_OriginalFileName)
                destination_path = target_dir / f"{zip_path.stem}_{content_path.name}"

                if destination_path.exists():
                    job_files.append(destination_path)
                    print(f"This file was already extracted, skipping.")
                    continue

                # Copies from source to destination in chunks
                with archive.open(contents) as source, open(destination_path, "wb") as destination:
                    shutil.copyfileobj(source, destination)

                 # Add each path to extracted files array
                job_files.append(destination_path)
                print(f"Extracted {destination_path.name} from {zip_path.name}")

    except zipfile.BadZipFile as e:
        print(e)

    return extracted_by_job