from db import db
from sqlalchemy.sql import text

def create_thread(inquirer_id, lister_id, listing_id):
    try:
        sql = text("INSERT INTO threads (inquirer_id, lister_id, listing_id) VALUES (:inquirer_id, :lister_id, :listing_id) RETURNING id")
        result = db.session.execute(sql, {"inquirer_id":inquirer_id, "lister_id":lister_id, "listing_id":listing_id})
        thread_id = result.fetchone()[0]
        db.session.commit()
        return thread_id
    except:
        return False

def initial_message(inquirer_id, lister_id, listing_id, message):
    try:
        thread_id = create_thread(inquirer_id, lister_id, listing_id)

        sql = text("INSERT INTO messages (thread_id, sender_id, message) VALUES (:thread_id, :sender_id, :message)")
        db.session.execute(sql, {"thread_id":thread_id, "sender_id":inquirer_id, "message":message})
        db.session.commit()
        return True
    except:
        return False
    
def send_message(sender_id, thread_id, message):
    try:
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
            WHEN threads.inquirer_id = :user_id THEN lister.username
            ELSE inquirer.username
        END AS username,
        listing.name AS listing_name,
        latest_messages.created_at AS message_created_at
        FROM threads
        JOIN users AS inquirer ON threads.inquirer_id = inquirer.id
        JOIN users AS lister ON threads.lister_id = lister.id
        JOIN listings AS listing ON threads.listing_id = listing.id
        JOIN (
            SELECT thread_id, MAX(created_at) AS created_at
            FROM messages
            GROUP BY thread_id
        ) AS latest_messages ON threads.id = latest_messages.thread_id
        JOIN messages ON latest_messages.thread_id = messages.thread_id AND latest_messages.created_at = messages.created_at
        WHERE threads.inquirer_id = :user_id OR threads.lister_id = :user_id
        ORDER BY latest_messages.created_at DESC
    """)
    result = db.session.execute(sql, {"user_id": user_id})
    threads = result.fetchall()
    return threads

def get_thread_messages(thread_id, user_id):
    sql = text("""
        SELECT 
            messages.id,
            CASE
                WHEN messages.visible = TRUE THEN messages.message
                ELSE 'Käyttäjä on poistanut viestin'
            END AS message,
            messages.sender_id,
            messages.created_at,
            listings.name AS listing_name,
            listings.id AS listing_id,
            users.username
        FROM messages
        JOIN threads ON messages.thread_id = threads.id
        JOIN listings ON listings.id = threads.listing_id
        JOIN users ON messages.sender_id = users.id
        WHERE threads.id = :thread_id
        AND (threads.inquirer_id = :user_id OR threads.lister_id = :user_id)
        ORDER BY messages.created_at DESC
    """)
    result = db.session.execute(sql, {"thread_id": thread_id, "user_id": user_id})
    rows = result.fetchall()

    listing_name = rows[0][4]
    listing_id = rows[0][5]

    messages = []
    for row in rows:
        message = {
            "message_id": row[0],
            "message": row[1],
            "sender_id": row[2],
            "created_at": row[3],
            "username": row[6]
        }
        messages.append(message)

    return messages, listing_name, listing_id

def thread_exists(thread_id, user_id):
    sql = text("""
        SELECT id
        FROM threads
        WHERE id = :thread_id
        AND (inquirer_id = :user_id OR lister_id = :user_id)
    """)
    result = db.session.execute(sql, {"thread_id": thread_id, "user_id": user_id})
    thread = result.fetchone()
    return thread is not None
    
def delete_message(message_id, user_id):
    try:
        sql = text("""
            UPDATE messages
            SET visible = FALSE
            WHERE id = :message_id
            AND sender_id = :user_id
        """)
        db.session.execute(sql, {"message_id":message_id, "user_id":user_id})
        db.session.commit()

        return True
    except:
        return False
