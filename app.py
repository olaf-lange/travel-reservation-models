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


@app.route('/api/reservations/<reservation_id>', methods=['PUT'])
def update_reservation(reservation_id):
    """Update an existing reservation"""
    try:
        data = load_data()
        
        # Find reservation
        reservation = next((r for r in data['reservations'] if r['id'] == reservation_id), None)
        
        if not reservation:
            return jsonify({'error': 'Reservation not found'}), 404
        
        # Handle invalid JSON
        try:
            update_data = request.get_json()
        except Exception:
            return jsonify({'error': 'Invalid JSON format'}), 400
        
        if not update_data:
            return jsonify({'error': 'No update data provided'}), 400
        
        # Validate at least one field is provided for update
        valid_fields = ['roomId', 'guestName', 'checkIn', 'checkOut']
        if not any(field in update_data for field in valid_fields):
            return jsonify({'error': 'No valid fields provided for update'}), 400
        
        # Validate guest name if provided
        if 'guestName' in update_data:
            if not update_data['guestName'] or not update_data['guestName'].strip():
                return jsonify({'error': 'Guest name cannot be empty'}), 400
        
        # Validate and handle room change if provided
        if 'roomId' in update_data:
            new_room_id = update_data['roomId']
            old_room_id = reservation['roomId']
            
            # Only process room change if it's actually different
            if new_room_id != old_room_id:
                new_room = next((r for r in data['rooms'] if r['id'] == new_room_id), None)
                
                if not new_room:
                    return jsonify({'error': 'New room not found'}), 404
                
                if new_room['availability'] <= 0:
                    return jsonify({'error': 'New room not available'}), 400
                
                # Update room availability
                old_room = next((r for r in data['rooms'] if r['id'] == old_room_id), None)
                if old_room:
                    old_room['availability'] += 1
                new_room['availability'] -= 1
                
                reservation['roomId'] = new_room_id
        
        # Validate and update dates if provided
        if 'checkIn' in update_data or 'checkOut' in update_data:
            check_in = update_data.get('checkIn', reservation['checkIn'])
            check_out = update_data.get('checkOut', reservation['checkOut'])
            
            # Basic date format validation
            try:
                from datetime import datetime as dt
                check_in_date = dt.strptime(check_in, '%Y-%m-%d')
                check_out_date = dt.strptime(check_out, '%Y-%m-%d')
                
                if check_out_date <= check_in_date:
                    return jsonify({'error': 'Check-out date must be after check-in date'}), 400
                    
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
            
            if 'checkIn' in update_data:
                reservation['checkIn'] = check_in
            if 'checkOut' in update_data:
                reservation['checkOut'] = check_out
        
        # Update guest name if provided
        if 'guestName' in update_data:
            reservation['guestName'] = update_data['guestName'].strip()
        
        # Save updated data
        save_data(data)
        
        return jsonify(reservation), 200
        
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
