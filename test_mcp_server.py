"""
Comprehensive test suite for MCP server reservation update functionality
Tests the update_reservation tool and validates all scenarios
"""

import pytest
import json
import os
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from mcp_server import handle_call_tool, load_data, save_data, DATA_FILE


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
# 1. SUCCESSFUL UPDATE TESTS (6 tests)
# ============================================================================

@pytest.mark.asyncio
async def test_update_reservation_guest_name_only():
    """Update only guest name"""
    result = await handle_call_tool(
        "update_reservation",
        {"reservation_id": "test-reservation-1", "guest_name": "Jane Smith"}
    )
    
    response = json.loads(result[0].text)
    assert response["success"] is True
    assert response["reservation"]["guestName"] == "Jane Smith"
    assert response["reservation"]["roomId"] == 1
    assert response["reservation"]["checkIn"] == "2025-11-15"
    assert response["reservation"]["checkOut"] == "2025-11-17"
    assert response["reservation"]["id"] == "test-reservation-1"
    assert response["reservation"]["createdAt"] == "2025-11-10T10:00:00"


@pytest.mark.asyncio
async def test_update_reservation_dates_only():
    """Update check-in and check-out dates only"""
    result = await handle_call_tool(
        "update_reservation",
        {
            "reservation_id": "test-reservation-1",
            "check_in": "2025-11-20",
            "check_out": "2025-11-22"
        }
    )
    
    response = json.loads(result[0].text)
    assert response["success"] is True
    assert response["reservation"]["checkIn"] == "2025-11-20"
    assert response["reservation"]["checkOut"] == "2025-11-22"
    assert response["reservation"]["guestName"] == "John Doe"
    assert response["reservation"]["roomId"] == 1


@pytest.mark.asyncio
async def test_update_reservation_room_only():
    """Change room, verify availability adjustments"""
    result = await handle_call_tool(
        "update_reservation",
        {"reservation_id": "test-reservation-1", "room_id": 2}
    )
    
    response = json.loads(result[0].text)
    assert response["success"] is True
    assert response["reservation"]["roomId"] == 2
    
    # Verify room availability changes
    data = load_data()
    room1 = next(r for r in data['rooms'] if r['id'] == 1)
    room2 = next(r for r in data['rooms'] if r['id'] == 2)
    assert room1['availability'] == 6  # Restored +1
    assert room2['availability'] == 0  # Reduced -1


@pytest.mark.asyncio
async def test_update_reservation_multiple_fields():
    """Update name, dates, and room together"""
    result = await handle_call_tool(
        "update_reservation",
        {
            "reservation_id": "test-reservation-1",
            "guest_name": "Bob Wilson",
            "room_id": 2,
            "check_in": "2025-12-01",
            "check_out": "2025-12-05"
        }
    )
    
    response = json.loads(result[0].text)
    assert response["success"] is True
    assert response["reservation"]["guestName"] == "Bob Wilson"
    assert response["reservation"]["roomId"] == 2
    assert response["reservation"]["checkIn"] == "2025-12-01"
    assert response["reservation"]["checkOut"] == "2025-12-05"


@pytest.mark.asyncio
async def test_update_reservation_partial_preserves_fields():
    """Verify unchanged fields remain intact"""
    result = await handle_call_tool(
        "update_reservation",
        {"reservation_id": "test-reservation-1", "check_in": "2025-11-16"}
    )
    
    response = json.loads(result[0].text)
    assert response["success"] is True
    assert response["reservation"]["checkIn"] == "2025-11-16"
    # All other fields should be preserved
    assert response["reservation"]["checkOut"] == "2025-11-17"
    assert response["reservation"]["guestName"] == "John Doe"
    assert response["reservation"]["roomId"] == 1
    assert response["reservation"]["id"] == "test-reservation-1"
    assert response["reservation"]["createdAt"] == "2025-11-10T10:00:00"


@pytest.mark.asyncio
async def test_update_reservation_preserves_immutable_fields():
    """Ensure immutable fields never change"""
    original_id = "test-reservation-1"
    original_created = "2025-11-10T10:00:00"
    
    result = await handle_call_tool(
        "update_reservation",
        {
            "reservation_id": "test-reservation-1",
            "guest_name": "Updated Name",
            "room_id": 2,
            "check_in": "2025-12-01",
            "check_out": "2025-12-05"
        }
    )
    
    response = json.loads(result[0].text)
    assert response["success"] is True
    assert response["reservation"]["id"] == original_id
    assert response["reservation"]["createdAt"] == original_created


# ============================================================================
# 2. VALIDATION ERROR TESTS (8 tests)
# ============================================================================

