class Entity:
    def __init__(self, name, status) -> None:
        self._name = name
        # Convert the dictionary to an immutable frozenset of items
        self._status = status

    @property
    def name(self):
        return self._name

    @property
    def status(self):
        # Optionally convert it back to a dictionary when accessed, or just keep it as frozenset
        return dict(self._status)
