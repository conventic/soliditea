import json
import os
import re
import subprocess
import typer
from dotenv import load_dotenv
from openai import OpenAI
from jinja2 import Environment, FileSystemLoader

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

app = typer.Typer()


def generate_html_report(slither_results, gpt4_results):
    filename = "report.html"
    env = Environment(loader=FileSystemLoader("templates/"))
    template = env.get_template("default.html")

    if gpt4_results:
        json_part = gpt4_results.split('```json\n', 1)[
            1].rsplit('```', 1)[0].strip()
        content = template.render(
            results=slither_results, analysis_results=json.loads(json_part))
    else:
        content = template.render(results=slither_results)

    with open(filename, mode="w", encoding="utf-8") as message:
        message.write(content)
        print(f"... wrote {filename}")


def remove_comments(solidity_code):
    # Remove single line comments
    solidity_code = re.sub(r'//.*', '', solidity_code)
    # Remove multi-line comments
    solidity_code = re.sub(r'/\*.*?\*/', '', solidity_code, flags=re.DOTALL)
    return solidity_code


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
        "Provide an exhaustive list of all issues and vulnerabilities inside the following smart contract. "
        "Be detailed in the issue descriptions and describe the actors involved. Include one exploit scenario "
        "in each vulnerability. Output as a valid JSON with a list of objects that each have 'description', "
        "'action', 'severity', 'actors', 'scenario', and 'type'. 'type' can be 'usability', 'vulnerability', "
        "'optimization', or 'suggestion'. 'actors' is a list of the involved actors. 'severity' can be "
        "'low + ice block emoji', 'medium', or 'high + fire emoji'. "
        "Output high severity findings first and low severity findings last.\n\n"
        "```\n" + flattened_code + "\n```\n\n"
        "Results from static code analysis: \n\n"
        "```\n" + json.dumps(slither_results, indent=2) + "\n```\n\n"
    )
    return prompt


def query_llm(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[{"role": "system", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
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
def analyze(
        contract_path: str,
        use_ai: bool = typer.Option(True, help="Use AI for further analysis"),
        without_comments: bool = typer.Option(
            False, help="Remove comments from the contract before analysis"),
        html: bool = typer.Option(False, help="generate HTML report")):
    """
    Analyze a smart contract for vulnerabilities.
    """
    slither_results = run_slither_analysis(contract_path)
    if slither_results:
        typer.echo("Static analysis completed.")

        if use_ai:
            flattened_code = flatten_contract(contract_path)
            if without_comments:
                flattened_code = remove_comments(flattened_code)

            prompt = generate_prompt(flattened_code, slither_results)

            # Write the generated prompt to a file
            with open('llm_prompt.txt', 'w') as file:
                file.write(prompt)
            print("Generated Prompt for LLM written to llm_prompt.txt")
            print("AI code review in progress. This might take a while.")
            print("...")

            gpt4_response = query_llm(prompt)
            typer.echo("AI Analysis Results:")
            typer.echo(gpt4_response)
            if html:
                generate_html_report(slither_results['results'], gpt4_response)
        else:
            typer.echo(json.dumps(slither_results, indent=2))
            if html:
                generate_html_report(slither_results['results'])
    else:
        typer.echo("Failed to analyze the contract.")


if __name__ == "__main__":
    app()
