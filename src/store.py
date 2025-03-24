import json
from dataclasses import dataclass, field
from typing import Dict, List, Any

@dataclass
class StoreUUIDS:
    data: Dict[str, List[Any]] = field(default_factory=dict)
    storage_file: str = "store_data.json"

    # Save data to a file
    def save(self):
        with open(self.storage_file, "w") as f:
            json.dump(self.data, f)

    # Load data from a file
    def load(self):
        try:
            with open(self.storage_file, "r") as f:
                self.data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.data = {}

    # Append data to an existing key
    def append(self, key: str, values: List[Any]):
        if key in self.data:
            self.data[key].extend(values)
        else:
            self.data[key] = values
        self.save()  # Save after updating

    # Get all stored data
    def get_all(self):
        return self.data

    # Get a specific key's data
    def get(self, key: str):
        return self.data.get(key, f"Key '{key}' not found.")

    # Delete an entry by key
    def delete(self, key: str):
        if key in self.data:
            del self.data[key]
            self.save()
        else:
            print(f"Key '{key}' not found in the dictionary.")

    # Remove and return an entry
    def pop(self, key: str):
        value = self.data.pop(key, f"Key '{key}' not found.")
        self.save()
        return value

# Example Usage
store = StoreUUIDS()
store.load()  # Load existing data