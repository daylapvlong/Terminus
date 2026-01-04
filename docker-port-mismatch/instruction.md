# Fix Docker Port Mapping

Your task is to fix a port mapping mismatch in the Dockerfile that prevents the Flask application from being properly documented.

## Problem

The Python Flask application is configured to listen on port 5000, but the Dockerfile exposes port 8080. While the application may still work, this misconfiguration causes issues with:
- Docker port auto-mapping (`docker run -P`)
- Documentation and best practices
- Container orchestration tools

## Current Configuration

- **Application**: Listens on port `5000` (in `/app/server.py`)
- **Dockerfile**: Exposes port `8080` (in `/environment/Dockerfile`)

## Requirements

1. Fix the `EXPOSE` directive in `/environment/Dockerfile` to match the application's port
2. The Dockerfile should expose port 5000
3. Do not modify the application code in `/app/server.py`
4. Only modify the Dockerfile

## Files to Modify

- **Input**: `/environment/Dockerfile`
- **Do NOT modify**: `/app/server.py`

## Expected Behavior

After the fix:
- The Dockerfile should expose port 5000
- The application starts successfully
- Health check endpoint at `/health` responds with `200 OK`
- The response contains `{"status": "healthy", "port": 5000}`

## Verification

The tests will verify that:
1. Server starts without errors
2. Application listens on port 5000 (not 8080)
3. All API endpoints respond correctly
4. Multiple requests can be handled

## Docker EXPOSE Directive

The `EXPOSE` directive documents which ports the container listens on at runtime. While it doesn't actually publish the port, it serves as documentation and is used by tools like `docker run -P` to automatically map ports. It's important that `EXPOSE` matches the actual port the application uses.