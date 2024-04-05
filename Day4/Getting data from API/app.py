import requests


api_endpoint = 'https://dog.ceo/api/breeds/image/random'

def get_random_dog_image():

    # response = requests.get(api_endpoint)

    # print(response.json())
    # print(response.status_code)

    ############################################################

    with requests.get(api_endpoint) as response:
        print(response.json())
        print(response.status_code)




get_random_dog_image()