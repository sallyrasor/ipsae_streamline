# **IPSAE Streamline**

Running AlphaFold3 prediction results through Dunbrack Lab's ipsae.py and compile the output from multiple jobs into a single Excel workbook. 

*This project was specifically built to help a biochemistry research lab to track structure-prediction scores without manual file handling.*

## **What it does**

Given an AlphaFold3 result .zip file, this tool:

- Extracts the .json and .cif files needed from each zip
- Runs ipsae.py on each matching prediction pair
- Compiles every job's chain-pair and residue-level scores into one .xlsx workbook, tagged with the job name they came from

## **Installation**
*Run one line at a time*

**1. Clone the repo:**

git clone https://github.com/sallyrasor/ipsae_streamline.git

cd ipsae_streamline

**2. Create and activate a virtual environment:**

python -m venv .venv

.venv\Scripts\activate      # Windows

source .venv/bin/activate   # Mac/Linux

**3. Install dependencies:**

pip install -r requirements.txt

**4. Run it:**

python main.py

### **You'll be prompted for:**

- The folder containing your AlphaFold3 .zip file(s)
- A folder to extract files into
- The path for the output Excel file

## **Project structure**
| File |	Purpose |
| --- | --- |
| main.py |	Entry point — prompts for folder paths, runs the full pipeline |
| file_finder.py | Extracts .json/.cif files from AlphaFold3 zip(s), grouped by job |
| ipsae_run.py |	Matches each job's .json/.cif pair and runs ipsae.py on it |
| results.py | Reads ipsae.py's output and appends it to the Excel workbook |
| ipsae.py | Dunbrack Lab's scoring script (unmodified — see Credits) |
| DunbrackLab/LICENSE.txt |	MIT license for ipsae.py, from its original source |

## **Credits**

This project relies entirely on ipsae.py by Roland Dunbrack. It's unmodified, under its original MIT license (see DunbrackLab/LICENSE.txt). All credit for ipsae.py belongs to the Dunbrack Lab.

### **Note on data**

AlphaFold prediction zip files and extracted results are not included in this repository, since they're based on real lab research data. The extracted/ folder is excluded via .gitignore and is generated automatically when you run the tool.

### **Future improvements**

Handle duplicate filename collisions. Streamline opening excel workbook, you currently need to open through path each time for it to properly update. Support configurable PAE/distance cutoffs via a prompt, they are currently both defaulted to 10.

## **License**

MIT — see LICENSE for this project's own code. ipsae.py is separately licensed by Dunbrack Lab (see above).
