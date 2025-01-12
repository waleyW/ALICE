import os
import openai
import time
import json
from dotenv import load_dotenv
import argparse

# Load environment variables from .env file
load_dotenv(r'Your env')

# Verify if the API key is loaded correctly
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("API key not found. Please ensure the .env file is correct and the key is properly set.")

# Set API key from environment variable
openai.api_key = api_key

# Define the TPM limit and a time window
tokens_used = 0
last_check_time = time.time()
TPM_LIMIT = 200000

def gpt35_turbo_inference(prompt, text, model="gpt-4o-mini", max_tokens=1000, temperature=0.7):
    global tokens_used, last_check_time
    
    current_time = time.time()
    elapsed_time = current_time - last_check_time

    if elapsed_time > 60:
        tokens_used = 0
        last_check_time = current_time

    combined_prompt = f"{text}\n\n{prompt}"
    tokens_estimate = len(combined_prompt.split()) + max_tokens
    
    if tokens_used + tokens_estimate > TPM_LIMIT:
        sleep_time = 60 - (current_time - last_check_time)
        print(f"Rate limit approaching. Sleeping for {sleep_time:.2f} seconds...")
        time.sleep(sleep_time)
        tokens_used = 0
        last_check_time = time.time()

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "user", "content": combined_prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
        tokens_used += response.usage['total_tokens']
        return response.choices[0].message['content'].strip(), tokens_used
    except Exception as e:
        print(f"Error occurred: {e}")
        return None, tokens_used

def process_files(directory, prompt, output_directory, progress_file):
    processed_files = set()
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as file:
            processed_files.update(file.read().splitlines())

    total_files = [f for f in os.listdir(directory) if f.endswith(".txt")]
    total_count = len(total_files)
    processed_count = len(processed_files)

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # 用于存储所有结果的列表
    all_results = []
    input_questions = "question1: What type of marker is this? question2: What is the relationship between markers and DNA methylation?"

    for filename in total_files:
        if filename in processed_files:
            print(f"Skipping {filename}, already processed.")
            # 如果文件已处理，从原来的txt文件中读取结果
            output_file_path = os.path.join(output_directory, filename)
            try:
                with open(output_file_path, 'r', encoding='utf-8') as f:
                    result = f.read()
                    result_dict = {
                        "id": filename,
                        "input": input_questions,
                        "output": result
                    }
                    all_results.append(result_dict)
            except Exception as e:
                print(f"Error reading processed file {output_file_path}: {e}")
            continue

        file_path = os.path.join(directory, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                result, tokens_used = gpt35_turbo_inference(prompt, text)
                if result:
                    # 保存txt文件
                    save_result(filename, result, output_directory)
                    print(f"Processed and saved {filename}")
                    
                    # 添加到JSON结果列表
                    result_dict = {
                        "id": filename,
                        "input": input_questions,
                        "output": result
                    }
                    all_results.append(result_dict)
                    
                    processed_count += 1
                    with open(progress_file, 'a') as pfile:
                        pfile.write(f"{filename}\n")
                else:
                    print(f"Failed to process {filename}")
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

        print(f"Progress: {processed_count}/{total_count} files processed.")

    # 保存JSON文件
    json_output_path = os.path.join(output_directory, 'all_results.json')
    try:
        with open(json_output_path, 'w', encoding='utf-8') as json_file:
            json.dump(all_results, json_file, ensure_ascii=False, indent=2)
        print(f"All results saved to {json_output_path}")
    except Exception as e:
        print(f"Error writing JSON file: {e}")

def save_result(filename, result, output_directory):
    output_file_path = os.path.join(output_directory, filename)
    try:
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(result)
        print(f"Output saved to {output_file_path}")
    except Exception as e:
        print(f"Error writing to {output_file_path}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process text files with GPT-4o-mini.")
    parser.add_argument('--input_directory', type=str, required=True, help="Directory containing input text files")
    parser.add_argument('--output_directory', type=str, required=True, help="Directory to save output text files")
    parser.add_argument('--progress_file', type=str, help="File to record progress of processed files")

    args = parser.parse_args()
    
    if not args.progress_file:
        args.progress_file = os.path.join(args.output_directory, 'progress.txt')

    # Prompt definition (same as before)
    prompt = """You are a biomedical expert specialized in DNA methylation markers. 
For each marker that appears in the text, provide TWO questions and answers:

Question 1: What is the relationship between DNA methylation markers and diagnostics?
Answer 1: MetDNA marker

Question 2: What is the relationship between [Marker Name] and DNA methylation?
Answer 2: [Choose ONE of the following terms that best matches the content:
- Epigenetic Regulation and Biomarkers
- Disease-Specific Methylation Signatures
- Diagnostic, Prognostic, and Predictive Biomarkers
- DNA Methylation as a Biopsy Marker
- DNA Methylation as a Liquid Biopsy Marker
- Methylation and Immune Response]

Rules:
1. Only create Q&A pairs for markers that are specifically mentioned in the text
2. For Question 1, always answer "MetDNA marker"
3. For Question 2, choose only ONE term from the provided list based on how the marker is discussed in the text
4. Do not add any additional explanation or commentary
5. If no markers from the list are mentioned in the text, respond with "No relevant methylation markers were found in the provided text."
6. Maintain consistent formatting for all answers"""

    process_files(args.input_directory, prompt, args.output_directory, args.progress_file)