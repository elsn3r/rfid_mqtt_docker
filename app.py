import platform

if platform.machine().startswith('arm') or platform.machine().startswith('aarch64'):
    import RPi.GPIO as GPIO
    # Hier GPIO spezifische Sachen machen
else:
    # Dummy oder Mock für Entwicklung am Mac
    class GPIOStub:
        def setup(self, *args, **kwargs): pass
        def input(self, *args, **kwargs): return 0
        def output(self, *args, **kwargs): pass
        def cleanup(self): pass
    GPIO = GPIOStub()
