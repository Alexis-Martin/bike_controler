from machine import Pin, PWM
import time

# Définir la broche où vous voulez générer le PWM (GPIO 4)
pwm_pin4 = Pin(4, Pin.OUT)
pwm_pin3 = Pin(3, Pin.OUT)

# Créer un objet PWM sur la broche
pwm4 = PWM(pwm_pin4)
pwm3 = PWM(pwm_pin3)

# Configurer la fréquence du PWM (en Hz)
pwm4.freq(20000)  # 5 kHz, vous pouvez ajuster selon vos besoins
pwm3.freq(20000)  # 5 kHz, vous pouvez ajuster selon vos besoins

# Configurer le rapport cyclique du PWM (duty cycle)
pwm4.duty(512)  # De 0 à 1023 pour une résolution de 10 bits
pwm3.duty(512)  # De 0 à 1023 pour une résolution de 10 bits

while True:
    # Augmenter progressivement le rapport cyclique
    for i in range(0, 1024, 10):  # Incrémenter de 10 à chaque fois
        pwm4.duty(i)
        pwm3.duty(i)
        time.sleep(0.01)
    
    # Réduire progressivement le rapport cyclique
    for i in range(1023, -1, -10):  # Décrémenter de 10 à chaque fois
        pwm4.duty(i)
        pwm3.duty(i)
        time.sleep(0.01)
