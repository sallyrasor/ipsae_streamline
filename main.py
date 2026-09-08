from pathlib import Path
from file_finder import extract_files
from ipsae_run import run_ipsae
from results import write_results

def get_source_dir():
# Prompt user for folder that holds AlphaFold Zip and validate
     while True:
        source_dir = Path(input("Enter the path to the folder that contains your AlphaFold zip files: ").strip().strip('"'))

        if source_dir.exists():
            return source_dir

        print(f"{source_dir} folder doesn't exist")
        retry = input("To choose a new folder type y = retry or type q = quit): ").strip().lower()

        if retry == "q":
            return None

def main():

    source_dir = get_source_dir()
    if source_dir is None:
        return

    # Did not validate output locations since they can be easily created
    target_dir = Path(input("Enter the path to the folder to extract files into: ").strip().strip('"'))
    workbook_path = Path(input("Enter the path for the output Excel file: ").strip().strip('"'))

    # Unzip AlphaFold files, score then with Dunbrack ipsae.py, write the scores to an excel
    extracted_by_job = extract_files(source_dir, target_dir)
    results_by_job = run_ipsae(extracted_by_job)
    write_results(results_by_job, workbook_path)

    print(f"Done, results written to {workbook_path}")

if __name__ == "__main__":
    main()