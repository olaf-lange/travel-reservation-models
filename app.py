"""
Travel Reservations Flask Backend
Provides REST API endpoints for managing hotel reservations
"""

from flask import Flask, render_template, jsonify, request
import json
import os
from datetime import datetime
import uuid

app = Flask(__name__)

DATA_FILE = 'data.json'


def load_data():
    """Load data from JSON file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"rooms": [], "reservations": []}


def save_data(data):
    """Save data to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')


@app.route('/api/rooms', methods=['GET'])
def get_rooms():
    """Get all available rooms"""
    data = load_data()
    return jsonify(data.get('rooms', []))


@app.route('/api/reservations', methods=['GET'])
def get_reservations():
    """Get all reservations"""
    data = load_data()
    return jsonify(data.get('reservations', []))


@app.route('/api/reservations', methods=['POST'])
def create_reservation():
    """Create a new reservation"""
    try:
        data = load_data()
        reservation_data = request.get_json()
        
        # Validate required fields
        required_fields = ['roomId', 'guestName', 'checkIn', 'checkOut']
        for field in required_fields:
            if field not in reservation_data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Check room availability
        room_id = reservation_data['roomId']
        room = next((r for r in data['rooms'] if r['id'] == room_id), None)
        
        if not room:
            return jsonify({'error': 'Room not found'}), 404
        
        if room['availability'] <= 0:
            return jsonify({'error': 'Room not available'}), 400
        
        # Create reservation
        reservation = {
            'id': str(uuid.uuid4()),
            'roomId': room_id,
            'guestName': reservation_data['guestName'],
            'checkIn': reservation_data['checkIn'],
            'checkOut': reservation_data['checkOut'],
            'createdAt': datetime.now().isoformat()
        }
        
        # Update room availability
        room['availability'] -= 1
        
        # Add reservation
        data['reservations'].append(reservation)
        save_data(data)
        
        return jsonify(reservation), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/reservations/<reservation_id>', methods=['DELETE'])
def cancel_reservation(reservation_id):
    """Cancel a reservation"""
    try:
        data = load_data()
        
        # Find reservation
        reservation = next((r for r in data['reservations'] if r['id'] == reservation_id), None)
        
        if not reservation:
            return jsonify({'error': 'Reservation not found'}), 404
        
        # Update room availability
        room = next((r for r in data['rooms'] if r['id'] == reservation['roomId']), None)
        if room:
            room['availability'] += 1
        
        # Remove reservation
        data['reservations'] = [r for r in data['reservations'] if r['id'] != reservation_id]
        save_data(data)
        
        return jsonify({'message': 'Reservation cancelled successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
