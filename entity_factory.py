import json
from entity import Entity
import os

class EntityFactory:
    _entities = {}

    def load_entities(self, directory):
        """Load entities from all JSON files in a specified directory."""
        # Iterate over all files in the given directory
        for filename in os.listdir(directory):
            if filename.endswith('.json'):
                json_file = os.path.join(directory, filename)
                with open(json_file, 'r') as file:
                    entities = json.load(file)
                    for name, details in entities.items():
                        if name not in EntityFactory._entities:
                            immutable_status = details.items()
                            EntityFactory._entities[name] = Entity(name, immutable_status)


    def get_entity(self, name):
        """Retrieve an already loaded entity by name."""
        return EntityFactory._entities.get(name)
    
    def get_entities(self, names):
        """Retrieve a list of entities by name."""
        return [EntityFactory._entities.get(name) for name in names]
    
    def get_all_entities_with_field(self, field):
        """Retrieve all entities that have a specific field."""
        return [entity for entity in EntityFactory._entities.values() if field in entity.status]
