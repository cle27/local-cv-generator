import json, json2latex
from pathlib import Path
from project.utils.path_utils import json_data, latex_var, pdfoutput_noext, latex_llm, file_check_and_read, save_content

class LatexVarGenerator:
    def __init__(self, json_path: str | Path, latex_var_name: str = 'data'):
        self.json_path = Path(json_path)
        self.latex_var_name = latex_var_name
        self.data = self._load_json()
        
    def _load_json(self) -> dict:
        """Load and validate JSON data"""
        if not self.json_path.exists():
            raise FileNotFoundError(f"JSON file not found: {self.json_path}")
            
        with open(self.json_path, 'r') as f:
            data = json.load(f)
            
        if not isinstance(data, (dict, list)):
            raise ValueError("JSON data must be a dictionary or list")
            
        return data

    def generate_latex_vars(self, output_path: str | Path) -> None:
        """Convert JSON data to LaTeX variables file"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json2latex.dump(self.latex_var_name, self.data, f)
    
    def get_value(self, key_path: str) -> str | list | dict:
        """Get value from JSON data using dot notation"""
        keys = key_path.split('.')
        current_data = self.data
        
        for key in keys:
            if isinstance(current_data, list):
                key = int(key)  # Handle list indices
            current_data = current_data[key]
        
        return current_data

    def get_latex_command(self, key_path: str) -> str:
        """Generate LaTeX access command for nested data"""
        keys = key_path.split('.')
        cmd = f'\\{self.latex_var_name}'
        for key in keys:
            cmd += f'[{key}]'
        return cmd
    
    def modify_json(self, key_path: str, new_value: str | list | dict):
        """Modify nested JSON data using dot notation for keys and list indexes
        
        Example:
        modify_json('personal.name', 'New Name')
        modify_json('experience.0.description.1', 'Updated description text')
        modify_json('hobbies.2', 'Gardening')
        """
        keys = key_path.split('.')
        current_data = self.data
        
        # Traverse the JSON structure
        for i, key in enumerate(keys[:-1]):
            if isinstance(current_data, list):
                key = int(key)  # Convert to index for lists
            current_data = current_data[key]
        
        # Set the final value
        final_key = keys[-1]
        if isinstance(current_data, list):
            final_key = int(final_key)  # Handle list indexes
        current_data[final_key] = new_value

    def save_json(self):
        # Save modified data back to the original JSON file
        with open(self.json_path, 'w') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def modify_and_save_json(self, key_path: str, new_value: str | list | dict):
        # Modify
        self.modify_json(self, key_path, new_value)
        # Save the modified json
        self.save_json()

    def merge_from_source(self, source_json_path: str | Path, index = 0):
        """
        Merge values from source JSON using index-based experience modification
        - source_json_path: JSON file containing override values with indexes
        """
        source_path = Path(source_json_path)
        if not source_path.exists():
            raise FileNotFoundError(f"Source file not found: {source_path}")

        with open(source_path, 'r') as f:
            source_data = json.load(f)

        # Merge skills
        if 'skills' in source_data:
            if index == 0:
                self.data['skills'] = source_data['skills']
            else:
                self.data['skills'] += source_data['skills']

        # Merge experiences by index
        if 'experiences' in source_data:
            for src_exp in source_data['experiences']:
                self.data['experiences'][index]['title'] = src_exp['title']
                self.data['experiences'][index]['description'] = src_exp['description']
                self.data['experiences'][index]['tags'] = src_exp['tags']

        self.save_json()

def escape_latex(text):
    # Replace each special character with its LaTeX-escaped equivalent
    escape_chars = {
        '\\': r'\textbackslash',
        '#': r'\#',
        '$': r'\$',
        '%': r'\%',
        '&': r'\&',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '^': r'\^{}',
        '~': r'\~{}'
    }
    for char, escaped_char in escape_chars.items():
        text = text.replace(char, escaped_char)
    return text

# Example usage in LaTeX generation
if __name__ == "__main__":
    # 1. Initialize with your JSON file
    generator = LatexVarGenerator(json_data, latex_var_name='user')
    generator.merge_from_source(latex_llm)
    print(file_check_and_read(json_data, True))
"""
    # 2. Generate variables.tex
    generator.generate_latex_vars(latex_var)
    
    # 3. Use in PyLaTeX document
    from pylatex import Document, NoEscape
    
    doc = Document()
    doc.append(NoEscape(r'\input{latex_var}'))  # Include generated variables
    
    # Access specific values using dot notation
    hobbies_cmd = generator.get_latex_command('hobbies')
    doc.append(NoEscape(f'Hobbies: {hobbies_cmd}'))
    
    doc.generate_pdf(pdfoutput_noext)
"""