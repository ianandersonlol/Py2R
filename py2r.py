from openai import OpenAI
import sys
import os
import re
import argparse
import logging
from pathlib import Path

def setup_logging(verbose=False, quiet=False):
    """Setup logging configuration based on verbosity settings."""
    if quiet:
        level = logging.ERROR
    elif verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO
    
    logging.basicConfig(
        level=level,
        format='%(levelname)s: %(message)s',
        handlers=[logging.StreamHandler()]
    )

def validate_api_key():
    """Validate that OpenAI API key is available."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logging.error("OPENAI_API_KEY environment variable is not set.")
        logging.error("Please set it with: export OPENAI_API_KEY=your_api_key_here")
        sys.exit(1)
    return api_key

def translate_code(client, code, source_language, target_language):
    """Translate code from source language to target language using OpenAI."""
    try:
        logging.info("Generating translated code, please wait...")
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
        # Remove code blocks with more robust regex
        translated_code = re.sub(r'```\w*\n?', '', translated_code)
        translated_code = re.sub(r'```', '', translated_code)
        return translated_code.strip()
    except Exception as e:
        logging.error(f"Failed to translate code: {e}")
        logging.error("Please check your API key and internet connection.")
        sys.exit(1)

def explain_code(client, code):
    """Generate an explanation of the translated code."""
    try:
        logging.info("Generating code explanation, please wait...")
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
        logging.error(f"Failed to explain code: {e}")
        logging.error("Please check your API key and internet connection.")
        sys.exit(1)

def determine_languages_and_output(filename, output_filename=None):
    """Determine source/target languages and output filename based on input file."""
    basename = os.path.splitext(filename)[0]
    extension = os.path.splitext(filename)[1].lower()
    
    if extension == '.py':
        source_lang, target_lang = "Python", "R"
        default_output = f"{basename}_translated.R"
    elif extension == '.r':
        source_lang, target_lang = "R", "Python"
        default_output = f"{basename}_translated.py"
    else:
        logging.error(f"Unsupported file extension: {extension}")
        logging.error("Supported extensions: .py, .r, .R")
        logging.error("Please provide a Python (.py) or R (.r/.R) script.")
        sys.exit(1)
    
    output_file = output_filename if output_filename else default_output
    return source_lang, target_lang, output_file

def read_input_file(filename):
    """Read and return contents of input file."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        logging.error(f"File not found: {filename}")
        logging.error("Please check the file path and try again.")
        sys.exit(1)
    except PermissionError:
        logging.error(f"Permission denied reading file: {filename}")
        logging.error("Please check file permissions and try again.")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Failed to read file {filename}: {e}")
        sys.exit(1)

def write_output_file(filename, content):
    """Write translated code to output file."""
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
        logging.info(f"Translated code saved to: {filename}")
    except PermissionError:
        logging.error(f"Permission denied writing to file: {filename}")
        logging.error("Please check directory permissions and try again.")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Failed to write file {filename}: {e}")
        sys.exit(1)

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Translate code between Python and R using AI",
        epilog="Example: python py2r.py script.py -o translated_script.R --no-explain"
    )
    
    parser.add_argument(
        'filename',
        help='Input file to translate (.py or .r/.R)'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output filename (default: input_translated.ext)'
    )
    
    parser.add_argument(
        '--no-explain',
        action='store_true',
        help='Skip code explanation step'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Suppress all output except errors'
    )
    
    return parser.parse_args()

def main():
    """Main function to orchestrate the translation process."""
    args = parse_arguments()
    
    # Validate argument combinations
    if args.verbose and args.quiet:
        print("Error: Cannot use both --verbose and --quiet options together.")
        sys.exit(1)
    
    # Setup logging
    setup_logging(args.verbose, args.quiet)
    
    # Validate API key and create client
    api_key = validate_api_key()
    client = OpenAI(api_key=api_key)
    
    # Determine languages and output file
    source_lang, target_lang, output_file = determine_languages_and_output(
        args.filename, args.output
    )
    
    logging.info(f"Translating {source_lang} to {target_lang}")
    logging.debug(f"Input file: {args.filename}")
    logging.debug(f"Output file: {output_file}")
    
    # Read input file
    code = read_input_file(args.filename)
    
    # Translate code
    translated_code = translate_code(client, code, source_lang, target_lang)
    
    # Write output file
    write_output_file(output_file, translated_code)
    
    # Explain code if requested
    if not args.no_explain:
        explain_code(client, translated_code)
    else:
        logging.info("Skipping code explanation as requested")

if __name__ == "__main__":
    main()