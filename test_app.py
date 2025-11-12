"""
Comprehensive test suite for Flask API reservation update endpoint
Tests all scenarios for PUT /api/reservations/<reservation_id>
"""

import pytest
import json
import os
import tempfile
from datetime import datetime
from app import app, DATA_FILE


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def test_data():
    """Standard test data fixture"""
    return {
        "rooms": [
            {"id": 1, "name": "Room 101", "type": "Single", "price": 100, "availability": 5},
            {"id": 2, "name": "Room 201", "type": "Double", "price": 150, "availability": 1},
            {"id": 3, "name": "Room 301", "type": "Suite", "price": 250, "availability": 0}
        ],
        "reservations": [
            {
                "id": "test-reservation-1",
                "roomId": 1,
                "guestName": "John Doe",
                "checkIn": "2025-11-15",
                "checkOut": "2025-11-17",
                "createdAt": "2025-11-10T10:00:00"
            }
        ]
    }


@pytest.fixture(autouse=True)
def setup_test_data(test_data):
    """Setup and teardown test data for each test"""
    # Save test data
    with open(DATA_FILE, 'w') as f:
        json.dump(test_data, f)
    
    yield
    
    # Cleanup after test
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)


# ============================================================================
# 1. SUCCESSFUL UPDATE TESTS
# ============================================================================

def test_update_guest_name_only(client):
    """Update only guest name, verify other fields unchanged"""
    response = client.put('/api/reservations/test-reservation-1',
                         json={'guestName': 'Jane Smith'},
                         content_type='application/json')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['guestName'] == 'Jane Smith'
    assert data['roomId'] == 1
    assert data['checkIn'] == '2025-11-15'
    assert data['checkOut'] == '2025-11-17'
    assert data['id'] == 'test-reservation-1'
    assert data['createdAt'] == '2025-11-10T10:00:00'


def test_update_dates_only(client):
    """Update check-in and check-out dates only"""
    response = client.put('/api/reservations/test-reservation-1',
                         json={'checkIn': '2025-11-20', 'checkOut': '2025-11-22'},
                         content_type='application/json')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['checkIn'] == '2025-11-20'
    assert data['checkOut'] == '2025-11-22'
    assert data['guestName'] == 'John Doe'
    assert data['roomId'] == 1


def test_update_room_id_only(client):
    """Change room, verify availability adjustments"""
    response = client.put('/api/reservations/test-reservation-1',
                         json={'roomId': 2},
                         content_type='application/json')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['roomId'] == 2
    
    # Verify room availability changes
    with open(DATA_FILE, 'r') as f:
        saved_data = json.load(f)
    
    room1 = next(r for r in saved_data['rooms'] if r['id'] == 1)
    room2 = next(r for r in saved_data['rooms'] if r['id'] == 2)
    assert room1['availability'] == 6  # Restored +1
    assert room2['availability'] == 0  # Reduced -1


def test_update_multiple_fields(client):
    """Update name, dates, and room together"""
    response = client.put('/api/reservations/test-reservation-1',
                         json={
                             'guestName': 'Bob Wilson',
                             'roomId': 2,
                             'checkIn': '2025-12-01',
                             'checkOut': '2025-12-05'
                         },
                         content_type='application/json')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['guestName'] == 'Bob Wilson'
    assert data['roomId'] == 2
    assert data['checkIn'] == '2025-12-01'
    assert data['checkOut'] == '2025-12-05'


def test_partial_update_preserves_other_fields(client):
    """Verify unchanged fields remain intact"""
    response = client.put('/api/reservations/test-reservation-1',
                         json={'checkIn': '2025-11-16'},
                         content_type='application/json')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['checkIn'] == '2025-11-16'
    # All other fields should be preserved
    assert data['checkOut'] == '2025-11-17'
    assert data['guestName'] == 'John Doe'
    assert data['roomId'] == 1
    assert data['id'] == 'test-reservation-1'
    assert data['createdAt'] == '2025-11-10T10:00:00'


def test_update_preserves_id_and_created_at(client):
    """Ensure immutable fields never change"""
    original_id = 'test-reservation-1'
    original_created = '2025-11-10T10:00:00'
    
    response = client.put('/api/reservations/test-reservation-1',
                         json={
                             'guestName': 'Updated Name',
                             'roomId': 2,
                             'checkIn': '2025-12-01',
                             'checkOut': '2025-12-05'
                         },
                         content_type='application/json')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == original_id
    assert data['createdAt'] == original_created


# ============================================================================
# 2. VALIDATION ERROR TESTS
# ============================================================================

def test_update_nonexistent_reservation(client):
    """Should return 404 for non-existent reservation"""
    response = client.put('/api/reservations/nonexistent-id',
                         json={'guestName': 'Test'},
                         content_type='application/json')
    
    assert response.status_code == 404
    assert 'error' in response.get_json()


