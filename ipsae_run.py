import subprocess
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
IPSAE_SCRIPT = PROJECT_DIR / "ipsae.py"

def run_ipsae(extracted_by_job, pae_cutoff=10, dist_cutoff=10):

    results_by_job = {}

    # Loop through files in job to get _full_data_ named .json files and any cif files
    for job_name, files in extracted_by_job.items():
        json_files = [f for f in files if f.suffix == ".json"]
        full_data_json_files = [f for f in json_files if "_full_data_" in f.name]
        cif_files = [f for f in files if f.suffix == ".cif"]

        chain_score_paths = []
        residue_score_paths = []

        # From DunbrackLab/IPSAE/README - AlphaFold3
        # python ipsae.py fold_aurka_tpx2_full_data_0.json fold_aurka_tpx2_model_0.cif 10 10

        # Alternating .json file to match .cif and find pair
        for json_path in full_data_json_files:
            find_matching_cif = (json_path.name.replace("_full_data_", "_model_").removesuffix(".json") + ".cif")

            matching_cif = next((f for f in cif_files if f.name == find_matching_cif), None)

            if matching_cif is None:
                print(f"No matching .cif found for {json_path.name}")
                continue

            # From DunbrackLab/IPSAE/README - AlphaFold3
            # python ipsae.py <path_to_af3_json_file> <path_to_af3_cif_file> <pae_cutoff> <dist_cutoff>

            try:

                # Command to run ipsae.py, will stop if errors
                running = subprocess.run(["python", str(IPSAE_SCRIPT), str(json_path), str(matching_cif), str(pae_cutoff), str(dist_cutoff)],
                                         check=True, capture_output=True, text=True)
                print(f"Successfully ran IPSAE on " f"{json_path.name} + {matching_cif.name}")

                # New file paths
                chain_score_paths.append(matching_cif.with_name(f"{matching_cif.stem}_{pae_cutoff:02d}_{dist_cutoff:02d}.txt"))
                residue_score_paths.append(matching_cif.with_name(f"{matching_cif.stem}_{pae_cutoff:02d}_{dist_cutoff:02d}_byres.txt"))

            except subprocess.CalledProcessError as e:
                print(f"Command failed with exit code {e.returncode}")
                print(f"Error message: {e.stderr}")

        results_by_job[job_name] = (chain_score_paths, residue_score_paths)

    return results_by_job