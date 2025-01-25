### The current version of this code has a bug where resizing the terminal to a smaller window causes the placeholder to print an infinite number of new lines if the user enters and deletes text within the input box.

class PlaceholderInput:
    def __init__(self, placeholder=""):
        self.placeholder = placeholder
        self.static_text = ">>> "

    def get_input(self):
        import sys
        if sys.platform.startswith('win'):
            import msvcrt
            typed_text = ""
            sys.stdout.write('\033[?25l') 
            sys.stdout.write(self.static_text + self.placeholder)
            sys.stdout.flush()
            cursor_visible = False
            try:
                while True:
                    ch = msvcrt.getwch()
                    if not cursor_visible:
                        sys.stdout.write('\033[?25h')  
                        sys.stdout.flush()
                        cursor_visible = True
                    if ch == '\r':
                        if typed_text.strip():
                            sys.stdout.write('\n')
                            break
                    elif ch in ('\b', '\x08', '\x7f'):
                        if typed_text:
                            typed_text = typed_text[:-1]
                            sys.stdout.write('\b \b')
                            sys.stdout.flush()
                            if not typed_text:
                                sys.stdout.write('\033[?25l') 
                                sys.stdout.write(self.placeholder)
                                sys.stdout.flush()
                                cursor_visible = False
                    else:
                        if not typed_text:
                            sys.stdout.write('\r' + ' ' * (len(self.placeholder)) + '\r')
                            sys.stdout.write(self.static_text)
                            sys.stdout.flush()
                        typed_text += ch
                        sys.stdout.write(ch)
                        sys.stdout.flush()
            finally:
                sys.stdout.write('\033[?25h') 
                sys.stdout.flush()
            return typed_text
        else:
            import tty, termios
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            typed_text = ""
            sys.stdout.write('\033[?25l')  
            sys.stdout.write(self.static_text + self.placeholder)
            sys.stdout.flush()
            cursor_visible = False
            try:
                tty.setcbreak(fd)
                while True:
                    ch = sys.stdin.read(1)
                    if not cursor_visible:
                        sys.stdout.write('\033[?25h')  
                        sys.stdout.flush()
                        cursor_visible = True
                    if ch in ('\n', '\r'):
                        if typed_text.strip():
                            sys.stdout.write('\n')
                            break
                    elif ch in ('\b', '\x08', '\x7f'):
                        if typed_text:
                            typed_text = typed_text[:-1]
                            sys.stdout.write('\b \b')
                            sys.stdout.flush()
                            if not typed_text:
                                sys.stdout.write('\033[?25l') 
                                sys.stdout.write(self.placeholder)
                                sys.stdout.flush()
                                cursor_visible = False
                    else:
                        if not typed_text:
                            sys.stdout.write('\r' + ' ' * (len(self.placeholder)) + '\r')
                            sys.stdout.write(self.static_text)
                            sys.stdout.flush()
                        typed_text += ch
                        sys.stdout.write(ch)
                        sys.stdout.flush()
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                sys.stdout.write('\033[?25h')  
                sys.stdout.flush()
            return typed_text

    def set_placeholder(self, new_placeholder):
        """Set a new placeholder text."""
        self.placeholder = new_placeholder