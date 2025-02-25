#!/bin/bash
echo "Starting Uvicorn on port: $PORT"
uvicorn app:app --host 0.0.0.0 --port $PORT --log-level info