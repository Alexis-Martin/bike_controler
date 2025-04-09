def stop_all(pwm_functions):
    for function in pwm_functions:
        function.stop()


class Indicator():
    def __init__(self, pwm):
        self.pwm = pwm 
        self.pwm.duty(0)
        self.i = 0
        self.inc = 70
        self.saturation_max = 1500
        self.saturation_min = -500
        self.started = False

    def __call__(self):
        self.started = True
        i = self.i
        if self.i > 1023:
            i = 1023
        elif self.i < 0:
            i = 0
        self.pwm.duty(i)
        self.i += self.inc

        if self.i > self.saturation_max:
            self.inc *= -1
        elif self.i < self.saturation_min:
            self.inc *= -1

    def stop(self):
        self.pwm.duty(0)
        self.i = 0
        self.inc = abs(self.inc)
        self.started = False

    def is_started(self):
        return self.started


class FrontLight():
    MODE = ["ECO", "NORMAL", "BOOST"]

    def __init__(self, pwm):
        self.pwm = pwm 
        self.pwm.duty(0)
        self.started = False
        self.mode = FrontLight.MODE[0]
        self.eco()

    def eco(self):
        self.duty_val = 70

    def normal(self):
        self.duty_val = 150

    def boost(self):
        self.duty_val = 600
    
    def set_mode(self, mode):
        if self.mode != FrontLight.MODE[mode]:
            self.mode = FrontLight.MODE[mode]
            print(self.mode)
            method_name = self.mode.lower()
            getattr(self, method_name)() 

    def __call__(self):
        self.pwm.duty(self.duty_val)


    def stop(self):
        self.pwm.duty(0)
        self.started = False

    def is_started(self):
        return self.started


class BackLight():
    MODE = ["ECO", "FADING", "BOOST"]
    def __init__(self, pwm):
        self.pwm = pwm 
        self.pwm.duty(0)
        self.started = False
        self.mode = BackLight.MODE[0]
        self.eco()

    def eco(self):
        self.val = 75

    def fading(self):
        self.val = 130

    def boost(self):
        self.val = 200
        
    def set_mode(self, mode):
        if self.mode != BackLight.MODE[mode]:
            self.mode = BackLight.MODE[mode]
            print(self.mode)
            method_name = self.mode.lower()
            getattr(self, method_name)() 

    def __call__(self):
        self.pwm.duty(self.val)


    def stop(self):
        self.pwm.duty(0)
        self.started = False          

    def is_started(self):
        return self.started


class Klaxon():
    def __init__(self, pwm_list):
        self.pwm_list = pwm_list 
        for pwm in self.pwm_list:
            pwm.duty(0)
        self.val = 900
        self.started = False

    def __call__(self):
        for pwm in self.pwm_list:
            pwm.duty(self.val)

    def stop(self):
        for pwm in self.pwm_list:
            pwm.duty(0)

    def is_started(self):
        return self.started
