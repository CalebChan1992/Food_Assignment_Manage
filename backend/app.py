from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import threading
import uuid

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# In-memory data storage
orders = []
bots = []
next_order_id = 1
bot_lock = threading.Lock()

class Order:
    def __init__(self, order_id, is_vip=False):
        self.id = order_id
        self.is_vip = is_vip
        self.status = "PENDING"
        self.timestamp = time.time()

class Bot:
    def __init__(self, bot_id):
        self.id = bot_id
        self.status = "IDLE"
        self.current_order = None
        self.thread = None

def process_order(bot, order):
    with bot_lock:
        bot.status = "PROCESSING"
        bot.current_order = order
        order.status = "PROCESSING"
    
    # Simulate processing time (10 seconds)
    time.sleep(10)
    
    with bot_lock:
        if bot.status == "PROCESSING":  # Check if bot wasn't destroyed
            order.status = "COMPLETE"
            bot.status = "IDLE"
            bot.current_order = None
            
            # Look for next order to process
            next_order = get_next_pending_order()
            if next_order:
                bot.thread = threading.Thread(target=process_order, args=(bot, next_order))
                bot.thread.daemon = True
                bot.thread.start()

def get_next_pending_order():
    # First, look for VIP orders
    for order in orders:
        if order.status == "PENDING" and order.is_vip:
            return order
    
    # Then, look for normal orders
    for order in orders:
        if order.status == "PENDING" and not order.is_vip:
            return order
    
    return None

@app.route('/api/orders', methods=['GET'])
def get_orders():
    return jsonify({
        'orders': [
            {
                'id': order.id,
                'is_vip': order.is_vip,
                'status': order.status,
                'timestamp': order.timestamp
            } for order in orders
        ]
    })

@app.route('/api/orders/normal', methods=['POST'])
def create_normal_order():
    global next_order_id
    order = Order(next_order_id, is_vip=False)
    next_order_id += 1
    orders.append(order)
    
    # Check if any bot is available
    for bot in bots:
        if bot.status == "IDLE":
            bot.thread = threading.Thread(target=process_order, args=(bot, order))
            bot.thread.daemon = True
            bot.thread.start()
            break
    
    return jsonify({
        'id': order.id,
        'is_vip': order.is_vip,
        'status': order.status
    })

@app.route('/api/orders/vip', methods=['POST'])
def create_vip_order():
    global next_order_id
    order = Order(next_order_id, is_vip=True)
    next_order_id += 1
    orders.append(order)
    
    # Check if any bot is available
    for bot in bots:
        if bot.status == "IDLE":
            bot.thread = threading.Thread(target=process_order, args=(bot, order))
            bot.thread.daemon = True
            bot.thread.start()
            break
    
    return jsonify({
        'id': order.id,
        'is_vip': order.is_vip,
        'status': order.status
    })

@app.route('/api/bots', methods=['GET'])
def get_bots():
    return jsonify({
        'bots': [
            {
                'id': bot.id,
                'status': bot.status,
                'current_order': bot.current_order.id if bot.current_order else None
            } for bot in bots
        ]
    })

@app.route('/api/bots/add', methods=['POST'])
def add_bot():
    bot_id = str(uuid.uuid4())
    bot = Bot(bot_id)
    bots.append(bot)
    
    # Check if there's a pending order
    next_order = get_next_pending_order()
    if next_order:
        bot.thread = threading.Thread(target=process_order, args=(bot, next_order))
        bot.thread.daemon = True
        bot.thread.start()
    
    return jsonify({
        'id': bot.id,
        'status': bot.status
    })

@app.route('/api/bots/remove', methods=['POST'])
def remove_bot():
    if not bots:
        return jsonify({'error': 'No bots available'}), 400
    
    # Remove the newest bot
    bot = bots.pop()
    
    # If the bot was processing an order, return it to pending
    if bot.status == "PROCESSING" and bot.current_order:
        bot.current_order.status = "PENDING"
        bot.status = "DESTROYED"
    
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)
