for what its worth I originally made this when open AI's API first came out and chatgpt and other out the box AI tools sucked for this... nowadays id say just throw it into Claude or ChatGPT and let it do it. 

# Py2R Documentation

This is a code translator tool that uses OpenAI's GPT-5 model to translate code from Python to R or from R to Python. It also generates an explanation of the translated code, focusing on how to use it.

## Table of Contents
- [Requirements](#requirements)
- [Setting up OpenAI Developer Account and API Key](#setting-up-openai-developer-account-and-api-key)
- [Installation](#installation)
- [Usage](#usage)
- [Command Line Options](#command-line-options)
- [Examples](#examples)
- [Functions](#functions)
- [Changelog](#changelog)
- [Disclaimer](#disclaimer)

## Requirements

- Python 3.6 or later
- OpenAI Python package: `pip install openai`
- OpenAI Developer Account and API key

## Setting Up OpenAI Developer Account and API Key

1. Visit the OpenAI website at [https://www.openai.com/](https://www.openai.com/).
2. Click on the "Sign Up" button and create an account.
3. After verifying your email address and logging in, navigate to the API section.
4. In the API section, you will find your API key. Copy this key and keep it safe.
5. Set your API key as an environment variable:
   ```bash
   export OPENAI_API_KEY=your_api_key_here
   ```

## Installation

1. Clone or download this repository
2. Install the required dependencies:
   ```bash
   pip install openai
   ```
3. Set your OpenAI API key as an environment variable (see above)

## Usage

The script accepts a Python (.py) or R (.r/.R) file and translates it to the opposite language.

Basic usage:
```bash
python py2r.py <input_file>
```

## Command Line Options

- `filename` - Required. Input file to translate (.py or .r/.R)
- `-o, --output` - Optional. Specify output filename (default: input_translated.ext)
- `--no-explain` - Optional. Skip the code explanation step
- `-v, --verbose` - Optional. Enable verbose output with debug information
- `-q, --quiet` - Optional. Suppress all output except errors
- `-h, --help` - Show help message and exit

## Examples

### Basic translation
```bash
# Translate Python to R
python py2r.py my_script.py

# Translate R to Python  
python py2r.py my_script.r
```

### Custom output filename
```bash
python py2r.py script.py -o converted_script.R
```

### Skip explanation
```bash
python py2r.py script.py --no-explain
```

### Verbose mode
```bash
python py2r.py script.py -v
```

### Quiet mode (errors only)
```bash
python py2r.py script.py -q
```

### Combined options
```bash
python py2r.py script.py -o new_script.R --no-explain -v
```

## Functions

### validate_api_key()
Validates that the OPENAI_API_KEY environment variable is set.

### translate_code(client, code, source_language, target_language)
Translates code from source language to target language using OpenAI's GPT-5 model.

**Arguments:**
- `client`: OpenAI client instance
- `code`: The code to be translated as a string
- `source_language`: Source programming language ("Python" or "R")
- `target_language`: Target programming language ("Python" or "R")

**Returns:**
- String containing the translated code

### explain_code(client, code)
Generates an explanation of the translated code using OpenAI's GPT-5 model.

**Arguments:**
- `client`: OpenAI client instance
- `code`: The code to be explained as a string

**Returns:**
- None. The explanation is printed to the console.

### determine_languages_and_output(filename, output_filename=None)
Determines source/target languages and output filename based on input file extension.

### read_input_file(filename)
Reads and returns contents of the input file with proper error handling.

### write_output_file(filename, content)
Writes translated code to the output file with proper error handling.

### setup_logging(verbose=False, quiet=False)
Configures logging based on verbosity settings.

## Changelog

### Latest Version
- **Security**: Now uses environment variables for API key instead of hardcoding
- **Modernization**: Updated to newer OpenAI client library with proper error handling
- **Efficiency**: Removed redundant file operations for better performance
- **Robustness**: Added case-insensitive file extension handling (.r, .R, .py)
- **Improved**: Better markdown removal using robust regex patterns
- **CLI**: Complete rewrite with argparse for professional command-line interface
- **Features**: Added --no-explain option to skip code explanation
- **Logging**: Implemented proper logging system with verbose (-v) and quiet (-q) modes
- **Customization**: Added custom output filename support with -o/--output option
- **Error Handling**: Comprehensive error messages with helpful guidance
- **File Support**: Added UTF-8 encoding support for better international character handling
- **Code Quality**: Modular function structure for better maintainability

### Previous Version
- Basic translation between Python and R
- Simple command-line interface
- Code explanation feature
- Hardcoded API key (security issue)

## Disclaimer

The OpenAI GPT-5 model is a powerful tool but it is not infallible. It may not always generate perfect translations or explanations, particularly for complex or poorly written code. Always review the generated code and explanations, and use your own judgment. Test translated code thoroughly before using in production environments.