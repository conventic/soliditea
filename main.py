import json
import openai
import os
import subprocess
import typer
from dotenv import load_dotenv

load_dotenv()

app = typer.Typer()


def flatten_contract(contract_path):
    try:
        flattened_code = subprocess.check_output(
            ['truffle-flattener', contract_path])
        return flattened_code.decode('utf-8')
    except subprocess.CalledProcessError as e:
        print(f"Error flattening contract: {e}")
        return None


def run_slither_analysis(contract_path):
    output_file = "slither_output.json"
    # Remove the existing output file if it exists
    if os.path.exists(output_file):
        os.remove(output_file)

    try:
        subprocess.check_output(
            ['slither', contract_path, '--json', output_file])
    except subprocess.CalledProcessError as e:
        # Check if the output file is generated despite the error
        if os.path.exists(output_file):
            with open(output_file, 'r') as file:
                return json.load(file)
        else:
            print(f"Error running Slither: {e}")
            return None


def generate_prompt(flattened_code, slither_results):
    prompt = (
        f"Provide an exhaustive list of all issues and vulnerabilities inside the following smart contract. "
        f"Be detailed in the issue descriptions and describe the actors involved. Include one exploit scenario "
        f"in each vulnerability. Output as a valid JSON with a list of objects that each have 'description', "
        f"'action', 'severity', 'actors', 'scenario', and 'type'. 'type' can be 'usability', 'vulnerability', "
        f"'optimization', or 'suggestion'. 'actors' is a list of the involved actors. 'severity' can be "
        f"'low + ice block emoji', 'medium', or 'high + fire emoji'. \n\n```\n{flattened_code}\n```\n\n"
        f"Results from static code analysis: \n\n```\n{json.dumps(slither_results, indent=2)}\n```\n\n"
    )
    return prompt


def query_llm(prompt):
    openai.api_key = os.getenv('OPENAI_API_KEY')
    try:
        response = openai.Completion.create(
            engine="gpt-4-1106-preview",
            prompt=prompt,
            max_tokens=4096
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error querying GPT-4: {e}")
        return None


@app.command()
def flatten(contract_path: str):
    """
    Flatten a smart contract.
    """
    flattened_code = flatten_contract(contract_path)
    if flattened_code:
        typer.echo("Contract successfully flattened.")
        typer.echo(flattened_code)
    else:
        typer.echo("Failed to flatten the contract.")


@app.command()
def analyze(contract_path: str, use_ai: bool = typer.Option(True, help="Use AI for further analysis")):
    """
    Analyze a smart contract for vulnerabilities.
    """
    slither_results = run_slither_analysis(contract_path)
    if slither_results:
        typer.echo("Static analysis completed.")
        if use_ai:
            flattened_code = flatten_contract(contract_path)
            prompt = generate_prompt(flattened_code, slither_results)
            gpt4_response = query_llm(prompt)
            typer.echo("AI Analysis Results:")
            typer.echo(gpt4_response)
        else:
            typer.echo(json.dumps(slither_results, indent=2))
    else:
        typer.echo("Failed to analyze the contract.")


if __name__ == "__main__":
    app()
