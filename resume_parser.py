from transformers import GPT2Tokenizer,GPT2LMHeadModel
import json
import torch 
import pdfplumber 
import io
tokenizer= GPT2Tokenizer.from_pretrained("gpt2")
model= GPT2LMHeadModel.from_pretrained("gpt2")
model.eval()


def extract_text_from_pdf(file_bytes:bytes)->str:
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        return "\n".join(pages.extract_text() or "" for pages in pdf.pages)

def extract_resume_info(text: str) ->dict:
    prompt=f""" You are an AI assistant. Extract the following details from this resume:
    1.  name 
    2. Email
    3. Phone_number
    4.Skills 
    5. Education 
    6. Work_experience 
    7. achievements 
    8. job_position 
     Respond in json format 
     Resume:
     {text}
    """
    inputs= tokenizer.encode(prompt,return_tensors="pt")
    inputs=inputs[:, :1024]
    outputs=model.generate(inputs,max_new_tokens=150,do_sample=True,top_p=0.95,top_k=30)
    response=tokenizer.decode(outputs[0],skip_special_tokens=True)
    try:
        result= json.loads(response)
    except json.JSONDecodeError:
        result = {"error": " Failed to parse response", "raw_output": response}

    return result
    
    
    
