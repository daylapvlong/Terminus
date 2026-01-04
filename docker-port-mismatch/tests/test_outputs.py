#!/usr/bin/env python3
"""Test suite for Docker port mapping fix."""

import subprocess
import time
import json

SERVER_HOST = "localhost"
SERVER_PORT = 5000

def is_server_running():
    """Check if server process is running."""
    try:
        result = subprocess.run(
            ["pgrep", "-f", "python.*server.py"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except:
        return False

def start_server():
    """Start the Flask server in background."""
    try:
        # Kill any existing server processes
        subprocess.run(
            ["pkill", "-f", "python.*server.py"],
            capture_output=True,
            timeout=5
        )
        time.sleep(1)
    except:
        pass
    
    # Start server
    process = subprocess.Popen(
        ["python", "/app/server.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait for server to start
    time.sleep(3)
    
    return process

def stop_server():
    """Stop the Flask server."""
    try:
        subprocess.run(
            ["pkill", "-f", "python.*server.py"],
            capture_output=True,
            timeout=5
        )
        time.sleep(1)
    except:
        pass

def make_request(endpoint="/health", timeout=5):
    """Make HTTP request to server using curl."""
    try:
        result = subprocess.run(
            ["curl", "-s", "-w", "\\n%{http_code}", 
             f"http://{SERVER_HOST}:{SERVER_PORT}{endpoint}"],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        if result.returncode != 0:
            return None, None
        
        # Parse output: body + status code on last line
        lines = result.stdout.strip().split('\n')
        if len(lines) >= 2:
            body = '\n'.join(lines[:-1])
            status_code = int(lines[-1])
            return body, status_code
        
        return None, None
    except Exception as e:
        return None, None

def test_server_can_start():
    """Server should start without errors."""
    stop_server()
    process = start_server()
    
    try:
        # Check if process is still running
        assert process.poll() is None, \
            "Server process exited immediately after start"
        
        # Check if server is actually running
        time.sleep(1)
        assert is_server_running(), \
            "Server process not found in process list"
    finally:
        stop_server()

def test_server_responds_on_port_5000():
    """Server should respond to HTTP requests on port 5000."""
    stop_server()
    process = start_server()
    
    try:
        body, status_code = make_request("/health")
        
        assert status_code is not None, \
            f"No response from server on port {SERVER_PORT}. " \
            "Check that the application is configured to listen on the correct port."
        
        assert status_code == 200, \
            f"Expected status 200, got {status_code}"
    finally:
        stop_server()

def test_health_endpoint_returns_json():
    """Health endpoint should return valid JSON."""
    stop_server()
    process = start_server()
    
    try:
        body, status_code = make_request("/health")
        
        assert body is not None, "No response body received"
        
        try:
            data = json.loads(body)
        except json.JSONDecodeError as e:
            raise AssertionError(f"Response is not valid JSON: {e}")
        
        assert isinstance(data, dict), \
            f"Response should be JSON object, got {type(data)}"
    finally:
        stop_server()

def test_health_endpoint_has_status_field():
    """Health endpoint should return status field."""
    stop_server()
    process = start_server()
    
    try:
        body, status_code = make_request("/health")
        data = json.loads(body)
        
        assert "status" in data, \
            f"Response missing 'status' field. Got keys: {list(data.keys())}"
        
        assert data["status"] == "healthy", \
            f"Expected status='healthy', got '{data['status']}'"
    finally:
        stop_server()

def test_health_endpoint_includes_port():
    """Health endpoint should include port information."""
    stop_server()
    process = start_server()
    
    try:
        body, status_code = make_request("/health")
        data = json.loads(body)
        
        assert "port" in data, \
            "Response should include 'port' field"
        
        assert data["port"] == 5000, \
            f"Port in response should be 5000, got {data['port']}"
    finally:
        stop_server()

def test_root_endpoint_responds():
    """Root endpoint should respond successfully."""
    stop_server()
    process = start_server()
    
    try:
        body, status_code = make_request("/")
        
        assert status_code == 200, \
            f"Root endpoint should return 200, got {status_code}"
        
        data = json.loads(body)
        assert "message" in data, \
            "Root endpoint should return message field"
    finally:
        stop_server()

def test_api_info_endpoint_responds():
    """API info endpoint should respond with service information."""
    stop_server()
    process = start_server()
    
    try:
        body, status_code = make_request("/api/info")
        
        assert status_code == 200, \
            f"API info endpoint should return 200, got {status_code}"
        
        data = json.loads(body)
        assert "service" in data, \
            "API info should include service name"
        assert "version" in data, \
            "API info should include version"
        assert "port" in data, \
            "API info should include port"
    finally:
        stop_server()

def test_multiple_requests_work():
    """Server should handle multiple sequential requests."""
    stop_server()
    process = start_server()
    
    try:
        # Make 5 requests
        for i in range(5):
            body, status_code = make_request("/health")
            assert status_code == 200, \
                f"Request {i+1} failed with status {status_code}"
    finally:
        stop_server()

def test_server_listens_on_correct_port():
    """Server should be configured to listen on port 5000."""
    stop_server()
    process = start_server()
    
    try:
        # Try wrong port (should fail)
        result = subprocess.run(
            ["curl", "-s", "--max-time", "2", f"http://{SERVER_HOST}:8080/health"],
            capture_output=True,
            text=True
        )
        # Should fail to connect
        assert result.returncode != 0, \
            "Server should NOT respond on port 8080"
        
        # Try correct port (should succeed)
        body, status_code = make_request("/health")
        assert status_code == 200, \
            "Server should respond on port 5000"
    finally:
        stop_server()