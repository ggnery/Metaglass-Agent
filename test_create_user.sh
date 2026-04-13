#!/bin/bash

# This script detects the project root to work from any directory
PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Helper function to run grpcurl
run_grpc() {
  local service_method=$1
  local data=$2
  grpcurl -plaintext \
    -import-path "$PROJECT_ROOT/proto" \
    -proto "$PROJECT_ROOT/proto/session.proto" \
    -d "$data" \
    localhost:50051 "$service_method"
}

echo "--- 1. Registering Device ---"
DEVICE_RESP=$(run_grpc "metaglass.Session/RegisterDevice" '{
  "device_name": "Ray-Ban Meta",
  "device_model": "V1",
  "metadata": {"firmware": "1.0.0"}
}')
echo "$DEVICE_RESP"

if ! command -v jq >/dev/null 2>&1; then
  echo -e "\n[ERROR] 'jq' is required for this automated test script."
  exit 1
fi

DEVICE_ID=$(echo "$DEVICE_RESP" | jq -r '.deviceId')

echo -e "\n--- 2. Creating User ---"
USER_RESP=$(run_grpc "metaglass.Session/CreateUser" "{
  \"name\": \"Jane Doe\",
  \"email\": \"jane@example.com\",
  \"preferred_language\": \"en-US\",
  \"device_id\": \"$DEVICE_ID\",
  \"metadata\": {\"origin\": \"test_script\"}
}")
echo "$USER_RESP"
USER_ID=$(echo "$USER_RESP" | jq -r '.userId')

echo -e "\n--- 3. Creating Session ---"
SESSION_RESP=$(run_grpc "metaglass.Session/CreateSession" "{
  \"user_id\": \"$USER_ID\",
  \"device_id\": \"$DEVICE_ID\",
  \"initial_metadata\": {\"location\": \"test-lab\"}
}")
echo "$SESSION_RESP"
SESSION_ID=$(echo "$SESSION_RESP" | jq -r '.sessionId')

echo -e "\n--- 4. Sending Heartbeat ---"
# Cross-platform way to get milliseconds
TIMESTAMP=$(python3 -c 'import time; print(int(time.time() * 1000))')
HEARTBEAT_RESP=$(run_grpc "metaglass.Session/Heartbeat" "{
  \"session_id\": \"$SESSION_ID\",
  \"timestamp_ms\": $TIMESTAMP
}")
echo "$HEARTBEAT_RESP"

echo -e "\n--- 5. Ending Session ---"
END_RESP=$(run_grpc "metaglass.Session/EndSession" "{
  \"session_id\": \"$SESSION_ID\"
}")
echo "$END_RESP"

echo -e "\n--- Lifecycle Test Complete ---"
