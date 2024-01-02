import json
from transformers import GPT2LMHeadModel, GPT2Tokenizer, TrainingArguments, Trainer
import torch
from torch.utils.data import Dataset
import os

class ArticlesDataset(Dataset):
    def __init__(self, tokenizer, folder_path, max_length):
        self.tokenizer = tokenizer
        self.input_ids = []
        self.attn_masks = []
        self.labels = []

        # Read each file in the folder
        for filename in os.listdir(folder_path):
            if filename.endswith('.txt'):  # Check if the file is a text file
                with open(os.path.join(folder_path, filename), 'r') as file:
                    lines = file.readlines()

                for line in lines:
                    abstract = line.strip()  # Remove leading/trailing whitespace
                    encodings_dict = tokenizer(abstract, truncation=True, max_length=max_length, padding="max_length")
                    
                    self.input_ids.append(torch.tensor(encodings_dict['input_ids']))
                    self.attn_masks.append(torch.tensor(encodings_dict['attention_mask']))
                    # For language modeling, labels are usually the input IDs themselves
                    self.labels.append(torch.tensor(encodings_dict['input_ids']))

    def __len__(self):
        return len(self.input_ids)

    def __getitem__(self, idx):
        return {
            'input_ids': self.input_ids[idx], 
            'attention_mask': self.attn_masks[idx],
            'labels': self.labels[idx]  # Adding labels
        }

# Load the tokenizer and model
tokenizer = GPT2Tokenizer.from_pretrained('gpt2-large')
tokenizer.pad_token = tokenizer.eos_token
model = GPT2LMHeadModel.from_pretrained('gpt2-large')

# Initialize dataset with the folder path
folder_path = 'data'  # Path to the folder containing the text files
dataset = ArticlesDataset(tokenizer, folder_path, max_length=512)

# Define training arguments
training_args = TrainingArguments(
    output_dir='./results',        
    num_train_epochs=10,              
    per_device_train_batch_size=2,  
    logging_dir='./logs',            
    logging_steps=10,
)

# Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
)

# Train the model
trainer.train()

# Save the model
model_save_path = "./5_trained_gpt2_model"
model.save_pretrained(model_save_path)

# Save the tokenizer
tokenizer_save_path = "./5_trained_gpt2_tokenizer"
tokenizer.save_pretrained(tokenizer_save_path)

print(f"Model saved to {model_save_path}")
print(f"Tokenizer saved to {tokenizer_save_path}")
