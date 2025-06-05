from openai import OpenAI
import sys
import os
from pathlib import Path

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("Error: OPENAI_API_KEY environment variable is not set.")
    print("Please set it with: export OPENAI_API_KEY=your_api_key_here")
    sys.exit(1)

client = OpenAI(api_key=OPENAI_API_KEY)

def translate_code(code, source_language, target_language):
    try:
        print("Generating new code, please wait...")
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": f"You are a helpful assistant that translates {source_language} code to {target_language} code."},
                {"role": "user", "content": code},
            ],
            temperature=0.7,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        translated_code = response.choices[0].message.content.strip()
        translated_code = translated_code.replace("```python", "").replace("```R", "").replace("```", "")
        return translated_code.strip()
    except Exception as e:
        print(f"Failed to translate code: {e}")
        sys.exit(1)

def explain_code(code):
    try:
        print("Generating explanation, please wait...")
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Your name is BinkyBonky and You are a knowledgeable AI trained to explain code to people."},
                {"role": "user", "content": f"Please generate an explanation for the following file with a focus on how to use it. This should be in plain language and not in markdown as your response will be printed to the terminal:\n{code}"},
            ],
            temperature=0.7,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        explanation = response.choices[0].message.content.strip()
        print(explanation)
    except Exception as e:
        print(f"Failed to explain code: {e}")
        sys.exit(1)
# Check that a filename has been provided as a command line argument
if len(sys.argv) < 2:
    print("Please provide a filename as a command line argument.")
    sys.exit(1)

filename = sys.argv[1]
basename = os.path.splitext(filename)[0]
extension = os.path.splitext(filename)[1]

try:
    with open(filename, 'r') as file:
        code = file.read()
except Exception as e:
    print(f"Failed to read file: {e}")
    sys.exit(1)

if extension == '.py':
    new_code = translate_code(code, "Python", "R")
    new_filename = f"{basename}_translated.R"
elif extension == '.r':
    new_code = translate_code(code, "R", "Python")
    new_filename = f"{basename}_translated.py"
else:
    print("Unsupported file extension. Please provide a Python or R script.")
    sys.exit(1)

try:
    with open(new_filename, 'w') as file:
        file.write(new_code)
except Exception as e:
    print(f"Failed to write new file: {e}")
    sys.exit(1)

try:
    with open(new_filename, 'r') as file:
        new_code = file.read()
except Exception as e:
    print(f"Failed to read new file: {e}")
    sys.exit(1)

explain_code(new_code)

