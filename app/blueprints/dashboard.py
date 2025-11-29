from flask import Blueprint, render_template, request, g, jsonify
from datetime import datetime, timedelta
import calendar

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
def index():
    """Main dashboard with analytics overview"""
    cursor = g.db.cursor()

    # Get current month/year
    now = datetime.now()
    current_month = now.strftime('%Y-%m')

    # --- Key Metrics ---

    # Total revenue (completed appointments)
    cursor.execute("""
        SELECT SUM(price) as total_revenue,
               SUM(product_cost) as total_costs,
               SUM(profit) as total_profit
        FROM Appointments
        WHERE status = 'completed'
    """)
    revenue_data = cursor.fetchone()

    # This month's revenue
    cursor.execute("""
        SELECT SUM(price) as month_revenue,
               COUNT(*) as month_appts,
               SUM(profit) as month_profit
        FROM Appointments
        WHERE status = 'completed'
          AND DATE_FORMAT(appt_date, '%%Y-%%m') = %s
    """, (current_month,))
    month_data = cursor.fetchone()

    # Total clients
    cursor.execute("SELECT COUNT(*) as total_clients FROM Clients")
    client_count = cursor.fetchone()['total_clients']

    # Upcoming appointments
    cursor.execute("""
        SELECT COUNT(*) as upcoming
        FROM Appointments
        WHERE appt_date >= CURDATE()
          AND status IN ('scheduled', 'confirmed')
    """)
    upcoming_count = cursor.fetchone()['upcoming']

    # Low stock items
    cursor.execute("""
        SELECT COUNT(*) as low_stock
        FROM Inventory
        WHERE quantity <= low_stock_threshold
    """)
    low_stock_count = cursor.fetchone()['low_stock']

    # --- Top Services ---
    cursor.execute("""
        SELECT s.name, COUNT(*) as bookings, SUM(a.price) as revenue
        FROM Appointments a
        JOIN Services s ON a.service_id = s.service_id
        WHERE a.status = 'completed'
        GROUP BY s.service_id
        ORDER BY bookings DESC
        LIMIT 5
    """)
    top_services = cursor.fetchall()

    # --- Top Clients ---
    cursor.execute("""
        SELECT c.name, COUNT(*) as visits, SUM(a.price) as total_spent
        FROM Appointments a
        JOIN Clients c ON a.client_id = c.client_id
        WHERE a.status = 'completed'
        GROUP BY c.client_id
        ORDER BY total_spent DESC
        LIMIT 5
    """)
    top_clients = cursor.fetchall()

    # --- Revenue trend (last 6 months) ---
    six_months_ago = now - timedelta(days=180)
    cursor.execute("""
        SELECT DATE_FORMAT(appt_date, '%%Y-%%m') as month,
               SUM(price) as revenue,
               SUM(profit) as profit,
               COUNT(*) as appointments
        FROM Appointments
        WHERE status = 'completed'
          AND appt_date >= %s
        GROUP BY month
        ORDER BY month
    """, (six_months_ago,))
    revenue_trend = cursor.fetchall()

    # --- Recent activity ---
    cursor.execute("""
        SELECT a.*, c.name as client_name, s.name as service_name
        FROM Appointments a
        JOIN Clients c ON a.client_id = c.client_id
        JOIN Services s ON a.service_id = s.service_id
        ORDER BY a.created_at DESC
        LIMIT 10
    """)
    recent_activity = cursor.fetchall()

    cursor.close()

    return render_template('dashboard/index.html',
                          revenue_data=revenue_data,
                          month_data=month_data,
                          client_count=client_count,
                          upcoming_count=upcoming_count,
                          low_stock_count=low_stock_count,
                          top_services=top_services,
                          top_clients=top_clients,
                          revenue_trend=revenue_trend,
                          recent_activity=recent_activity)

@dashboard.route('/revenue-analysis')
def revenue_analysis():
    """Detailed revenue analysis"""
    cursor = g.db.cursor()

    # Monthly revenue breakdown
    cursor.execute("""
        SELECT DATE_FORMAT(appt_date, '%%Y-%%m') as month,
               COUNT(*) as appointments,
               SUM(price) as revenue,
               SUM(product_cost) as costs,
               SUM(profit) as profit,
               AVG(price) as avg_price
        FROM Appointments
        WHERE status = 'completed'
        GROUP BY month
        ORDER BY month DESC
        LIMIT 12
    """)
    monthly_data = cursor.fetchall()

    # Service profitability
    cursor.execute("""
        SELECT s.name,
               COUNT(*) as times_booked,
               SUM(a.price) as total_revenue,
               SUM(a.product_cost) as total_cost,
               SUM(a.profit) as total_profit,
               AVG(a.price) as avg_price,
               AVG(a.profit) as avg_profit
        FROM Appointments a
        JOIN Services s ON a.service_id = s.service_id
        WHERE a.status = 'completed'
        GROUP BY s.service_id
        ORDER BY total_profit DESC
    """)
    service_profitability = cursor.fetchall()

    cursor.close()

    return render_template('dashboard/revenue_analysis.html',
                          monthly_data=monthly_data,
                          service_profitability=service_profitability)

@dashboard.route('/client-analytics')
def client_analytics():
    """Client behavior and analytics"""
    cursor = g.db.cursor()

    # Client lifetime value
    cursor.execute("""
        SELECT c.name, c.phone,
               COUNT(a.appt_id) as total_visits,
               SUM(a.price) as lifetime_value,
               AVG(a.price) as avg_spend,
               MAX(a.appt_date) as last_visit,
               DATEDIFF(CURDATE(), MAX(a.appt_date)) as days_since_visit
        FROM Clients c
        LEFT JOIN Appointments a ON c.client_id = a.client_id AND a.status = 'completed'
        GROUP BY c.client_id
        HAVING total_visits > 0
        ORDER BY lifetime_value DESC
    """)
    client_ltv = cursor.fetchall()

    # New clients by month
    cursor.execute("""
        SELECT DATE_FORMAT(created_at, '%%Y-%%m') as month,
               COUNT(*) as new_clients
        FROM Clients
        GROUP BY month
        ORDER BY month DESC
        LIMIT 12
    """)
    new_clients = cursor.fetchall()

    # Client retention (clients who visited in last 90 days)
    cursor.execute("""
        SELECT COUNT(DISTINCT client_id) as active_clients
        FROM Appointments
        WHERE appt_date >= DATE_SUB(CURDATE(), INTERVAL 90 DAY)
          AND status = 'completed'
    """)
    active_clients = cursor.fetchone()['active_clients']

    cursor.close()

    return render_template('dashboard/client_analytics.html',
                          client_ltv=client_ltv,
                          new_clients=new_clients,
                          active_clients=active_clients)
