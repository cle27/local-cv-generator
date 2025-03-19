import ollama, re
from pathlib import Path
from project.utils.path_utils import latex_llm, generate_prompt_list

def extract_curly_brace_content(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Use regex to extract everything including the first `{` and the last `}`
    match = re.search(r'(\{.*\})', content, re.DOTALL)
    
    if match:
        extracted_content = match.group(1)  # Get the content including the braces
    
        with open(file_path, 'w') as file:
            file.write(extracted_content)


# Generate LaTeX with Ollama
def process_job_offer_with_llm(prompt, output_file=latex_llm, model="llama3.2:3b"):
    generate_prompt_list()
    try:
        response = ollama.generate(
            model=model,  # Use llama3, mistral, or other suitable model
            prompt=prompt,
            options={
                'temperature': 0.7,
                'num_ctx': 16000,  # Max context size for most models
                'num_predict': 1000
            }
        )
    except ollama.ResponseError as e:
        print(f"Error: {e.error}")

    # Save output
    latex_code = response['response']
    Path(output_file).write_text(latex_code)
    extract_curly_brace_content(output_file)
    print("LaTeX summary generated successfully!")


if __name__ == "__main__":
    for prompt in generate_prompt_list():
        print(prompt)
        process_job_offer_with_llm(prompt)