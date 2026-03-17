import requests



base_url = "https://api.thecatapi.com/v1"

def get_gatos():
    url =  f"{base_url}/breeds"

    header = {
        "x-api-key": "live_bBvEYQtgPIAhmHEVDJ0na6L0PT8wKOiFom3kvumhMrDkzrVnH1psg7hmghzoN1U2"
    }

    resposta = requests.get(url, headers=header)

    return resposta.json()

def get_images():
    url = "https://api.thecatapi.com/v1/images/search"

    resposta = requests.get(url)

    return resposta.json()[0]
