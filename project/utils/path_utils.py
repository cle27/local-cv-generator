import os, shutil
from pathlib import Path

# Check that file exist and read its content
def file_check_and_read (file_path, isPythonCode=False):
    try:
        with open(file_path, "r") as f:
            if isPythonCode:
                return f.read().strip()
            else :
                return f.read().strip().replace("{", "{{").replace("}", "}}")
    except FileNotFoundError:
        print(f"Error: {file_path} not found!")
        return False
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return False

def check_file(file_path, isImage=False):
    path = Path(file_path)
    # Check if file exists
    if not path.is_file():
        print(f"Error: File '{file_path}' does not exist.")
        return False
    # Check if it's an image file based on extension
    if isImage & (path.suffix.lower() not in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']):
        print(f"Error: File '{file_path}' is not a recognized image format.")
        return False
    else:
        return path

def clean_output (folder_path):
    # Remove all contents of the output folder
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.unlink(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)

def backup_file(original_file_path):
    # Ensure path is valid
    original_file_path = Path(check_file(original_file_path))
    new_file_name = original_file_path.with_suffix(original_file_path.suffix + ".backup")

    # Copy the file to the backup directory
    shutil.copy2(original_file_path, new_file_name)

    return str(new_file_name)

def duplicate_file_for_process(original_file_path, shouldOverride = False, prefix="processed_", output_dir = None):
    # Ensure path is valid
    original_file_path = Path(check_file(original_file_path))
    
    original_name = original_file_path.name
    parent_dir = original_file_path.parent
    
    new_name = f"{prefix}{original_name}"
    if output_dir != None :
        new_file_path = output_dir / new_name
    else:
        new_file_path = parent_dir / new_name
    
    # Copy the file to create the processing file only once
    if (not new_file_path.exists()) | shouldOverride:
        shutil.copy2(original_file_path, new_file_path)

    return str(new_file_path)

def save_content(text_content, output_file):
    with open(output_file, 'w') as f:
        f.write(text_content)
    print(f"Text Saved under:{output_file}")

def generate_prompt_list():
    xp_list = []
    for txt_file in XP_DIR.glob("*.txt"):
        xp_list.append(file_check_and_read(txt_file))

    prompt_list = []
    for xp_txt in xp_list:
        prompt_list.append(prompt_input.format(
            experience_text=xp_txt,                 # Handle context window limits
            language_genp=language_gen,
            job_text=file_check_and_read(html2txt), # Trim if necessary
            json_template=json_template
        ))
    return prompt_list

# Define the base project directory
BASE_DIR = Path(__file__).resolve().parent.parent
MODULES_DIR = BASE_DIR / "modules"

# OUTPUT
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)
clean_output(OUTPUT_DIR)

latex_llm = OUTPUT_DIR / "latex_llm.json"

html2txt = OUTPUT_DIR / "html2txt.txt"

LATEX_OUTPUT_DIR = OUTPUT_DIR / "latex"
LATEX_OUTPUT_DIR.mkdir(exist_ok=True)
clean_output(LATEX_OUTPUT_DIR)

pdfoutput = LATEX_OUTPUT_DIR / "output.pdf"
pdfoutput_noext = LATEX_OUTPUT_DIR / "output"

latex_var = LATEX_OUTPUT_DIR / "latex_var.tex"
orig_latex_module = MODULES_DIR / "altacv.cls"
dest_latex_module = LATEX_OUTPUT_DIR
duplicate_file_for_process(orig_latex_module, True, "", dest_latex_module)

# INPUT
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

XP_DIR = DATA_DIR / "xp"
XP_DIR.mkdir(exist_ok=True)

prompt_input = file_check_and_read(DATA_DIR / "prompt.txt", 1)

json_template = file_check_and_read(DATA_DIR / "json_template.json", True)

photo_cv = check_file(DATA_DIR / "photo_cv.jpg", True)

json_data = duplicate_file_for_process(DATA_DIR / "user_data.json", True)

language_gen = "french"