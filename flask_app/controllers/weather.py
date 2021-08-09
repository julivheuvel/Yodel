import requests
import math
        
        
id = 1


pokemon_url = requests.get(f"https://pokeapi.co/api/v2/pokemon/{id}/")
pokemon_data = pokemon_url.json()

pokemon = pokemon_data['name']


print(pokemon)