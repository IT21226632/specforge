from google import genai
from dotenv import load_dotenv
from pathlib import Path
from pipeline.stages.sandbox import validate_safe_path
import os
from pipeline.util import clean_code_block

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_tests(generated_code: str):

    with open("pipeline/prompts/testgen.txt", "r") as file:
        test_prompt = file.read()

    prompt = f"""
    {test_prompt}

    GENERATED CODE:
    {generated_code}
    """

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt,
    )

    generated_tests = clean_code_block(response.text)

    test_dir = Path("sandbox/generated/tests")
    test_dir.mkdir(parents=True, exist_ok=True)

    output_file = validate_safe_path(
        test_dir / "test_generated_api.py"
    )

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(generated_tests)

    return output_file