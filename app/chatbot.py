from flask import request
from PIL import Image
from io import BytesIO
from app.models import ImageRequest
import openai
import os
from . import db

import requests

def generate_response(input_text):
    openai.api_key=os.environ['OPENAI_API_KEY']
    model_engine="text-davinci-002"
    prompt=f"Geotechnical engineering question:{input_text}/nAnswer:"
    response=openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    print(f"response: {response}")
    return response.choices[0].text.strip()

def generate_image(prompt):
    img_response=openai.Image.create(
        prompt=prompt,
        n=5,
        size="512x512"
    )
    if not img_response:
        raise ValueError("No image generated")
    if len(img_response) < 1:
        raise ValueError("No image generated")
    if len(img_response)>1:
        print(f"Warning: Multiple images generated. Using the first one.")
    print(img_response)
    return img_response