# McDonald's Order Management System

This project implements a McDonald's order management system with automated cooking bots as described in the assignment.

## Project Structure

- **Frontend**: Vue 3 with TypeScript
- **Backend**: Python with Flask

## Features

1. Create normal and VIP orders
2. VIP orders are prioritized over normal orders
3. Add and remove cooking bots
4. Each bot processes one order at a time (10 seconds per order)
5. Orders move from PENDING to COMPLETE after processing

## Setup Instructions

### Backend Setup

1. Make sure you have Python installed (Python 3.6 or higher)
2. Navigate to the backend directory:
   ```
   cd backend
   ```
3. Create a virtual environment:
   ```
   py -m venv venv
   ```
4. Activate the virtual environment:
   - Windows:
     ```
     .\venv\Scripts\activate
     ```
   - macOS/Linux:
     ```
     source venv/bin/activate
     ```
5. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
6. Run the Flask server:
   ```
   py app.py
   ```
   The server will run on http://localhost:5000

### Frontend Setup

1. Make sure you have Node.js installed (v14 or higher)
2. Navigate to the frontend directory:
   ```
   cd frontend/food-order-system
   ```
3. Install dependencies:
   ```
   npm install
   ```
4. Run the development server:
   ```
   npm run dev
   ```
   The application will be available at http://localhost:5173

## How to Use

1. Open the application in your browser
2. Use the "New Normal Order" and "New VIP Order" buttons to create orders
3. Use the "+ Bot" and "- Bot" buttons to manage cooking bots
4. Watch as orders move from PENDING to COMPLETE as bots process them

## Implementation Details

- The backend uses Flask to provide a RESTful API
- The frontend uses Vue 3 with TypeScript for a responsive UI
- Orders and bots are stored in memory (no database required)
- The frontend polls the backend every second for updates
