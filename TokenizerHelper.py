# Importing necessary libraries
import tiktoken
from transformers import AutoTokenizer

class TokenizerHelper:
    def __init__(self, model_type, model_name):

        self.model_type = model_type
        self.model_name = model_name
        
        if model_type == "gpt":
            self.tokenizer = tiktoken.get_encoding(model_name)
        elif model_type == "hf":
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        else:
            raise ValueError("Invalid model type. Use 'gpt' for GPT models or 'hf' for Hugging Face models.")

    def count_tokens(self, text):
        """
        Count the number of tokens in the provided text using the specified tokenizer.
        
        text: The input text to tokenize
        """
        if self.model_type == "gpt":
            # For GPT models using tiktoken
            tokens = self.tokenizer.encode(text)
        elif self.model_type == "hf":
            # For Hugging Face models
            tokens = self.tokenizer.encode(text)
        return len(tokens)



# Example usage
# For GPT model tokenization 
# Use "cl100k_base" encoding for GPT-3.5 and GPT-4 models
# Use "o200k_base" encoding for GPT-4o models
gpt_tokenizer = TokenizerHelper(model_type="gpt", model_name="o200k_base")
num_tokens_gpt = gpt_tokenizer.count_tokens("This is a test sentence.")
print(f"Number of tokens (GPT): {num_tokens_gpt}")

# For Hugging Face model tokenization (e.g., LLaMA or other models)
hf_tokenizer = TokenizerHelper(model_type="hf", model_name="hf-internal-testing/llama-tokenizer")
num_tokens_hf = hf_tokenizer.count_tokens("This is a test sentence.")
print(f"Number of tokens (Hugging Face LLaMA): {num_tokens_hf}")