from transformers import GPT2LMHeadModel, GPT2Tokenizer

model = GPT2LMHeadModel.from_pretrained("./3_trained_gpt2_model")
tokenizer = GPT2Tokenizer.from_pretrained("./3_trained_gpt2_tokenizer")

# tokenizer = GPT2Tokenizer.from_pretrained('gpt2-large')
# tokenizer.pad_token = tokenizer.eos_token
# model = GPT2LMHeadModel.from_pretrained('gpt2-large')



def generate_text(input_text, model, tokenizer, max_new_tokens=200):
    # Ensure model and input are on the same device
    device = model.device

    # Adjust tokenizer padding side and pad token
    tokenizer.padding_side = 'right'
    tokenizer.pad_token = tokenizer.eos_token

    # Encode the input text and create attention mask
    encoded_input = tokenizer.encode_plus(
        input_text, 
        return_tensors='pt', 
        padding='max_length', 
        truncation=True,
        max_length=512  # Maximum length for GPT-2
    )
    input_ids = encoded_input['input_ids'].to(device)
    attention_mask = encoded_input['attention_mask'].to(device)

    output = model.generate(
        input_ids,
        attention_mask=attention_mask,
        max_length=512 + max_new_tokens,
        top_k=50,
        repetition_penalty=1.1,
        num_beams=5,
        early_stopping=True,
        no_repeat_ngram_size=2,
        length_penalty=1.0,
        pad_token_id=model.config.pad_token_id
    )

    
    return tokenizer.decode(output[0], skip_special_tokens=True)


input_text = """
Water regulation is critical to survival of soil amoebae, and D. discoideum has a rich system of contractile vacuoles which it uses to control its osmotic status. Heuser et al. reported the presence of carbonic anhydrase in cytoplasmic extracts, and they suggested a mechanism in which HCO; is the counter-ion during the acidification of the vacuoles, generating osmotically active carbonic acid and its dissociation products, which could draw water into the vacuoles. This hypothesis is supported by the discovery of a bicarbonate transporter. Steck et al. demonstrated that certain amino acids are excreted by the cells in response to hypotonicity. The vacuole system also stains with antibodies to calmodulin and has a P-type-Cat*-ATPase in contractile vacuoles, indicating that it may function in calcium homeostasis as well as water homeostasis. Add some recent developments in this area:
"""

updated_text = generate_text(input_text, model, tokenizer)
print(updated_text)
