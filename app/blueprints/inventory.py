from flask import Blueprint, render_template, request, redirect, url_for, flash, g

inventory = Blueprint('inventory', __name__)

@inventory.route('/')
def list_inventory():
    """Display all inventory items with low-stock alerts"""
    cursor = g.db.cursor()

    # Get all inventory items
    query = """
        SELECT *,
               CASE
                   WHEN quantity <= low_stock_threshold THEN 1
                   ELSE 0
               END as is_low_stock
        FROM Inventory
        ORDER BY
            CASE WHEN quantity <= low_stock_threshold THEN 0 ELSE 1 END,
            name
    """
    cursor.execute(query)
    items = cursor.fetchall()

    # Count low stock items
    low_stock_count = sum(1 for item in items if item['is_low_stock'])

    # Calculate total inventory value
    cursor.execute("SELECT SUM(quantity * unit_cost) as total_value FROM Inventory")
    result = cursor.fetchone()
    total_value = result['total_value'] or 0

    cursor.close()

    return render_template('inventory/list.html',
                          items=items,
                          low_stock_count=low_stock_count,
                          total_value=total_value)

@inventory.route('/add', methods=['GET', 'POST'])
def add_item():
    """Add a new inventory item"""
    if request.method == 'POST':
        name = request.form.get('name')
        quantity = request.form.get('quantity')
        unit = request.form.get('unit')
        unit_cost = request.form.get('unit_cost')
        supplier = request.form.get('supplier')
        low_stock_threshold = request.form.get('low_stock_threshold')
        category = request.form.get('category')

        if not all([name, quantity, unit, unit_cost]):
            flash('Name, quantity, unit, and unit cost are required!', 'error')
            return redirect(url_for('inventory.add_item'))

        cursor = g.db.cursor()

        try:
            query = """
                INSERT INTO Inventory
                (name, quantity, unit, unit_cost, supplier, low_stock_threshold, category)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (name, quantity, unit, unit_cost, supplier,
                                 low_stock_threshold, category))
            g.db.commit()
            flash(f'Inventory item "{name}" added successfully!', 'success')
            return redirect(url_for('inventory.list_inventory'))

        except Exception as e:
            g.db.rollback()
            flash(f'Error adding item: {str(e)}', 'error')

        finally:
            cursor.close()

    return render_template('inventory/add.html')

@inventory.route('/<int:item_id>/edit', methods=['GET', 'POST'])
def edit_item(item_id):
    """Edit an inventory item"""
    cursor = g.db.cursor()

    if request.method == 'POST':
        name = request.form.get('name')
        quantity = request.form.get('quantity')
        unit = request.form.get('unit')
        unit_cost = request.form.get('unit_cost')
        supplier = request.form.get('supplier')
        low_stock_threshold = request.form.get('low_stock_threshold')
        category = request.form.get('category')

        try:
            query = """
                UPDATE Inventory
                SET name = %s, quantity = %s, unit = %s, unit_cost = %s,
                    supplier = %s, low_stock_threshold = %s, category = %s
                WHERE item_id = %s
            """
            cursor.execute(query, (name, quantity, unit, unit_cost, supplier,
                                 low_stock_threshold, category, item_id))
            g.db.commit()
            flash(f'Item "{name}" updated successfully!', 'success')
            return redirect(url_for('inventory.list_inventory'))

        except Exception as e:
            g.db.rollback()
            flash(f'Error updating item: {str(e)}', 'error')

        finally:
            cursor.close()

    # GET request
    cursor.execute("SELECT * FROM Inventory WHERE item_id = %s", (item_id,))
    item = cursor.fetchone()
    cursor.close()

    if not item:
        flash('Item not found!', 'error')
        return redirect(url_for('inventory.list_inventory'))

    return render_template('inventory/edit.html', item=item)

@inventory.route('/<int:item_id>/adjust', methods=['POST'])
def adjust_quantity(item_id):
    """Adjust inventory quantity (add or subtract)"""
    adjustment = request.form.get('adjustment')
    reason = request.form.get('reason', 'Manual adjustment')

    if not adjustment:
        flash('Adjustment amount is required!', 'error')
        return redirect(url_for('inventory.list_inventory'))

    cursor = g.db.cursor()

    try:
        adjustment = float(adjustment)

        # Update quantity
        cursor.execute("""
            UPDATE Inventory
            SET quantity = quantity + %s
            WHERE item_id = %s
        """, (adjustment, item_id))

        g.db.commit()

        if adjustment > 0:
            flash(f'Added {adjustment} units to inventory', 'success')
        else:
            flash(f'Removed {abs(adjustment)} units from inventory', 'success')

    except Exception as e:
        g.db.rollback()
        flash(f'Error adjusting inventory: {str(e)}', 'error')

    finally:
        cursor.close()

    return redirect(url_for('inventory.list_inventory'))

@inventory.route('/<int:item_id>/delete', methods=['POST'])
def delete_item(item_id):
    """Delete an inventory item"""
    cursor = g.db.cursor()

    try:
        # Check if item is linked to services
        cursor.execute("""
            SELECT COUNT(*) as count FROM ServiceItems WHERE item_id = %s
        """, (item_id,))
        result = cursor.fetchone()

        if result['count'] > 0:
            flash('Cannot delete item that is linked to services!', 'error')
            return redirect(url_for('inventory.list_inventory'))

        cursor.execute("DELETE FROM Inventory WHERE item_id = %s", (item_id,))
        g.db.commit()
        flash('Item deleted successfully!', 'success')

    except Exception as e:
        g.db.rollback()
        flash(f'Error deleting item: {str(e)}', 'error')

    finally:
        cursor.close()

    return redirect(url_for('inventory.list_inventory'))

@inventory.route('/low-stock')
def low_stock():
    """Show only low stock items"""
    cursor = g.db.cursor()

    query = """
        SELECT * FROM Inventory
        WHERE quantity <= low_stock_threshold
        ORDER BY (quantity / NULLIF(low_stock_threshold, 0)) ASC
    """
    cursor.execute(query)
    items = cursor.fetchall()

    cursor.close()

    return render_template('inventory/low_stock.html', items=items)

@inventory.route('/service-usage')
def service_usage():
    """Show inventory usage by service"""
    cursor = g.db.cursor()

    query = """
        SELECT s.name as service_name, i.name as item_name,
               si.quantity_used, i.unit, i.unit_cost,
               (si.quantity_used * i.unit_cost) as cost_per_service
        FROM ServiceItems si
        JOIN Services s ON si.service_id = s.service_id
        JOIN Inventory i ON si.item_id = i.item_id
        ORDER BY s.name, i.name
    """
    cursor.execute(query)
    usage = cursor.fetchall()

    cursor.close()

    return render_template('inventory/service_usage.html', usage=usage)
