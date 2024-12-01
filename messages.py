from db import db
from sqlalchemy.sql import text

def create_message(sender_id, recipient_id, listing_id, thread_id, message):
    try:
        if thread_id == None:
            sql = text("INSERT INTO threads (sender_id, recipient_id, listing_id) VALUES (:sender_id, :recipient_id, :listing_id) RETURNING id")
            result = db.session.execute(sql, {"sender_id":sender_id, "recipient_id":recipient_id, "listing_id":listing_id})
            thread_id = result.fetchone()[0]
            db.session.commit()
        sql = text("INSERT INTO messages (thread_id, sender_id, message) VALUES (:thread_id, :sender_id, :message)")
        db.session.execute(sql, {"thread_id":thread_id, "sender_id":sender_id, "message":message})
        db.session.commit()
        return True
    except:
        return False
    
def get_threads(user_id):
    sql = text("""
        SELECT 
            threads.id,
            threads.listing_id,
            threads.created_at,
            CASE
                WHEN threads.sender_id = :user_id THEN recipient.username
                ELSE sender.username
            END AS username,
            listing.name AS listing_name
        FROM threads
        JOIN users AS sender ON threads.sender_id = sender.id
        JOIN users AS recipient ON threads.recipient_id = recipient.id
        JOIN listings AS listing ON threads.listing_id = listing.id 
        WHERE threads.sender_id = :user_id OR threads.recipient_id = :user_id
        ORDER BY threads.created_at DESC
    """)
    result = db.session.execute(sql, {"user_id": user_id})
    threads = result.fetchall()
    return threads

def get_thread_messages(thread_id, user_id):
    sql = text("""
        SELECT 
            messages.message,
            messages.created_at,
            users.username
        FROM messages
        JOIN threads ON messages.thread_id = threads.id
        JOIN users ON messages.sender_id = users.id
        WHERE threads.id = :thread_id
        AND (threads.sender_id = :user_id OR threads.recipient_id = :user_id)
    """)
    result = db.session.execute(sql, {"thread_id": thread_id, "user_id": user_id})
    messages = result.fetchall()
    return messages
