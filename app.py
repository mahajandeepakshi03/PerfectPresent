from flask import Flask, render_template, request, jsonify
import openai
import json
import requests
from bs4 import BeautifulSoup
import os
import matplotlib.pyplot as plt

openai.api_key = "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"

app = Flask(__name__)

def load_image_url(query,i):
    url = f"https://www.google.com/search?q={query}&source=lnms&tbm=isch"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    images = soup.find_all("img")

    # download each image and save to the folder
    for x, image in enumerate(images):
        try:
            img_url = image["src"]
            img_data = requests.get(img_url).content
            loc = r"output"
            with open(f"{loc}\{i}.jpg", "wb") as f:
                f.write(img_data)
                break
        except:
            pass

def generate_gift_suggestion(prompt):
    # Use the OpenAI API to generate a response to the prompt
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.5,
        max_tokens=1024,
        n=1,
        stop=None,
        timeout=10
    )
    # Extract the generated text from the response
    suggestion = response.choices[0].text.strip()
    return suggestion

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        prompt = request.form["prompt"]
        price = request.form["price"]
        
        real_prompt = f"Can you suggest 10 gifts related to {prompt} under {price} rupees in json form with 2 keys : gift and price"
        result = generate_gift_suggestion(real_prompt)
        json_result = json.loads(result)    #gift + price

        for i,gift in enumerate(json_result):
            load_image_url(json_result[i]["gift"],i)
            json_result[i]["img_url"] = f"output\{i}.jpg" 
            print(jsonify(json_result))

        return render_template("index.html", result=json_result)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
