# Placeholder for logging functions
import os
import datetime
import glob

def log_error(message):
    """Logs an error message."""
    try:
        os.makedirs("logs", exist_ok=True)  # Creates the 'logs' directory if it does not exist.
        with open("logs/error.log", "a") as f:
           f.write(f"ERROR: {message}\n")
        print("Error logged to logs/error.log")
    except Exception as e:
        print(f"Error while logging message {message}: {e}")

def log_chat(input_text, output_text, log_file_path):
    """Logs chat input and output to a separate file with timestamp."""
    try:
        with open(log_file_path, "a") as f:
            f.write(f"USER: {input_text}\n")
            f.write(f"BOT: {output_text}\n")
        print(f"Chat logged to {log_file_path}")
        rotate_chat_logs()

    except Exception as e:
        print(f"Error while logging input: {input_text} and output: {output_text}: {e}")


def rotate_chat_logs():
    """Deletes the oldest chat log file if there are more than 10."""
    log_dir = os.path.join("logs", "chat_logs")
    log_files = glob.glob(os.path.join(log_dir, "chat_*.log"))
    if len(log_files) > 10:
        log_files.sort(key=os.path.getmtime)  # Sort by modification time, oldest first.
        oldest_log = log_files[0]  # Select the oldest log file.
        try:
          os.remove(oldest_log)
          print(f"Oldest chat log file removed: {oldest_log}")
        except Exception as e:
           print(f"Error while removing old log files: {e}")