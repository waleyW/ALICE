# Architecture
## Base Architecture
```bash
Model Type: Decoder-only Transformer
Parameters: 7B
Context Length: 32k tokens
Architecture Type: Dense
```

### Key Components
-Attention Mechanism: Grouped-query Attention (GQA)
-Position Encoding: Rotary Position Embedding (RoPE)
-Window Size: Sliding Window Attention
-Layer Structure: Multi-layer Transformer blocks

### Technical Specifications
```bash
Model Configuration:
- Hidden Size: 4096
- Intermediate Size: 14336
- Layers: 32
- Heads: 32
- Bytes per Parameter: 2
- Sliding Window Size: 4096
- Vocabulary Size: 32000
```

## Special Features
### Attention Mechanisms
GQA (Grouped-query Attention):
-Reduced memory usage
-Faster inference speed
-Better performance scaling

### Optimizations
Speed Improvements:
-Flash attention implementation
-Parallel computation
-Efficient token processing

## Implementation Details
Model Structure
```bash
Input → Embedding → Transformer Blocks → Output
    ↳ Token Embedding
    ↳ Position Encoding
    ↳ Layer Normalization
```

# Training Method
A Python script that automates the analysis of DNA methylation markers in scientific texts using GPT models. The script processes multiple text files and generates structured Q&A outputs about methylation markers and their relationships.

## Training-database Generating

Teacher Model Selction: GPT-4o

### Features
-Batch processing of text files
-Rate limiting for API calls
-Progress tracking
-Output in both TXT and JSON formats
-Error handling and recovery
-Environment variable management

### Requirements
Required Python packages
```bash 
cd LLM
pip install -r requirements.txt
```

### Setup

#### Environment Configuration
``` bash
# Create a .env file with your OpenAI API key
OPENAI_API_KEY=your_api_key_here
```

#### Directory Structure
```bash
project/
├── input/
│   └── (your text files)
├── output/
│   ├── processed_files/
│   └── progress.txt
├── .env
└── script.py
```

### Usage
```bash
python script.py --input_directory "path/to/input" --output_directory "path/to/output" --progress_file "path/to/progress.txt"
```

#### Parameters
--input_directory: Directory containing input text files
--output_directory: Directory to save output files
--progress_file: (Optional) File to track processing progress

### Output Format
#### Individual TXT Files
One file per processed input
Contains Q&A pairs about methylation markers

#### JSON Summary
all_results.json containing:
-File ID
-Input questions
-Generated answers

### Rate Limiting
TPM (Tokens Per Minute) limit: 200,000
Automatic rate limiting and sleep functionality

## Supervised Fine-tuning
MS-SWIFT (Microsoft Scalable, Weighted, Iterative, Fine-Tuning) was used for model fine-tuning.

### Download MS-SWIFT
```bash
# pip install git+https://github.com/modelscope/ms-swift.git

git clone https://github.com/modelscope/ms-swift.git
cd ms-swift
pip install -e .
```
### Training
```bash
CUDA_VISIBLE_DEVICES=0 swift sft \
    --model Mistral-7B \
    --dataset AI-ModelScope/alpaca-gpt4-data-en \
    --train_type lora \
    --output_dir output \
    ...
```
### Inference
```bash
CUDA_VISIBLE_DEVICES=0 swift infer \
    --model Qwen/Qwen2.5-7B-Instruct \
    --adapters swift/test_lora \
    --stream true \
    --infer_backend pt \
    --temperature 0 \
    --max_new_tokens 2048
```