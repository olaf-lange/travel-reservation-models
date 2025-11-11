const { createApp } = Vue;

createApp({
    data() {
        return {
            currentView: 'rooms',
            rooms: [],
            reservations: [],
            loading: false,
            error: null,
            showModal: false,
            selectedRoom: null,
            bookingForm: {
                guestName: '',
                checkIn: '',
                checkOut: ''
            },
            bookingError: null,
            submitting: false,
            today: new Date().toISOString().split('T')[0]
        };
    },
    mounted() {
        this.loadRooms();
        this.loadReservations();
    },
    methods: {
        async loadRooms() {
            this.loading = true;
            this.error = null;
            try {
                const response = await fetch('/api/rooms');
                if (!response.ok) throw new Error('Failed to load rooms');
                this.rooms = await response.json();
            } catch (err) {
                this.error = err.message;
                console.error('Error loading rooms:', err);
            } finally {
                this.loading = false;
            }
        },
        
        async loadReservations() {
            this.loading = true;
            this.error = null;
            try {
                const response = await fetch('/api/reservations');
                if (!response.ok) throw new Error('Failed to load reservations');
                this.reservations = await response.json();
            } catch (err) {
                this.error = err.message;
                console.error('Error loading reservations:', err);
            } finally {
                this.loading = false;
            }
        },
        
        selectRoom(room) {
            this.selectedRoom = room;
            this.showModal = true;
            this.bookingError = null;
            // Reset form
            this.bookingForm = {
                guestName: '',
                checkIn: '',
                checkOut: ''
            };
        },
        
        closeModal() {
            this.showModal = false;
            this.selectedRoom = null;
            this.bookingError = null;
        },
        
        async submitBooking() {
            if (!this.selectedRoom) return;
            
            // Validate dates
            if (this.bookingForm.checkOut <= this.bookingForm.checkIn) {
                this.bookingError = 'Check-out date must be after check-in date';
                return;
            }
            
            this.submitting = true;
            this.bookingError = null;
            
            try {
                const response = await fetch('/api/reservations', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        roomId: this.selectedRoom.id,
                        guestName: this.bookingForm.guestName,
                        checkIn: this.bookingForm.checkIn,
                        checkOut: this.bookingForm.checkOut
                    })
                });
                
                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.error || 'Failed to create reservation');
                }
                
                // Reload data
                await this.loadRooms();
                await this.loadReservations();
                
                // Close modal and show success
                this.closeModal();
                this.currentView = 'reservations';
                
            } catch (err) {
                this.bookingError = err.message;
                console.error('Error creating reservation:', err);
            } finally {
                this.submitting = false;
            }
        },
        
        async cancelReservation(reservationId) {
            if (!confirm('Are you sure you want to cancel this reservation?')) {
                return;
            }
            
            try {
                const response = await fetch(`/api/reservations/${reservationId}`, {
                    method: 'DELETE'
                });
                
                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.error || 'Failed to cancel reservation');
                }
                
                // Reload data
                await this.loadRooms();
                await this.loadReservations();
                
            } catch (err) {
                alert('Error cancelling reservation: ' + err.message);
                console.error('Error cancelling reservation:', err);
            }
        },
        
        getRoomName(roomId) {
            const room = this.rooms.find(r => r.id === roomId);
            return room ? room.name : 'Unknown Room';
        },
        
        formatDate(dateString) {
            const date = new Date(dateString);
            return date.toLocaleDateString('en-US', { 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric' 
            });
        }
    }
}).mount('#app');
