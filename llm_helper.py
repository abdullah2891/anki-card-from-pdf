import subprocess

def run_llm_model(prompt: str) -> str:
    model = "llama3.2"
    
    # Command to run with shell features (e.g., command substitution)
    command = f'ollama run {model} "{prompt}"'

    # Execute the command, capturing the output
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    # Check if the command ran successfully
    if result.returncode == 0:
        return result.stdout
    else:
        pass