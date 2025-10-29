#!/usr/bin/env python3
import os
import subprocess
import sys
import multiprocessing

# --- FUNCTIONS ---

def run_app(port, is_cloud):
    """
    Runs the web app process using gunicorn for cloud or simple app.py for local.
    """
    try:
        if is_cloud:
            # CLOUD DEPLOYMENT (Linux-based systems like Railway) - Use Gunicorn
            print(f"Starting web app (Gunicorn for health check) on port {port}...")
            # Assumes your Flask instance is named 'app' in 'app.py' (app:app)
            subprocess.run(
                [sys.executable, "-m", "gunicorn", "-w", "4", "-b", f"0.0.0.0:{port}", "app:app"], 
                check=True
            )
        else:
            # LOCAL DEVELOPMENT (Windows/macOS) - Use simple Flask server
            print(f"Starting web app (Flask dev server) on port {port}...")
            # NOTE: This assumes 'app.py' starts your Flask app (e.g., app.run())
            subprocess.run([sys.executable, "app.py"], check=True)

    except subprocess.CalledProcessError as e:
        print(f"Web app process failed with exit code {e.returncode}:")
        # Print stdout/stderr if available
        if e.stderr:
            print(e.stderr.decode('utf-8'))
        elif e.stdout:
            print(e.stdout.decode('utf-8'))
        sys.exit(1)

def run_bot():
    """
    Runs the Telegram bot as a Pyrogram module using long polling.
    """
    try:
        print("Starting Telegram bot process (Extractor module)...")
        # Ensure sessions directory exists for Pyrogram session files
        os.makedirs("sessions", exist_ok=True)
        
        # Launch the pyrogram/pyromod bot via its module name
        subprocess.run([sys.executable, "-m", "Extractor"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Bot process (Extractor) failed with exit code {e.returncode}:")
        if e.stderr:
            print(e.stderr.decode('utf-8'))
        elif e.stdout:
            print(e.stdout.decode('utf-8'))
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error in bot process: {e}")
        sys.exit(1)

# --- MAIN EXECUTION ---

if __name__ == "__main__":
    # 1) Verify we have the credentials we need
    try:
        from config import API_ID, API_HASH, BOT_TOKEN
        if not all([API_ID, API_HASH, BOT_TOKEN]):
            sys.exit("⚠️  Missing API_ID, API_HASH, or BOT_TOKEN in the environment or config.py")
    except ImportError:
        sys.exit("⚠️  Cannot import config.py. Check your file structure.")


    # 2) Check for cloud deployment variable (like Railway's $PORT)
    PORT = os.environ.get('PORT')
    
    if PORT:
        # --- CLOUD DEPLOYMENT LOGIC (Railway/Render/etc.) ---
        print("--- Running in Cloud Deployment Mode ---")
        
        # Start the Telegram bot in a separate, non-blocking process
        bot_proc = multiprocessing.Process(target=run_bot, name="telegram_bot")
        bot_proc.start()
        
        # The main thread runs the gunicorn web server on $PORT for the health check
        run_app(PORT, is_cloud=True)
        
        # Wait for the bot process if the web app stops
        bot_proc.join()
        
    else:
        # --- LOCAL DEVELOPMENT LOGIC ---
        
        print("--- Running in Local Development Mode (No PORT variable) ---")
        
        # Default local port for Flask
        local_port = 8080
        
        procs = [
            # NOTE: is_cloud=False to use the Windows-compatible Flask dev server
            multiprocessing.Process(target=run_app, name="web_app", args=(local_port, False)),
            multiprocessing.Process(target=run_bot, name="telegram_bot"),
        ]
        
        for p in procs:
            p.start()

        # Wait for both processes
        for p in procs:
            p.join()