import hashlib

def string_to_md5(input_string):
    # Create an MD5 hash object
    md5_hash = hashlib.md5()
    # Update the hash object with the bytes of the input string
    md5_hash.update(input_string.encode('utf-8'))
    # Get the hexadecimal representation of the hash
    md5_hex = md5_hash.hexdigest()
    return md5_hex
    


def register_user(user_name:str, user_password:str):
    from database.db_queries import ChatAppDatabase
    try:
        user = ChatAppDatabase().add_user(name=user_name, user_password=string_to_md5(user_password))
        print(f"User {user_name} registered successfully with ID: {user.user_id}: {user}")
        return True
    except Exception as e:
        print(f"Error registering user {user_name}: {e}")
        return False    
