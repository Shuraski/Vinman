class PlaceholderInput:
    def __init__(self, placeholder="Enter message"):
        self.placeholder = placeholder
    def get_input(self):
        import sys
        if sys.platform.startswith('win'):
            import msvcrt
            typed_text = ""
            sys.stdout.write(self.placeholder)
            sys.stdout.flush()
            while True:
                ch = msvcrt.getwch()
                if ch == '\r':
                    sys.stdout.write('\n')
                    break
                elif ch in ('\b', '\x08', '\x7f'):
                    if typed_text:
                        typed_text = typed_text[:-1]
                        sys.stdout.write('\b \b')
                        sys.stdout.flush()
                        if not typed_text:
                            sys.stdout.write(self.placeholder)
                            sys.stdout.flush()
                else:
                    if not typed_text:
                        sys.stdout.write('\r' + ' ' * len(self.placeholder) + '\r')
                        sys.stdout.flush()
                    typed_text += ch
                    sys.stdout.write(ch)
                    sys.stdout.flush()
            return typed_text
        else:
            import tty, termios
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            typed_text = ""
            sys.stdout.write(self.placeholder)
            sys.stdout.flush()
            try:
                tty.setcbreak(fd)
                while True:
                    ch = sys.stdin.read(1)
                    if ch in ('\n', '\r'):
                        sys.stdout.write('\n')
                        break
                    elif ch in ('\b', '\x08', '\x7f'):
                        if typed_text:
                            typed_text = typed_text[:-1]
                            sys.stdout.write('\b \b')
                            sys.stdout.flush()
                            if not typed_text:
                                sys.stdout.write(self.placeholder)
                                sys.stdout.flush()
                    else:
                        if not typed_text:
                            sys.stdout.write('\r' + ' ' * len(self.placeholder) + '\r')
                            sys.stdout.flush()
                        typed_text += ch
                        sys.stdout.write(ch)
                        sys.stdout.flush()
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return typed_text