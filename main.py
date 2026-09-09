from pathlib import Path
from file_finder import extract_files
from ipsae_run import run_ipsae
from results import write_results

def get_zip_path():

    # Prompt user for AlphaFold Zip and validate
     while True:
        zip_path = Path(input("Enter the path to the AlphaFold ZIP file: ").strip().strip('"'))

        if zip_path.exists():
            return zip_path

        print(f"{zip_path} doesn't exist")
        retry = input("Try another path? [y/n]: ").strip().lower()

        if retry == "n":
            return None

def main():

    zip_path = get_zip_path()
    if zip_path is None:
        return

    # Did not validate output locations since they can be easily created
    target_dir = Path(input("Enter the folder where the extracted files should be saved: ").strip().strip('"'))
    workbook_path = Path(input("Enter the path for the output Excel file (.xlsx): ").strip().strip('"'))

    # Unzip AlphaFold files, score then with Dunbrack ipsae.py, write the scores to an Excel
    extracted_by_job = extract_files(zip_path, target_dir)
    results_by_job = run_ipsae(extracted_by_job)
    write_results(results_by_job, workbook_path)

    print(f"Done, results written to {workbook_path}")

if __name__ == "__main__":
    main()