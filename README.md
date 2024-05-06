# Pokemon Collector

## Description
Pokemon Collector is a program developed using Object-Oriented Programming (OOP) principles, designed to fetch and display Pokémon data.
The program uses the PokeAPI for fetching Pokémon data and DynamoDB for storing and fetching of the data.

## Functionality

1. The program prompts the user to decide whether they want to draw a Pokémon.
2. If the user answers yes, a random Pokémon name is fetched from the PokeAPI.
3. If the fetched Pokémon already exists in DynamoDB 'Pokemon Collection' table, existing data is retrieved from the database and presented to the user.
4. If it doesn't exist in the database, it's details are fetched from the PokeAPI, stored for future reference in DynamoDB 'Pokemon Collection' table, and then presented to the user.

## Usage
1. Run `main.py` to start the program.
2. When prompted, enter 'Y' to fetch and display a random Pokémon or 'N' to exit the program.
3. If 'Y' is entered, a random Pokémon's information will be displayed, including its name, abilities, types, species, and description.

## Setup
Before running the program, ensure that you have installed the required dependencies:

```bash
pip install boto3 requests
```

Also, make sure you have set up AWS credentials with sufficient permissions to access DynamoDB.

## Dependencies
- boto3: The AWS SDK for Python, used to interact with DynamoDB.
- requests: Used to make HTTP requests to the PokeAPI.
