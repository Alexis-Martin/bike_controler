from machine import Pin
import time


class Button():
    def __init__(self, pin):
        self.pin = pin
        self.button = Pin(pin, Pin.IN, Pin.PULL_UP)

    def __call__(self, pin):
        pass

class InterruptButton(Button):
    DEBOUNCE_TIME = 100 
    def __init__(self, pin, events):
        super().__init__(pin)
        self.button.irq(trigger=Pin.IRQ_FALLING, handler=self)
        self.events = events
        self.last_state = self.button.value()
        self.events[self.pin] = not self.button.value()
        self.last_interrupt_time = time.ticks_ms()
    
    def is_debouncing(self):
        current_time = time.ticks_ms()
        if current_time >  self.last_interrupt_time + self.DEBOUNCE_TIME:
            self.last_interrupt_time = current_time
            return True
        return False

    def __call__(self, pin):
        if self.is_debouncing():
            self.events[self.pin] = not self.button.value()
                


class AltInterruptButton(InterruptButton):
    def __init__(self, pin, events):
        super().__init__(pin, events)
        self.configure_interrupt()
    
    def configure_interrupt(self):
        if self.button.value() == 0:
            self.button.irq(trigger=Pin.IRQ_RISING, handler=self)
        else:
            self.button.irq(trigger=Pin.IRQ_FALLING, handler=self)

    def __call__(self, pin):
        super().__call__(pin)
        self.configure_interrupt()
        

class ModeButton(AltInterruptButton):
    def __init__(self, pin, events, nb_mode):
        super().__init__(pin, events)
        self.count = -1
        self.nb_mode = nb_mode
        self.exec()

    def exec(self):
        if self.button.value() == 0:
            self.count += 1
            if self.count >= self.nb_mode:
                self.count = 0
            self.events[self.pin] = self.count
        else:
            self.events[self.pin] = -1

    def __call__(self, pin):
        if self.is_debouncing():
            self.exec()

        self.configure_interrupt()

        