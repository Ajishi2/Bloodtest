#!/usr/bin/env python3
"""
Startup script for Blood Test Analyzer with Queue Worker Model
This script helps start all required services: Redis, Celery Worker, and FastAPI
"""

import subprocess
import sys
import time
import os
import signal
from pathlib import Path

def check_redis():
    """Check if Redis is running"""
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
        return True
    except:
        return False

def start_redis():
    """Start Redis server"""
    print("🔴 Starting Redis server...")
    try:
        # Try to start Redis using common commands
        redis_commands = [
            ["redis-server"],
            ["brew", "services", "start", "redis"],
            ["systemctl", "start", "redis"],
            ["service", "redis", "start"]
        ]
        
        for cmd in redis_commands:
            try:
                subprocess.run(cmd, check=True, capture_output=True)
                print("✅ Redis started successfully")
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
        
        print("❌ Could not start Redis automatically")
        print("Please start Redis manually:")
        print("  - macOS: brew services start redis")
        print("  - Ubuntu: sudo systemctl start redis")
        print("  - Windows: Download and run Redis server")
        return False
        
    except Exception as e:
        print(f"❌ Error starting Redis: {e}")
        return False

def start_celery_worker():
    """Start Celery worker"""
    print("🟢 Starting Celery worker...")
    try:
        # Start Celery worker in background
        worker_process = subprocess.Popen([
            sys.executable, "-m", "celery", "-A", "celery_app", "worker", 
            "--loglevel=info", "--concurrency=2"
        ])
        print("✅ Celery worker started successfully")
        return worker_process
    except Exception as e:
        print(f"❌ Error starting Celery worker: {e}")
        return None

def start_fastapi():
    """Start FastAPI server"""
    print("🚀 Starting FastAPI server...")
    try:
        # Start FastAPI server
        server_process = subprocess.Popen([
            sys.executable, "main.py"
        ])
        print("✅ FastAPI server started successfully")
        return server_process
    except Exception as e:
        print(f"❌ Error starting FastAPI server: {e}")
        return None

def main():
    """Main startup function"""
    print("🏥 Blood Test Analyzer - Starting Services")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("main.py").exists():
        print("❌ Error: main.py not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    processes = []
    
    try:
        # Check and start Redis
        if not check_redis():
            if not start_redis():
                print("❌ Redis is required but could not be started")
                sys.exit(1)
        else:
            print("✅ Redis is already running")
        
        # Wait a moment for Redis to be ready
        time.sleep(2)
        
        # Start Celery worker
        worker_process = start_celery_worker()
        if worker_process:
            processes.append(("Celery Worker", worker_process))
        
        # Wait a moment for worker to start
        time.sleep(3)
        
        # Start FastAPI server
        server_process = start_fastapi()
        if server_process:
            processes.append(("FastAPI Server", server_process))
        
        print("\n" + "=" * 50)
        print("🎉 All services started successfully!")
        print("\n📋 Service Status:")
        print("  - Redis: ✅ Running")
        print("  - Celery Worker: ✅ Running")
        print("  - FastAPI Server: ✅ Running")
        print("\n🌐 Access your API at: http://localhost:8000")
        print("📖 API Documentation: http://localhost:8000/docs")
        print("💚 Health Check: http://localhost:8000/health")
        print("\n⏹️  Press Ctrl+C to stop all services")
        
        # Keep the script running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping all services...")
        
        # Stop all processes
        for name, process in processes:
            print(f"Stopping {name}...")
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            except:
                pass
        
        print("✅ All services stopped")

if __name__ == "__main__":
    main() 