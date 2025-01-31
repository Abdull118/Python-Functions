from datetime import datetime, timedelta, timezone

# Calculate the current time in UTC and add 5 minutes
future_time = datetime.now(timezone.utc) + timedelta(minutes=3)

# Convert the future time to a uint256 timestamp
uint256_timestamp = int(future_time.timestamp())

print(uint256_timestamp)
