import os
import sys
import signal
from multiprocessing import Process, freeze_support
from jarvis_ai_core import start_jarvis_background
from system_data_engine import start_system_data_engine
start_system_data_engine()


def run_gui():
    """Import and launch the GUI in a separate process."""
    from jarvis_gui import main
    main()


if __name__ == '__main__':
    freeze_support()  # Required for multiprocessing on Windows

    # Remove old lock file if it exists
    try:
        lock_path = "jarvis_data/gui_running.lock"
        if os.path.exists(lock_path):
            os.remove(lock_path)
    except Exception:
        pass

    # Ensure the required data directory exists
    os.makedirs("jarvis_data", exist_ok=True)

    # Start JARVIS AI brain in background
    print("Starting JARVIS AI system...")
    start_jarvis_background()  # <<<<<<<< ADDED THIS

    # Launch the GUI in a separate process
    gui_process = Process(target=run_gui)
    gui_process.daemon = False  # Keep GUI running even if parent exits
    gui_process.start()

    # Save GUI PID to a lock file
    try:
        with open("jarvis_data/gui_running.lock", "w") as f:
            f.write(str(gui_process.pid))
    except Exception:
        pass

    # Cleanup function to remove the lock file on exit
    def cleanup(signum, frame):
        try:
            if os.path.exists("jarvis_data/gui_running.lock"):
                os.remove("jarvis_data/gui_running.lock")
        except Exception:
            pass
        sys.exit(0)

    # Register cleanup handlers
    signal.signal(signal.SIGTERM, cleanup)
    signal.signal(signal.SIGINT, cleanup)

    # Wait for GUI process to finish
    gui_process.join()
