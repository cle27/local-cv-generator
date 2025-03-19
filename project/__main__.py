import argparse, time

from project.utils.path_utils import json_data, latex_var, latex_llm, html2txt, generate_prompt_list
from project.modules.html_read import read_url
from project.modules.latex_gen import generate_latex
from project.modules.ollama_gen import process_job_offer_with_llm
from project.utils.data_handler import LatexVarGenerator

'''TODO: 
' - better args handling with --help handling
' - refactor some functions (read/write file, error handling)
' - implement language selection in args and in code
' - implement llm selection in args and in code
' - do some logging in an output.log and optionnally in console
' - fulfill requirements and setup.py
' - make the solution work in a docker container
' - optimize llm generation (different model, different prompt)
'''
def main():
    # Parser
    parser = argparse.ArgumentParser(description="Read and analyse HTML page.") # Create an argument parser
    parser.add_argument("html_page", help="The HTML page to read") # Add a positional argument for the file name
    args = parser.parse_args() # Parse the arguments
    read_url(args.html_page, True, html2txt)
    generator = LatexVarGenerator(json_data, latex_var_name='user') # Initialize with the JSON file

    # Generate using llm
    for index, prompt in enumerate(generate_prompt_list()):
        print(prompt)
        process_job_offer_with_llm(prompt)
        generator.merge_from_source(latex_llm, index)
    
    generator.generate_latex_vars(latex_var) # Generate variables.tex
    generate_latex(generator) # Generate LATEX file


if __name__ == "__main__":
    start_time = time.time()

    main()

    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")
