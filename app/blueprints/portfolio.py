from flask import Blueprint, render_template, request, redirect, url_for, flash, g

portfolio = Blueprint('portfolio', __name__)

@portfolio.route('/')
def gallery():
    """Display portfolio gallery"""
    cursor = g.db.cursor()

    # Get filter parameters
    tag_filter = request.args.get('tag')

    if tag_filter:
        query = """
            SELECT DISTINCT p.*, GROUP_CONCAT(t.name SEPARATOR ', ') as tags
            FROM PortfolioPhotos p
            LEFT JOIN PhotoTags pt ON p.photo_id = pt.photo_id
            LEFT JOIN Tags t ON pt.tag_id = t.tag_id
            WHERE p.photo_id IN (
                SELECT photo_id FROM PhotoTags pt2
                JOIN Tags t2 ON pt2.tag_id = t2.tag_id
                WHERE t2.name = %s
            )
            GROUP BY p.photo_id
            ORDER BY p.created_at DESC
        """
        cursor.execute(query, (tag_filter,))
    else:
        query = """
            SELECT p.*, GROUP_CONCAT(t.name SEPARATOR ', ') as tags
            FROM PortfolioPhotos p
            LEFT JOIN PhotoTags pt ON p.photo_id = pt.photo_id
            LEFT JOIN Tags t ON pt.tag_id = t.tag_id
            GROUP BY p.photo_id
            ORDER BY p.created_at DESC
        """
        cursor.execute(query)

    photos = cursor.fetchall()

    # Get all tags for filter
    cursor.execute("SELECT * FROM Tags ORDER BY name")
    all_tags = cursor.fetchall()

    cursor.close()

    return render_template('portfolio/gallery.html',
                          photos=photos,
                          all_tags=all_tags,
                          current_tag=tag_filter)

@portfolio.route('/add', methods=['GET', 'POST'])
def add_photo():
    """Add a new portfolio photo"""
    cursor = g.db.cursor()

    if request.method == 'POST':
        image_url = request.form.get('image_url')
        title = request.form.get('title')
        description = request.form.get('description')
        appt_id = request.form.get('appt_id')
        tags = request.form.getlist('tags')

        if not image_url:
            flash('Image URL is required!', 'error')
            return redirect(url_for('portfolio.add_photo'))

        try:
            # Insert photo
            query = """
                INSERT INTO PortfolioPhotos (image_url, title, description, appt_id)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (image_url, title, description, appt_id if appt_id else None))
            photo_id = cursor.lastrowid

            # Add tags
            if tags:
                for tag_id in tags:
                    cursor.execute("""
                        INSERT INTO PhotoTags (photo_id, tag_id) VALUES (%s, %s)
                    """, (photo_id, tag_id))

            g.db.commit()
            flash('Photo added to portfolio successfully!', 'success')
            return redirect(url_for('portfolio.gallery'))

        except Exception as e:
            g.db.rollback()
            flash(f'Error adding photo: {str(e)}', 'error')

        finally:
            cursor.close()

    # GET - show form
    cursor.execute("SELECT * FROM Tags ORDER BY category, name")
    tags = cursor.fetchall()

    cursor.execute("""
        SELECT a.appt_id, c.name as client_name, a.appt_date, s.name as service_name
        FROM Appointments a
        JOIN Clients c ON a.client_id = c.client_id
        JOIN Services s ON a.service_id = s.service_id
        WHERE a.status = 'completed'
        ORDER BY a.appt_date DESC
        LIMIT 50
    """)
    appointments = cursor.fetchall()

    cursor.close()

    return render_template('portfolio/add.html', tags=tags, appointments=appointments)

@portfolio.route('/<int:photo_id>')
def view_photo(photo_id):
    """View single photo details"""
    cursor = g.db.cursor()

    query = """
        SELECT p.*, GROUP_CONCAT(t.name SEPARATOR ', ') as tags
        FROM PortfolioPhotos p
        LEFT JOIN PhotoTags pt ON p.photo_id = pt.photo_id
        LEFT JOIN Tags t ON pt.tag_id = t.tag_id
        WHERE p.photo_id = %s
        GROUP BY p.photo_id
    """
    cursor.execute(query, (photo_id,))
    photo = cursor.fetchone()

    if not photo:
        flash('Photo not found!', 'error')
        return redirect(url_for('portfolio.gallery'))

    # Get appointment details if linked
    appointment = None
    if photo['appt_id']:
        cursor.execute("""
            SELECT a.*, c.name as client_name, s.name as service_name
            FROM Appointments a
            JOIN Clients c ON a.client_id = c.client_id
            JOIN Services s ON a.service_id = s.service_id
            WHERE a.appt_id = %s
        """, (photo['appt_id'],))
        appointment = cursor.fetchone()

    cursor.close()

    return render_template('portfolio/view.html', photo=photo, appointment=appointment)

@portfolio.route('/<int:photo_id>/delete', methods=['POST'])
def delete_photo(photo_id):
    """Delete a portfolio photo"""
    cursor = g.db.cursor()

    try:
        cursor.execute("DELETE FROM PortfolioPhotos WHERE photo_id = %s", (photo_id,))
        g.db.commit()
        flash('Photo deleted successfully!', 'success')

    except Exception as e:
        g.db.rollback()
        flash(f'Error deleting photo: {str(e)}', 'error')

    finally:
        cursor.close()

    return redirect(url_for('portfolio.gallery'))
