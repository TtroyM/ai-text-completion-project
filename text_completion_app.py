"""
AI Text Completion App

Author: Troy May
Date: 2025-06-01
Description: A Python application that uses OpenAI's GPT-3.5 Turbo to generate text completions
based on user input. Supports temperature and token control via terminal input.
"""

import openai
import os
from dotenv import load_dotenv

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_float_input(prompt_text, default):
    val = input(prompt_text).strip()
    return float(val) if val else default

def get_int_input(prompt_text, default):
    val = input(prompt_text).strip()
    return int(val) if val else default

def generate_response(prompt, temperature=0.7, max_tokens=150):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
    except openai.AuthenticationError:
        return "Error: Invalid API key. Please check your credentials."
    except openai.RateLimitError:
        return "Error: Rate limit exceeded. Please wait and try again."
    except openai.APIConnectionError:
        return "Error: Network issue. Please check your internet connection."
    except openai.BadRequestError:
        return "Error: Malformed request. Check your prompt or parameters."
    except Exception as e:
        return f"Unexpected error: {e}"

print("=== Generative AI Text Completion App ===")

while True:
    user_input = input("\nEnter a prompt (or type 'exit' to quit): ").strip()

    if not user_input:
        print("Input cannot be empty.")
        continue
    if len(user_input) > 1000:
        print("Input too long. Please keep it under 1000 characters.")
        continue
    if user_input.lower() == 'exit':
        print("Exiting the application.")
        break

    temperature = get_float_input("Enter temperature (0–1, default 0.7): ", 0.7)
    max_tokens = get_int_input("Enter max tokens (default 150): ", 150)

    result = generate_response(user_input, temperature, max_tokens)
    print(f"\nAI Response:\n{result}")