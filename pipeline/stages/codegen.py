from google import genai
from dotenv import load_dotenv
from pathlib import Path
import os
from pipeline.stages.sandbox import validate_safe_path
from pipeline.util import clean_code_block

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_code(plan: str):

    with open("pipeline/prompts/codegen.txt", "r") as file:
        codegen_prompt = file.read()

    prompt = f"""
    {codegen_prompt}

    IMPLEMENTATION PLAN:
    {plan}
    """

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt,
    )

    generated_code = clean_code_block(response.text)

    sandbox_dir = Path("sandbox/generated")
    sandbox_dir.mkdir(parents=True, exist_ok=True)

    output_file = validate_safe_path(
    sandbox_dir / "generated_api.py"
)

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(generated_code)

    return output_file