@pytest.mark.asyncio
async def test_update_nonexistent_reservation():
    """Invalid reservation ID"""
    result = await handle_call_tool(
        "update_reservation",
        {"reservation_id": "nonexistent-id", "guest_name": "Test"}
    )
    
    response = json.loads(result[0].text)
    assert "error" in response
    assert "not found" in response["error"].lower()


@pytest.mark.asyncio
async def test_update_with_nonexistent_room():
    """Invalid room ID"""
    result = await handle_call_tool(
        "update_reservation",
        {"reservation_id": "test-reservation-1", "room_id": 999}
    )
    
    response = json.loads(result[0].text)
    assert "error" in response
    assert "room not found" in response["error"].lower()


@pytest.mark.asyncio
async def test_update_with_unavailable_room():
    """Room has 0 availability"""
    result = await handle_call_tool(
        "update_reservation",
        {"reservation_id": "test-reservation-1", "room_id": 3}
    )
    
    response = json.loads(result[0].text)
    assert "error" in response
    assert "not available" in response["error"].lower()


@pytest.mark.asyncio
async def test_update_with_invalid_date_format():
    """Malformed date strings"""
    result = await handle_call_tool(
        "update_reservation",
        {"reservation_id": "test-reservation-1", "check_in": "15-11-2025"}
    )
    
    response = json.loads(result[0].text)
    assert "error" in response
    assert "date format" in response["error"].lower()


@pytest.mark.asyncio
async def test_update_checkout_before_checkin():
    """Invalid date range"""
    result = await handle_call_tool(
        "update_reservation",
        {
            "reservation_id": "test-reservation-1",
            "check_in": "2025-11-20",
            "check_out": "2025-11-18"
        }
    )
    
    response = json.loads(result[0].text)
    assert "error" in response
    assert "after" in response["error"].lower()


@pytest.mark.asyncio
async def test_update_with_empty_guest_name():
    """Empty/whitespace name"""
    result = await handle_call_tool(
        "update_reservation",
        {"reservation_id": "test-reservation-1", "guest_name": "   "}
    )
    
    response = json.loads(result[0].text)
    assert "error" in response
    assert "empty" in response["error"].lower()


@pytest.mark.asyncio
async def test_update_with_no_update_fields():
    """Only reservation_id provided"""
    result = await handle_call_tool(
        "update_reservation",
        {"reservation_id": "test-reservation-1"}
    )
    
    response = json.loads(result[0].text)
    assert "error" in response
    assert "no valid fields" in response["error"].lower()


@pytest.mark.asyncio
async def test_update_with_same_room_id():
    """No availability change when room unchanged"""
    result = await handle_call_tool(
        "update_reservation",
        {"reservation_id": "test-reservation-1", "room_id": 1, "guest_name": "Updated"}
    )
    
    response = json.loads(result[0].text)
    assert response["success"] is True
    
    # Verify availability unchanged
    data = load_data()
    room1 = next(r for r in data['rooms'] if r['id'] == 1)
    assert room1['availability'] == 5  # Should be unchanged


# ============================================================================
# 3. ROOM AVAILABILITY TESTS (4 tests)
# ============================================================================

@pytest.mark.asyncio
async def test_update_room_availability_restored():
    """Old room +1, new room -1"""
    # Initial state: Room 1 has 5 available, Room 2 has 1 available
    result = await handle_call_tool(
        "update_reservation",
        {"reservation_id": "test-reservation-1", "room_id": 2}
    )
    
    response = json.loads(result[0].text)
    assert response["success"] is True
    
    data = load_data()
    room1 = next(r for r in data['rooms'] if r['id'] == 1)
    room2 = next(r for r in data['rooms'] if r['id'] == 2)
    
    assert room1['availability'] == 6
    assert room2['availability'] == 0


@pytest.mark.asyncio
async def test_update_room_availability_unchanged_same_room():
    """Same room = no change"""
    result = await handle_call_tool(
        "update_reservation",
        {"reservation_id": "test-reservation-1", "room_id": 1, "guest_name": "Updated Name"}
    )
    
    response = json.loads(result[0].text)
    assert response["success"] is True
    
    data = load_data()
    room1 = next(r for r in data['rooms'] if r['id'] == 1)
    assert room1['availability'] == 5  # Unchanged


@pytest.mark.asyncio
async def test_update_cannot_use_fully_booked_room():
    """Block unavailable rooms"""
    result = await handle_call_tool(
        "update_reservation",
        {"reservation_id": "test-reservation-1", "room_id": 3}
    )
    
    response = json.loads(result[0].text)
    assert "error" in response


