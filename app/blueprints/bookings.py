from flask import Blueprint, render_template, request, redirect, url_for, flash, g, jsonify
from datetime import datetime, timedelta, time

bookings = Blueprint('bookings', __name__)

@bookings.route('/')
def calendar():
    """Display booking calendar"""
    cursor = g.db.cursor()

    # Get current month or requested month
    month = request.args.get('month', datetime.now().strftime('%Y-%m'))
    year, month_num = map(int, month.split('-'))

    # Get appointments for the month
    start_date = f"{year}-{month_num:02d}-01"
    if month_num == 12:
        end_date = f"{year+1}-01-01"
    else:
        end_date = f"{year}-{month_num+1:02d}-01"

    query = """
        SELECT a.*, c.name as client_name, s.name as service_name, s.avg_duration
        FROM Appointments a
        JOIN Clients c ON a.client_id = c.client_id
        JOIN Services s ON a.service_id = s.service_id
        WHERE a.appt_date >= %s AND a.appt_date < %s
        ORDER BY a.appt_date, a.appt_time
    """
    cursor.execute(query, (start_date, end_date))
    appointments = cursor.fetchall()

    cursor.close()

    return render_template('bookings/calendar.html',
                          appointments=appointments,
                          current_month=month)

@bookings.route('/book', methods=['GET', 'POST'])
def book_appointment():
    """Book a new appointment"""
    cursor = g.db.cursor()

    if request.method == 'POST':
        client_id = request.form.get('client_id')
        service_id = request.form.get('service_id')
        appt_date = request.form.get('appt_date')
        appt_time = request.form.get('appt_time')
        notes = request.form.get('notes')
        price = request.form.get('price')

        if not all([client_id, service_id, appt_date, appt_time, price]):
            flash('All fields are required!', 'error')
            return redirect(url_for('bookings.book_appointment'))

        # Check if time slot is available
        cursor.execute("""
            SELECT COUNT(*) as count
            FROM Appointments
            WHERE appt_date = %s AND appt_time = %s AND status != 'cancelled'
        """, (appt_date, appt_time))
        result = cursor.fetchone()

        if result['count'] > 0:
            flash('This time slot is already booked!', 'error')
            return redirect(url_for('bookings.book_appointment'))

        try:
            query = """
                INSERT INTO Appointments
                (client_id, service_id, appt_date, appt_time, price, status, notes)
                VALUES (%s, %s, %s, %s, %s, 'scheduled', %s)
            """
            cursor.execute(query, (client_id, service_id, appt_date, appt_time, price, notes))
            g.db.commit()

            flash('Appointment booked successfully!', 'success')
            return redirect(url_for('bookings.calendar'))

        except Exception as e:
            g.db.rollback()
            flash(f'Error booking appointment: {str(e)}', 'error')

        finally:
            cursor.close()

    # GET request - show booking form
    # Get all clients
    cursor.execute("SELECT client_id, name, phone FROM Clients ORDER BY name")
    clients = cursor.fetchall()

    # Get all active services
    cursor.execute("SELECT * FROM Services WHERE is_active = 1 ORDER BY name")
    services = cursor.fetchall()

    cursor.close()

    # Get suggested date (next available weekday)
    suggested_date = datetime.now() + timedelta(days=1)
    while suggested_date.weekday() >= 5:  # Skip weekends
        suggested_date += timedelta(days=1)

    return render_template('bookings/book.html',
                          clients=clients,
                          services=services,
                          suggested_date=suggested_date.strftime('%Y-%m-%d'))

