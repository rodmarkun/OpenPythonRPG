class EventDispatcher:
    def __init__(self):
        self.listeners = {}

    def subscribe(self, event_type, listener):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(listener)

    def unsubscribe(self, event_type, listener):
        if event_type in self.listeners:
            self.listeners[event_type].remove(listener)

    def dispatch(self, character, event_type, event_data):
        print(f"Event: {event_type} with data: {event_data}")
        if event_type in self.listeners:
            for listener in self.listeners[event_type]:
                listener.handle_event(character, event_type, event_data)