@pytest.mark.asyncio
async def test_update_availability_consistent_on_error():
    """Rollback on validation failure"""
    # Try to update with invalid data
    result = await handle_call_tool(
        "update_reservation",
        {"reservation_id": "test-reservation-1", "room_id": 999}
    )
    
    response = json.loads(result[0].text)
    assert "error" in response
    
    # Verify availability unchanged
    data = load_data()
    room1 = next(r for r in data['rooms'] if r['id'] == 1)
    assert room1['availability'] == 5  # Should be unchanged


# ============================================================================
# 4. DATA INTEGRITY TESTS (4 tests)
# ============================================================================

@pytest.mark.asyncio
async def test_update_does_not_duplicate_reservation():
    """Modify, not create"""
    result = await handle_call_tool(
        "update_reservation",
        {"reservation_id": "test-reservation-1", "guest_name": "Updated Name"}
    )
    
    response = json.loads(result[0].text)
    assert response["success"] is True
    
    data = load_data()
    assert len(data['reservations']) == 1  # Still only one reservation


@pytest.mark.asyncio
async def test_update_persists_to_json():
    """Changes saved to data.json"""
    result = await handle_call_tool(
        "update_reservation",
        {"reservation_id": "test-reservation-1", "guest_name": "Persisted Name"}
    )
    
    response = json.loads(result[0].text)
    assert response["success"] is True
    
    # Read directly from file
    data = load_data()
    reservation = data['reservations'][0]
    assert reservation['guestName'] == "Persisted Name"


@pytest.mark.asyncio
async def test_update_reservation_id_never_changes():
    """UUID immutable"""
    original_id = "test-reservation-1"
    
    # Perform multiple updates
    await handle_call_tool(
        "update_reservation",
        {"reservation_id": "test-reservation-1", "guest_name": "First Update"}
    )
    
    result = await handle_call_tool(
        "update_reservation",
        {"reservation_id": "test-reservation-1", "guest_name": "Second Update"}
    )
    
    response = json.loads(result[0].text)
    assert response["success"] is True
    assert response["reservation"]["id"] == original_id


@pytest.mark.asyncio
async def test_update_created_at_never_changes():
    """Timestamp immutable"""
    original_created = "2025-11-10T10:00:00"
    
    result = await handle_call_tool(
        "update_reservation",
        {"reservation_id": "test-reservation-1", "guest_name": "Updated Name"}
    )
    
    response = json.loads(result[0].text)
    assert response["success"] is True
    assert response["reservation"]["createdAt"] == original_created


# ============================================================================
# 5. EDGE CASES (3 tests)
# ============================================================================

@pytest.mark.asyncio
async def test_update_with_special_characters_in_name():
    """Unicode, emojis"""
    special_name = "José García 🎉 O'Brien-Smith"
    result = await handle_call_tool(
        "update_reservation",
        {"reservation_id": "test-reservation-1", "guest_name": special_name}
    )
    
    response = json.loads(result[0].text)
    assert response["success"] is True
    assert response["reservation"]["guestName"] == special_name


@pytest.mark.asyncio
async def test_update_with_very_long_guest_name():
    """Test limits"""
    long_name = "A" * 500
    result = await handle_call_tool(
        "update_reservation",
        {"reservation_id": "test-reservation-1", "guest_name": long_name}
    )
    
    # Should succeed (no explicit length limit)
    response = json.loads(result[0].text)
    assert response["success"] is True
    assert response["reservation"]["guestName"] == long_name


@pytest.mark.asyncio
async def test_update_same_values_as_current():
    """No-op update succeeds"""
    result = await handle_call_tool(
        "update_reservation",
        {
            "reservation_id": "test-reservation-1",
            "guest_name": "John Doe",
            "room_id": 1,
            "check_in": "2025-11-15",
            "check_out": "2025-11-17"
        }
    )
    
    response = json.loads(result[0].text)
    assert response["success"] is True


# ============================================================================
# ADDITIONAL VALIDATION TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_update_checkout_only_validates_with_existing_checkin():
    """Updating only checkout should validate against existing checkin"""
    # Original: checkIn='2025-11-15', checkOut='2025-11-17'
    result = await handle_call_tool(
        "update_reservation",
        {"reservation_id": "test-reservation-1", "check_out": "2025-11-14"}
    )
    
    response = json.loads(result[0].text)
    assert "error" in response


@pytest.mark.asyncio
async def test_update_checkin_only_validates_with_existing_checkout():
    """Updating only checkin should validate against existing checkout"""
    # Original: checkIn='2025-11-15', checkOut='2025-11-17'
    result = await handle_call_tool(
        "update_reservation",
        {"reservation_id": "test-reservation-1", "check_in": "2025-11-18"}
    )
    
    response = json.loads(result[0].text)
    assert "error" in response

