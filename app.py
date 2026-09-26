from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# Helper function - Reusable logic
def find_event(event_id):
    return next((e for e in events if e.id == event_id), None)

# POST /events - Create a new event from JSON input
@app.route('/events', methods=['POST'])
def create_event():
    data = request.get_json()
    
    # Input Validation
    if not data or 'title' not in data or not data['title'].strip():
        return jsonify({"error": "Title is required"}), 400
    
    new_id = max([e.id for e in events], default=0) + 1
    new_event = Event(new_id, data['title'].strip())
    events.append(new_event)
    
    return jsonify(new_event.to_dict()), 201

# PATCH /events/<id> - Update title of an event
@app.route('/events/<int:id>', methods=['PATCH'])
def update_event(id):
    event = find_event(id)
    
    # Event Not Found
    if not event:
        return jsonify({"error": "Event not found"}), 404
    
    data = request.get_json()
    
    # If no title field, leave unchanged
    if data and 'title' in data:
        title = data['title']

    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "Title cannot be empty"}), 400

    event.title = title.strip()  
    return jsonify(event.to_dict()), 200

# DELETE /events/<id> - Remove an event from the list
@app.route('/events/<int:id>', methods=['DELETE'])
def delete_event(id):
    event = find_event(id)

    if not event:
        return jsonify({"error": "Event not found"}), 404

    events.remove(event)

    return jsonify({"message": f"Event {id} deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True)