def test_update_with_nonexistent_room(client):
    """Should return 404 when changing to invalid room"""
    response = client.put('/api/reservations/test-reservation-1',
                         json={'roomId': 999},
                         content_type='application/json')
    
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data
    assert 'room not found' in data['error'].lower()


def test_update_with_unavailable_room(client):
    """Should return 400 when new room has 0 availability"""
    response = client.put('/api/reservations/test-reservation-1',
                         json={'roomId': 3},
                         content_type='application/json')
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert 'not available' in data['error'].lower()


def test_update_with_invalid_date_format(client):
    """Should return 400 for malformed dates"""
    response = client.put('/api/reservations/test-reservation-1',
                         json={'checkIn': '15-11-2025'},  # Wrong format
                         content_type='application/json')
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert 'date format' in data['error'].lower()


def test_update_with_checkout_before_checkin(client):
    """Should return 400 for invalid date range"""
    response = client.put('/api/reservations/test-reservation-1',
                         json={'checkIn': '2025-11-20', 'checkOut': '2025-11-18'},
                         content_type='application/json')
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert 'after' in data['error'].lower()


def test_update_with_empty_guest_name(client):
    """Should return 400 for empty/whitespace name"""
    response = client.put('/api/reservations/test-reservation-1',
                         json={'guestName': '   '},
                         content_type='application/json')
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert 'empty' in data['error'].lower()


def test_update_with_no_fields(client):
    """Should return 400 if no update fields provided"""
    response = client.put('/api/reservations/test-reservation-1',
                         json={},
                         content_type='application/json')
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data


def test_update_with_invalid_json(client):
    """Should return 400 for malformed request body"""
    response = client.put('/api/reservations/test-reservation-1',
                         data='not valid json',
                         content_type='application/json')
    
    assert response.status_code == 400


# ============================================================================
# 3. ROOM AVAILABILITY TESTS
# ============================================================================

def test_room_availability_restored_on_room_change(client):
    """Old room +1, new room -1"""
    # Initial state: Room 1 has 5 available, Room 2 has 1 available
    response = client.put('/api/reservations/test-reservation-1',
                         json={'roomId': 2},
                         content_type='application/json')
    
    assert response.status_code == 200
    
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    
    room1 = next(r for r in data['rooms'] if r['id'] == 1)
    room2 = next(r for r in data['rooms'] if r['id'] == 2)
    
    assert room1['availability'] == 6
    assert room2['availability'] == 0


def test_room_availability_unchanged_when_keeping_same_room(client):
    """No change if room stays same"""
    response = client.put('/api/reservations/test-reservation-1',
                         json={'roomId': 1, 'guestName': 'Updated Name'},
                         content_type='application/json')
    
    assert response.status_code == 200
    
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    
    room1 = next(r for r in data['rooms'] if r['id'] == 1)
    assert room1['availability'] == 5  # Unchanged


def test_cannot_update_to_fully_booked_room(client):
    """Should fail if target room has 0 availability"""
    response = client.put('/api/reservations/test-reservation-1',
                         json={'roomId': 3},
                         content_type='application/json')
    
    assert response.status_code == 400


def test_room_availability_consistent_after_failed_update(client):
    """No changes on validation failure"""
    # Try to update with invalid data
    response = client.put('/api/reservations/test-reservation-1',
                         json={'roomId': 999},  # Invalid room
                         content_type='application/json')
    
    assert response.status_code == 404
    
    # Verify availability unchanged
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    
    room1 = next(r for r in data['rooms'] if r['id'] == 1)
    assert room1['availability'] == 5  # Should be unchanged


# ============================================================================
# 4. DATA INTEGRITY TESTS
# ============================================================================

def test_update_does_not_create_duplicate_reservation(client):
    """Should modify existing, not create new"""
    response = client.put('/api/reservations/test-reservation-1',
                         json={'guestName': 'Updated Name'},
                         content_type='application/json')
    
    assert response.status_code == 200
    
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    
    assert len(data['reservations']) == 1  # Still only one reservation


def test_update_persists_to_data_file(client):
    """Verify changes are saved to JSON"""
    response = client.put('/api/reservations/test-reservation-1',
                         json={'guestName': 'Persisted Name'},
                         content_type='application/json')
    
    assert response.status_code == 200
    
    # Read directly from file
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    
    reservation = data['reservations'][0]
    assert reservation['guestName'] == 'Persisted Name'


def test_original_reservation_id_never_changes(client):
    """UUID must remain constant"""
    original_id = 'test-reservation-1'
    
    # Perform multiple updates
    client.put('/api/reservations/test-reservation-1',
              json={'guestName': 'First Update'},
              content_type='application/json')
    
    response = client.put('/api/reservations/test-reservation-1',
                         json={'guestName': 'Second Update'},
                         content_type='application/json')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == original_id


