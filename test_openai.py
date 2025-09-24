import openai

openai.api_key = "AIzaSyA7xHVI8x6XblV8PBMPf4dzQVdQAgBTeTE"
models = openai.Model.list()
print(models)