@bookings.route('/<int:appt_id>/edit', methods=['GET', 'POST'])
def edit_appointment(appt_id):
    """Edit an existing appointment"""
    cursor = g.db.cursor()

    if request.method == 'POST':
        service_id = request.form.get('service_id')
        appt_date = request.form.get('appt_date')
        appt_time = request.form.get('appt_time')
        price = request.form.get('price')
        status = request.form.get('status')
        notes = request.form.get('notes')
        product_cost = request.form.get('product_cost', 0)

        try:
            query = """
                UPDATE Appointments
                SET service_id = %s, appt_date = %s, appt_time = %s,
                    price = %s, status = %s, notes = %s, product_cost = %s
                WHERE appt_id = %s
            """
            cursor.execute(query, (service_id, appt_date, appt_time, price,
                                 status, notes, product_cost, appt_id))
            g.db.commit()

            # Update loyalty points if appointment completed
            if status == 'completed':
                cursor.execute("SELECT client_id FROM Appointments WHERE appt_id = %s", (appt_id,))
                result = cursor.fetchone()
                if result:
                    points = int(float(price) / 10)  # 1 point per $10 spent
                    cursor.execute("""
                        UPDATE LoyaltyPoints
                        SET points = points + %s,
                            lifetime_points = lifetime_points + %s,
                            last_earned = NOW()
                        WHERE client_id = %s
                    """, (points, points, result['client_id']))
                    g.db.commit()

            flash('Appointment updated successfully!', 'success')
            return redirect(url_for('bookings.view_appointment', appt_id=appt_id))

        except Exception as e:
            g.db.rollback()
            flash(f'Error updating appointment: {str(e)}', 'error')

        finally:
            cursor.close()

    # GET request
    query = """
        SELECT a.*, c.name as client_name, c.phone, s.name as service_name
        FROM Appointments a
        JOIN Clients c ON a.client_id = c.client_id
        JOIN Services s ON a.service_id = s.service_id
        WHERE a.appt_id = %s
    """
    cursor.execute(query, (appt_id,))
    appointment = cursor.fetchone()

    if not appointment:
        flash('Appointment not found!', 'error')
        return redirect(url_for('bookings.calendar'))

    # Get all services
    cursor.execute("SELECT * FROM Services WHERE is_active = 1 ORDER BY name")
    services = cursor.fetchall()

    cursor.close()

    return render_template('bookings/edit.html',
                          appointment=appointment,
                          services=services)

@bookings.route('/<int:appt_id>')
def view_appointment(appt_id):
    """View appointment details"""
    cursor = g.db.cursor()

    query = """
        SELECT a.*, c.name as client_name, c.phone, c.email, c.allergies,
               s.name as service_name, s.avg_duration
        FROM Appointments a
        JOIN Clients c ON a.client_id = c.client_id
        JOIN Services s ON a.service_id = s.service_id
        WHERE a.appt_id = %s
    """
    cursor.execute(query, (appt_id,))
    appointment = cursor.fetchone()

    cursor.close()

    if not appointment:
        flash('Appointment not found!', 'error')
        return redirect(url_for('bookings.calendar'))

    return render_template('bookings/view.html', appointment=appointment)

@bookings.route('/<int:appt_id>/cancel', methods=['POST'])
def cancel_appointment(appt_id):
    """Cancel an appointment"""
    cursor = g.db.cursor()

    try:
        cursor.execute("""
            UPDATE Appointments
            SET status = 'cancelled'
            WHERE appt_id = %s
        """, (appt_id,))
        g.db.commit()
        flash('Appointment cancelled successfully!', 'success')

    except Exception as e:
        g.db.rollback()
        flash(f'Error cancelling appointment: {str(e)}', 'error')

    finally:
        cursor.close()

    return redirect(url_for('bookings.calendar'))

@bookings.route('/available-times')
def available_times():
    """API endpoint to get available time slots for a date"""
    date = request.args.get('date')

    if not date:
        return jsonify({'error': 'Date required'}), 400

    cursor = g.db.cursor()

    # Get booked times for the date
    cursor.execute("""
        SELECT appt_time FROM Appointments
        WHERE appt_date = %s AND status != 'cancelled'
    """, (date,))
    booked = cursor.fetchall()
    cursor.close()

    booked_times = [b['appt_time'].strftime('%H:%M') if b['appt_time'] else '' for b in booked]

    # Generate all possible time slots (9 AM to 6 PM, every 30 minutes)
    available = []
    start_time = time(9, 0)
    end_time = time(18, 0)
    current = datetime.combine(datetime.today(), start_time)
    end = datetime.combine(datetime.today(), end_time)

    while current <= end:
        time_str = current.strftime('%H:%M')
        if time_str not in booked_times:
            available.append({
                'time': time_str,
                'display': current.strftime('%I:%M %p')
            })
        current += timedelta(minutes=30)

    return jsonify({'available_times': available})
