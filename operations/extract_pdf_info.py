import fitz
import requests
from transformers import AutoProcessor, AutoModelForVision2Seq
from io import BytesIO
from transformers import AutoConfig
import torch
from PIL import Image

processor = AutoProcessor.from_pretrained("Qwen/Qwen2.5-VL-7B-Instruct")
model = AutoModelForVision2Seq.from_pretrained("Qwen/Qwen2.5-VL-7B-Instruct").to("cuda" if torch.cuda.is_available() else "cpu")

def send_to_ai(project, deliverable, doi, pdf):
    # Load PDF and get first page as image
    doc = fitz.open(stream=pdf, filetype="pdf")
    page = doc.load_page(0)  # first page (0-indexed)
    pix = page.get_pixmap(dpi=150)  # render page
    img_bytes = pix.tobytes("png")

    image = Image.open(BytesIO(img_bytes))

    prompt = "Extract project partners, authors or contributors, not  reviewers, usually inside paranthesis, and list only partners nothing else. Do not list partners twice. For example: CSC."
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": image},
                {"type": "text", "text": prompt}  
            ]
        }
    ]

    inputs = processor.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt"
    ).to(model.device)

    outputs = model.generate(**inputs, max_new_tokens=100)
    answer = processor.decode(outputs[0][inputs["input_ids"].shape[-1]:], skip_special_tokens=True)

    # Split lines, remove empty ones, strip whitespace
    partners_list = [line.strip() for line in answer.splitlines() if line.strip()]

    # Join partners into a single comma-separated string
    partners_str = ", ".join(partners_list)

    import csv

    with open("partners.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([project, deliverable, doi, partners_str])

    print("partners saved as csv.")
