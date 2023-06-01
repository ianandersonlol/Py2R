# Py2R Documentation

This is a code translator tool that uses OpenAI's GPT-4 model to translate code from Python to R or from R to Python. It also generates an explanation of the translated code, focusing on how to use it.

## Table of Contents

- [Requirements](#requirements)
- [Setting up Open AI Developer Account and API Key](#Setting_Up_OpenAI_Developer_Account_and_API_Key)
- [Usage](#usage)
- [Functions](#functions)
  - [translate_code](#translate_code)
  - [explain_code](#explain_code)
-[Disclaimer](#disclaimer)

## Requirements

- Python 3.6 or later
- OpenAI Python package: `pip install openai`

## Setting Up OpenAI Developer Account and API Key

1. Visit the OpenAI website at [https://www.openai.com/](https://www.openai.com/).
2. Click on the "Sign Up" button and create an account.
3. After verifying your email address and logging in, navigate to the API section.
4. In the API section, you will find your API key. Copy this key and keep it safe; you'll need it for the next step.

## Usage

To use the code translator, you need to provide a script file as a command line argument. The script file should be either a Python script (`.py` extension) or an R script (`.r` extension). The translated code will be saved in a new file with the same name as the input file but with the extension changed to the target language. For example, if you provide a Python script as input, the translated R script will have the same name with the `_rewritten.R` suffix, and vice versa for R scripts.

Run the script with the following command:

```bash
python py2r.py <filename>
```

Replace `<filename>` with the path to your input script file.

## Functions

### translate_code

```python
def translate_code(code, source_language, target_language)
```

Translates the code from the source language to the target language using OpenAI's GPT-4 model.

**Arguments:**

- `code`: The code to be translated as a string.
- `source_language`: The source programming language as a string. It should be either "Python" or "R".
- `target_language`: The target programming language as a string. It should be either "Python" or "R".

**Returns:**

- A string containing the translated code.

### explain_code

```python
def explain_code(code)
```

Generates an explanation of the code with a focus on how to use it using OpenAI's GPT-4 model.

**Arguments:**

- `code`: The code to be explained as a string.

**Returns:**

- None. The explanation is printed to the console.


## Disclaimer

The OpenAI GPT4 model is a powerful tool but it is not infallible. It may not always generate a perfect explanation, particularly for complex or poorly written code. Always review the generated explanations and use your own judgement.