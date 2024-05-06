from pokemon import Pokemon
import boto3
import requests
import random

class PokemonCollector:

    def __init__(self):
        self.table = self.get_dynamodb_table()
        
        self.fetch_pokemon()

    def get_dynamodb_table(self):
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

        # Check if the table already exists
        existing_tables = dynamodb.meta.client.list_tables()['TableNames']
        if not 'PokemonCollection' in existing_tables:
            self.create_dynamodb_table(dynamodb)
        
        return dynamodb.Table('PokemonCollection')

    def create_dynamodb_table(self, dynamodb):
        table = dynamodb.create_table(
            TableName='PokemonCollection',
            KeySchema=[
                {
                    'AttributeName': 'name',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'name',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )

        # Wait for table to be created
        table.meta.client.get_waiter('table_exists').wait(TableName='PokemonCollection')

    def get_pokemon(self, name):
        """
        Retrieves Pokemon data from DynamoDB based on the given name.
        
        Parameters:
        - name (str): The name of the Pokemon to retrieve.
        
        Returns:
        - Pokemon: A Pokemon object containing the retrieved information.
        """
    
        response = self.table.get_item(Key={'name' : name})
        
        if 'Item' in response:
            item = response['Item']
            return Pokemon(item['name'], item['abilities'], item['types'], item['species'], item['description'])
        
        return None
    
    def add_to_dynamodb(self, pokemon):
        """
        Adds a Pokemon object to DynamoDB.
        
        Parameters:
        - pokemon (Pokemon): The Pokemon object to add to DynamoDB.
        """

        self.table.put_item(Item=pokemon.to_dict())
    
    def create_pokemon(self, name):
        """
        Fetches Pokemon data from the PokeAPI based on the given name.
        Retrieves information such as abilities, types, species, and description.
        
        Parameters:
        - name (str): The name of the Pokemon to fetch information for.
        
        Returns:
        - Pokemon: A Pokemon object containing the acquired information.
        """

        info = requests.get(f'https://pokeapi.co/api/v2/pokemon/{name}').json()

        abilities = [ability['ability']['name'] for ability in info['abilities']]
        types = [p_type['type']['name'] for p_type in info['types']]
        species_url = info['species']['url']
        species = requests.get(species_url).json()['genera'][7]['genus']
        descriptions = requests.get(species_url).json()['flavor_text_entries']
        description = next((desc['flavor_text'] for desc in descriptions if desc['language']['name'] == 'en'), '')

        return Pokemon(name, abilities, types, species, description)

    def fetch_pokemon(self):
        """
        Fetches a random Pokemon from the PokeAPI.
        If the Pokemon data is not found in DynamoDB, fetches the data from the API, adds it to DynamoDB, and returns the Pokemon object.
        If the Pokemon data is found in DynamoDB, returns the Pokemon object directly.

        Returns:
        - Pokemon: A Pokemon object containing the fetched Pokemon's information.
        """
        
        response = requests.get('https://pokeapi.co/api/v2/pokemon/?limit=50')
        pokemon_list = response.json()['results']
        pokemon_name = random.choice(pokemon_list)['name']

        pokemon = self.get_pokemon(pokemon_name)
   
        if not pokemon:
            pokemon = self.create_pokemon(pokemon_name)
            self.add_to_dynamodb(pokemon)
        
        # prints fetched pokemon information to user
        print(pokemon.__str__())