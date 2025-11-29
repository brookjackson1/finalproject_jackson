# NailsbyBrookJ - Professional Nail Business Management System

A comprehensive business management and booking platform for independent nail businesses, built with Flask and MySQL.

## Project Overview

NailsbyBrookJ is a full-featured web application designed to streamline nail salon operations, enhance client experience, and provide data-driven business insights. The platform combines appointment booking, client management, inventory tracking, and analytics in one elegant solution.

## Features Implemented

### 1. Client Management System
- Add, view, edit, and delete client profiles
- Track contact information, preferences, and allergies
- View complete appointment history per client
- Client statistics (total visits, lifetime value)
- Integrated loyalty points tracking

### 2. Appointment Booking System
- Interactive calendar view for all appointments
- Real-time availability checking
- Service selection with pricing
- Status tracking (scheduled, confirmed, completed, cancelled, no-show)
- Profitability tracking with product cost calculations

### 3. Inventory Management
- Track supplies with quantity, unit, and cost
- Automated low-stock alerts with priority levels
- Category organization and supplier tracking
- Quick inventory adjustments
- Total inventory valuation

### 4. Business Analytics Dashboard
- Revenue trends with Chart.js visualizations
- Top services and top clients analysis
- Monthly profitability tracking
- Recent activity feed
- Key performance indicators

### 5. Portfolio Gallery
- Showcase completed nail designs
- Tag-based filtering (22+ tags)
- Search by style, color, season, occasion
- Link photos to appointments
- Trend analysis capabilities

### 6. Loyalty Rewards System
- Automatic point accrual (1 point per $10)
- Lifetime points tracking
- Integration with client profiles

### 7. AI-Powered Style Assistant (NEW!)
- **Groq API integration** for lightning-fast AI responses
- Natural conversation about services, pricing, and nail care
- **Smart style suggestions** based on occasion, season, and color preferences
- Context-aware responses using live business data
- Quick suggestion buttons for common questions
- Beautiful chat interface with typing indicators

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: MySQL / JawsDB
- **AI Integration**: Groq API (LLaMA 3 70B model)
- **Frontend**: Bootstrap 5, Font Awesome, Chart.js
- **Deployment**: Heroku-ready with gunicorn

## Installation

1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
4. Install dependencies: `pip install -r requirements.txt`
5. Configure `.env` with database credentials and Groq API key:
   ```
   DB_HOST=your_host
   DB_USER=your_user
   DB_PASSWORD=your_password
   DB_PORT=3306
   DB_NAME=your_database
   GROQ_API_KEY=your_groq_api_key
   ```
6. Initialize database: `python init_db.py`
7. Run: `python app.py`

## Database Schema

9 interconnected tables:
- Clients, Services, Appointments
- Inventory, ServiceItems
- PortfolioPhotos, Tags, PhotoTags
- LoyaltyPoints

## Author

Brook Jackson
Georgia College & State University
MIS Program - Final Project
