# coding: UTF-8
import settings
import requests
import base64

headers = {
    # Request headers.
    'Content-Type': 'application/octet-stream',

    # NOTE: Replace the "Ocp-Apim-Subscription-Key" value with a valid subscription key.
    'Ocp-Apim-Subscription-Key': settings.AZKEY,
}

params = {
    # Request parameters. All of them are optional.
    'visualFeatures': 'Categories,Description',
    'details': 'Celebrities',
    'language': 'en',
}

def analyze(path):
    print("- analyze -")
    image = open(path,'rb').read()

    try:
        response = requests.post(url = 'https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/analyze',
                                 headers = headers,
                                 params = params,
                                 data = image)
        data = response.json()
        # print(data["description"]["captions"][0]["text"])
        if len(data["description"]["captions"]) == 0:
            tags = data["description"]["tags"]
            return " ".join(tags[0:int(len(tags) / 2)])
        else:
            return data["description"]["captions"][0]["text"]
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
