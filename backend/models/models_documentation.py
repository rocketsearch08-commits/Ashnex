# ========================================
# ASHNEX AGROTRADE - MONGODB MODELS
# Database Schema Definitions
# ========================================

"""
This file documents the MongoDB collections and schemas used by Ashnex Agrotrade.

To use MongoDB with this application:
1. Install pymongo: pip install pymongo
2. Create a MongoDB instance (local or Atlas)
3. Uncomment the MongoDB imports in app.py
4. Replace in_memory_data with actual MongoDB queries

MONGODB SETUP (LOCAL):
```
# Install MongoDB Community Edition
# On Windows: https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/
# On Mac: brew install mongodb-community
# On Linux: Follow official docs

# Start MongoDB
mongod

# Connect to MongoDB shell
mongo
```

MONGODB SETUP (ATLAS - Cloud):
1. Create account at https://www.mongodb.com/cloud/atlas
2. Create a cluster
3. Get connection string
4. Add to .env as MONGO_DB_URI
"""

# ========== PRODUCTS COLLECTION ==========
"""
Collection: products

Document Structure:
{
    "_id": ObjectId,
    "id": 1,
    "name": "Premium Cashew",
    "category": "Cashew",
    "description": "High-quality cashew nuts...",
    "price": 450,
    "unit": "kg",
    "minOrder": "500 kg",
    "image": "cashew.jpg",
    "createdAt": datetime,
    "updatedAt": datetime,
    "active": True
}

Indexes:
- db.products.createIndex({ "name": 1 })
- db.products.createIndex({ "category": 1 })
- db.products.createIndex({ "id": 1 })
"""

# ========== CONTACTS COLLECTION ==========
"""
Collection: contacts

Document Structure:
{
    "_id": ObjectId,
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "product": "Cashew",
    "quantity": 500,
    "message": "I'm interested in wholesale purchasing...",
    "createdAt": datetime,
    "status": "new",  // new, contacted, converted
    "notes": "Called on 2024-01-15"
}

Indexes:
- db.contacts.createIndex({ "email": 1 })
- db.contacts.createIndex({ "status": 1 })
- db.contacts.createIndex({ "createdAt": -1 })
"""

# ========== ORDERS COLLECTION ==========
"""
Collection: orders

Document Structure:
{
    "_id": ObjectId,
    "id": 1,
    "name": "ABC Company",
    "email": "orders@abc.com",
    "product": "Ginger",
    "quantity": 1000,
    "message": "Need monthly supply",
    "createdAt": datetime,
    "completedAt": null,
    "status": "pending",  // pending, confirmed, shipped, delivered, cancelled
    "estimatedPrice": 80000,
    "actualPrice": null,
    "paymentStatus": "pending"  // pending, paid, failed
}

Indexes:
- db.orders.createIndex({ "status": 1 })
- db.orders.createIndex({ "email": 1 })
- db.orders.createIndex({ "createdAt": -1 })
"""

# ========== EXAMPLE PYMONGO USAGE ==========
"""
# Import MongoDB client (in app.py)
from pymongo import MongoClient

# Connection
client = MongoClient(MONGO_DB_URI)
db = client[MONGO_DB_NAME]

# Access collections
products_collection = db.products
contacts_collection = db.contacts
orders_collection = db.orders

# Create indexes
db.products.create_index("name")
db.contacts.create_index("email")
db.orders.create_index("status")

# ===== BASIC CRUD OPERATIONS =====

# CREATE
product = {
    "name": "New Product",
    "category": "Category",
    "price": 100
}
result = products_collection.insert_one(product)
print(result.inserted_id)

# READ (Single)
product = products_collection.find_one({"name": "Premium Cashew"})

# READ (Multiple)
products = list(products_collection.find({"category": "Cashew"}))

# UPDATE
products_collection.update_one(
    {"_id": product_id},
    {"$set": {"price": 500}}
)

# DELETE
products_collection.delete_one({"_id": product_id})

# AGGREGATION (Advanced queries)
pipeline = [
    {"$match": {"status": "pending"}},
    {"$group": {"_id": "$product", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}}
]
results = list(orders_collection.aggregate(pipeline))
"""

# ========== DATA EXAMPLES ==========

SAMPLE_PRODUCTS = [
    {
        "id": 1,
        "name": "Premium Cashew",
        "category": "Cashew",
        "description": "High-quality W180 grade cashew nuts",
        "price": 450,
        "unit": "kg",
        "minOrder": "500 kg"
    },
    {
        "id": 2,
        "name": "Organic Ginger",
        "category": "Ginger",
        "description": "Fresh ginger powder and raw ginger",
        "price": 80,
        "unit": "kg",
        "minOrder": "1 ton"
    },
    {
        "id": 3,
        "name": "Pure Turmeric",
        "category": "Turmeric",
        "description": "High curcumin turmeric powder",
        "price": 150,
        "unit": "kg",
        "minOrder": "500 kg"
    }
]

# ========== MONGODB QUERY EXAMPLES ==========

# Example 1: Find all cashew products
# db.products.find({ "category": "Cashew" })

# Example 2: Find contacts created in last 7 days
# db.contacts.find({
#     "createdAt": { "$gte": ISODate("2024-01-08") }
# })

# Example 3: Count pending orders
# db.orders.countDocuments({ "status": "pending" })

# Example 4: Get total revenue
# db.orders.aggregate([
#     { "$match": { "status": "delivered" } },
#     { "$group": { "_id": null, "totalRevenue": { "$sum": "$actualPrice" } } }
# ])

# Example 5: Find top selling products
# db.orders.aggregate([
#     { "$group": { "_id": "$product", "totalQuantity": { "$sum": "$quantity" } } },
#     { "$sort": { "totalQuantity": -1 } },
#     { "$limit": 10 }
# ])
