import hashlib
import time
import random

def generate_unique_id_hash():
    # Get the current time in seconds since the epoch
    current_time = str(time.time())

    # Generate a random number
    random_number = str(random.randint(0, int(1e18)))

    # Combine the current time and the random number to create a unique string
    unique_string = current_time + random_number

    # Create a SHA-256 hash of the unique string
    unique_id_hash = hashlib.sha256(unique_string.encode('utf-8')).hexdigest()

    return unique_id_hash

# Generate the uniqueIdHash
unique_id_hash = generate_unique_id_hash()
print(f"uniqueIdHash: 0x{unique_id_hash}")
