from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from datetime import datetime

clients = Blueprint('clients', __name__)

@clients.route('/')
def list_clients():
    """Display all clients"""
    cursor = g.db.cursor()

    # Get all clients with their appointment count
    query = """
        SELECT c.*, COUNT(a.appt_id) as appt_count,
               MAX(a.appt_date) as last_visit
        FROM Clients c
        LEFT JOIN Appointments a ON c.client_id = a.client_id
        GROUP BY c.client_id
        ORDER BY c.name
    """

    cursor.execute(query)
    clients_list = cursor.fetchall()
    cursor.close()

    return render_template('clients/list.html', clients=clients_list)

@clients.route('/add', methods=['GET', 'POST'])
def add_client():
    """Add a new client"""
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        instagram = request.form.get('instagram')
        email = request.form.get('email')
        allergies = request.form.get('allergies')
        notes = request.form.get('notes')

        if not name or not phone:
            flash('Name and phone number are required!', 'error')
            return redirect(url_for('clients.add_client'))

        cursor = g.db.cursor()

        try:
            query = """
                INSERT INTO Clients (name, phone, instagram, email, allergies, notes)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (name, phone, instagram, email, allergies, notes))
            g.db.commit()

            # Create loyalty points entry for new client
            client_id = cursor.lastrowid
            cursor.execute("INSERT INTO LoyaltyPoints (client_id, points) VALUES (%s, 0)", (client_id,))
            g.db.commit()

            flash(f'Client {name} added successfully!', 'success')
            return redirect(url_for('clients.view_client', client_id=client_id))

        except Exception as e:
            g.db.rollback()
            flash(f'Error adding client: {str(e)}', 'error')

        finally:
            cursor.close()

    return render_template('clients/add.html')

@clients.route('/<int:client_id>')
def view_client(client_id):
    """View client details and appointment history"""
    cursor = g.db.cursor()

    # Get client information
    cursor.execute("SELECT * FROM Clients WHERE client_id = %s", (client_id,))
    client = cursor.fetchone()

    if not client:
        flash('Client not found!', 'error')
        return redirect(url_for('clients.list_clients'))

    # Get appointment history
    query = """
        SELECT a.*, s.name as service_name
        FROM Appointments a
        JOIN Services s ON a.service_id = s.service_id
        WHERE a.client_id = %s
        ORDER BY a.appt_date DESC, a.appt_time DESC
    """
    cursor.execute(query, (client_id,))
    appointments = cursor.fetchall()

    # Get loyalty points
    cursor.execute("SELECT points, lifetime_points FROM LoyaltyPoints WHERE client_id = %s", (client_id,))
    loyalty = cursor.fetchone()

    # Calculate statistics
    cursor.execute("""
        SELECT COUNT(*) as total_visits,
               SUM(price) as total_spent,
               AVG(price) as avg_spent
        FROM Appointments
        WHERE client_id = %s AND status = 'completed'
    """, (client_id,))
    stats = cursor.fetchone()

    cursor.close()

    return render_template('clients/view.html',
                          client=client,
                          appointments=appointments,
                          loyalty=loyalty,
                          stats=stats)

@clients.route('/<int:client_id>/edit', methods=['GET', 'POST'])
def edit_client(client_id):
    """Edit client information"""
    cursor = g.db.cursor()

    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        instagram = request.form.get('instagram')
        email = request.form.get('email')
        allergies = request.form.get('allergies')
        notes = request.form.get('notes')

        if not name or not phone:
            flash('Name and phone number are required!', 'error')
            return redirect(url_for('clients.edit_client', client_id=client_id))

        try:
            query = """
                UPDATE Clients
                SET name = %s, phone = %s, instagram = %s,
                    email = %s, allergies = %s, notes = %s
                WHERE client_id = %s
            """
            cursor.execute(query, (name, phone, instagram, email, allergies, notes, client_id))
            g.db.commit()
            flash(f'Client {name} updated successfully!', 'success')
            return redirect(url_for('clients.view_client', client_id=client_id))

        except Exception as e:
            g.db.rollback()
            flash(f'Error updating client: {str(e)}', 'error')

        finally:
            cursor.close()

    # GET request - show form
    cursor.execute("SELECT * FROM Clients WHERE client_id = %s", (client_id,))
    client = cursor.fetchone()
    cursor.close()

    if not client:
        flash('Client not found!', 'error')
        return redirect(url_for('clients.list_clients'))

    return render_template('clients/edit.html', client=client)

@clients.route('/<int:client_id>/delete', methods=['POST'])
def delete_client(client_id):
    """Delete a client (soft delete by marking inactive)"""
    cursor = g.db.cursor()

    try:
        # Check if client has any appointments
        cursor.execute("""
            SELECT COUNT(*) as count FROM Appointments
            WHERE client_id = %s AND status IN ('scheduled', 'confirmed')
        """, (client_id,))
        result = cursor.fetchone()

        if result['count'] > 0:
            flash('Cannot delete client with upcoming appointments!', 'error')
            return redirect(url_for('clients.view_client', client_id=client_id))

        # Delete client
        cursor.execute("DELETE FROM Clients WHERE client_id = %s", (client_id,))
        g.db.commit()
        flash('Client deleted successfully!', 'success')
        return redirect(url_for('clients.list_clients'))

    except Exception as e:
        g.db.rollback()
        flash(f'Error deleting client: {str(e)}', 'error')
        return redirect(url_for('clients.view_client', client_id=client_id))

    finally:
        cursor.close()
