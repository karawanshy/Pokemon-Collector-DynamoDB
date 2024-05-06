class Pokemon:
    
    def __init__(self, name, abilities, types, species, description):
        self.name = name
        self.abilities = abilities
        self.types = types
        self.species = species
        self.description = description

    def to_dict(self):
        # Convert abilities and types lists to strings to be stored in DynamoDB
        abilities_str = ','.join(self.abilities)
        types_str = ','.join(self.types)

        return {
                "name" : self.name,
                "abilities" : abilities_str,
                "types" : types_str,
                "species" : self.species,
                "description" : self.description
        }
    
    def __str__(self):
        ability_str = "\n".join(f"- {ability}" for ability in self.abilities)
        type_str = "\n".join(f"- {p_type}" for p_type in self.types)
        return f"\nPokemon name: {self.name}\n\nAbility:\n{ability_str}\n\nType:\n{type_str}\n\nSpecies:\n{self.species}\n\nDescription: \n{self.description}\n"
