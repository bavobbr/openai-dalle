# main.py
import os

import openai
import requests
from dotenv import load_dotenv
from flask import Flask
from flask import request, redirect

load_dotenv()
my_secret_key = os.getenv("OPENAI_API_KEY")
s3_lambda = os.getenv("S3_LAMBDA")
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello Dalle!"


@app.route("/generate", methods=['POST'])
def generate():
    """
    main endpoint to accept a prompt request and generate a image
    :return: the URL info of the created image
    """
    myprompt = request.form.get('prompt')
    print('The prompt is: {}'.format(myprompt))
    openai.api_key = my_secret_key
    resp = openai.Image.create(prompt=myprompt, n=1, size="512x512")
    print(resp)
    original_url = resp.data[0].url
    url = s3_lambda + '/store'
    form_data = {'location': original_url}
    server = requests.post(url, data=form_data)
    output = server.text
    print('response from S3 server: \n', output)
    return output


@app.route("/render", methods=['GET'])
def render():
    """
    utility endpoint to directly process a request  and render the image in browser
    :return: http redirect to generated image
    """
    myprompt = request.args.get('prompt')
    print('The prompt is: {}'.format(myprompt))
    openai.api_key = my_secret_key
    resp = openai.Image.create(
        prompt=myprompt,
        n=1,
        size="512x512"
    )
    print(resp.data[0].url)
    return redirect(resp.data[0].url, code=302)
