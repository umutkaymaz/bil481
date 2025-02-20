import requests

# Testing requests

response = requests.get("https://upload.wikimedia.org/wikipedia/commons/5/5d/Seminole_courhouse.JPG")

with open("./webScraping_TEST/image.jpg","wb") as image:
    image.write(response.content)

print("Download completed.")