def test_created_at_timestamp_never_changes(client):
    """Creation time is immutable"""
    original_created = '2025-11-10T10:00:00'
    
    response = client.put('/api/reservations/test-reservation-1',
                         json={'guestName': 'Updated Name'},
                         content_type='application/json')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['createdAt'] == original_created


# ============================================================================
# 5. EDGE CASES
# ============================================================================

def test_update_reservation_with_special_characters_in_name(client):
    """Unicode, emojis, etc."""
    special_name = "José García 🎉 O'Brien-Smith"
    response = client.put('/api/reservations/test-reservation-1',
                         json={'guestName': special_name},
                         content_type='application/json')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['guestName'] == special_name


def test_update_with_very_long_guest_name(client):
    """Test reasonable limits"""
    long_name = "A" * 500  # 500 character name
    response = client.put('/api/reservations/test-reservation-1',
                         json={'guestName': long_name},
                         content_type='application/json')
    
    # Should succeed (no explicit length limit in current implementation)
    assert response.status_code == 200
    data = response.get_json()
    assert data['guestName'] == long_name


def test_update_with_past_dates(client):
    """Should allow or reject based on business logic"""
    response = client.put('/api/reservations/test-reservation-1',
                         json={'checkIn': '2020-01-01', 'checkOut': '2020-01-05'},
                         content_type='application/json')
    
    # Current implementation allows past dates
    assert response.status_code == 200


def test_update_with_far_future_dates(client):
    """Test date boundaries"""
    response = client.put('/api/reservations/test-reservation-1',
                         json={'checkIn': '2099-12-25', 'checkOut': '2099-12-31'},
                         content_type='application/json')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['checkIn'] == '2099-12-25'
    assert data['checkOut'] == '2099-12-31'


def test_update_same_values_as_current(client):
    """Should succeed with no actual changes"""
    response = client.put('/api/reservations/test-reservation-1',
                         json={
                             'guestName': 'John Doe',
                             'roomId': 1,
                             'checkIn': '2025-11-15',
                             'checkOut': '2025-11-17'
                         },
                         content_type='application/json')
    
    assert response.status_code == 200


# ============================================================================
# 6. HTTP METHOD TESTS
# ============================================================================

def test_put_endpoint_returns_200_on_success(client):
    """Correct status code"""
    response = client.put('/api/reservations/test-reservation-1',
                         json={'guestName': 'Test'},
                         content_type='application/json')
    
    assert response.status_code == 200


def test_put_endpoint_returns_updated_object(client):
    """Response includes all fields"""
    response = client.put('/api/reservations/test-reservation-1',
                         json={'guestName': 'Test Name'},
                         content_type='application/json')
    
    assert response.status_code == 200
    data = response.get_json()
    
    # Verify all required fields are present
    assert 'id' in data
    assert 'roomId' in data
    assert 'guestName' in data
    assert 'checkIn' in data
    assert 'checkOut' in data
    assert 'createdAt' in data


def test_put_requires_json_content_type(client):
    """Should handle missing content-type"""
    response = client.put('/api/reservations/test-reservation-1',
                         data='{"guestName": "Test"}')
    
    # Flask will handle this - may return 400 or process it
    # The important thing is it doesn't crash
    assert response.status_code in [200, 400]


def test_other_http_methods_not_allowed(client):
    """POST/GET/PATCH to update endpoint should fail"""
    # The endpoint should only respond to PUT for this specific path pattern
    # GET and POST are handled by different routes, so we test PATCH
    response = client.patch('/api/reservations/test-reservation-1',
                           json={'guestName': 'Test'},
                           content_type='application/json')
    
    assert response.status_code == 405  # Method Not Allowed


# ============================================================================
# ADDITIONAL VALIDATION TESTS
# ============================================================================

def test_update_with_invalid_field_names(client):
    """Should ignore unknown fields"""
    response = client.put('/api/reservations/test-reservation-1',
                         json={
                             'guestName': 'Valid Name',
                             'invalidField': 'Should be ignored'
                         },
                         content_type='application/json')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'invalidField' not in data


def test_update_checkout_date_only_validates_with_existing_checkin(client):
    """Updating only checkout should validate against existing checkin"""
    # Original: checkIn='2025-11-15', checkOut='2025-11-17'
    response = client.put('/api/reservations/test-reservation-1',
                         json={'checkOut': '2025-11-14'},  # Before existing checkIn
                         content_type='application/json')
    
    assert response.status_code == 400


def test_update_checkin_date_only_validates_with_existing_checkout(client):
    """Updating only checkin should validate against existing checkout"""
    # Original: checkIn='2025-11-15', checkOut='2025-11-17'
    response = client.put('/api/reservations/test-reservation-1',
                         json={'checkIn': '2025-11-18'},  # After existing checkOut
                         content_type='application/json')
    
    assert response.status_code == 400
