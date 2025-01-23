import time
import sys
import threading

class LoadingAnimation:
    def __init__(self):
        self.stop_event = threading.Event()
        self.animation_thread = None

    def hide_cursor(self):
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

    def show_cursor(self):
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()

    def animate_dots(self, message):
        self.hide_cursor()
        while not self.stop_event.is_set():
            for dots in range(0, 4):
                if self.stop_event.is_set():
                    break
                sys.stdout.write(f"\r{message}{'.' * dots}{' ' * (3 - dots)}")
                sys.stdout.flush()
                time.sleep(0.5)
        sys.stdout.write("\r" + " " * (len(message) + 3) + "\r")  
        sys.stdout.flush()
        self.show_cursor()

    def start(self, start_message="Generating personality"):
        self.stop_event.clear()
        self.animation_thread = threading.Thread(target=self.animate_dots, args=(start_message,))
        self.animation_thread.start()

    def stop(self, end_message="Personality generated"):
        self.stop_event.set()
        self.animation_thread.join()
        sys.stdout.write(f"\r{end_message}\n")
        sys.stdout.flush()