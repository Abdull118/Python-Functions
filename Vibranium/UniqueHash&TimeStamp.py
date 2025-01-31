import hashlib
import time
import random
from datetime import datetime, timedelta, timezone


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

# Calculate the current time in UTC and add 5 minutes
future_time = datetime.now(timezone.utc) + timedelta(minutes=3)

# Convert the future time to a uint256 timestamp
uint256_timestamp = int(future_time.timestamp())

print(uint256_timestamp)
# Generate the uniqueIdHash
unique_id_hash = generate_unique_id_hash()
print(f"uniqueIdHash: 0x{unique_id_hash}")
