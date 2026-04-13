#!/bin/bash

# This script detects the project root to work from any directory
PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

echo "Step 1: Registering a Device..."
DEVICE_RESPONSE=$(grpcurl -plaintext \
  -import-path "$PROJECT_ROOT/proto" \
  -proto "$PROJECT_ROOT/proto/session.proto" \
  -d '{
    "device_name": "Ray-Ban Meta",
    "device_model": "V1",
    "metadata": {"firmware": "1.0.0"}
  }' \
  localhost:50051 metaglass.Session/RegisterDevice)

echo "$DEVICE_RESPONSE"

# Extract device_id using jq if available, otherwise suggest manual copy
if command -v jq >/dev/null 2>&1; then
    DEVICE_ID=$(echo "$DEVICE_RESPONSE" | jq -r '.deviceId')
    
    if [ "$DEVICE_ID" != "null" ] && [ -n "$DEVICE_ID" ]; then
        echo -e "\nStep 2: Creating a User for Device: $DEVICE_ID..."
        grpcurl -plaintext \
          -import-path "$PROJECT_ROOT/proto" \
          -proto "$PROJECT_ROOT/proto/session.proto" \
          -d "{
            \"name\": \"Jane Doe\",
            \"email\": \"jane@example.com\",
            \"preferred_language\": \"en-US\",
            \"device_id\": \"$DEVICE_ID\",
            \"metadata\": {\"origin\": \"test_script\"}
          }" \
          localhost:50051 metaglass.Session/CreateUser
    else
        echo "Error: Could not extract device_id from response."
    fi
else
    echo -e "\n[INFO] 'jq' not found. To create a user with a valid device_id, copy the device_id from above and run:"
    echo "grpcurl -plaintext -import-path ./proto -proto session.proto -d '{\"name\": \"Jane\", \"device_id\": \"PASTE_HERE\"}' localhost:50051 metaglass.Session/CreateUser"
fi
