from spike import PrimeHub, ColorSensor, DistanceSensor, Motor
from spike.control import Timer, wait_for_seconds

hub = PrimeHub()

class Robot:
    # Inicia tudo e todos os métodos da classe "ROBOT"
    def __init__(self):
        self.hub = PrimeHub()
        self.cor = ColorSensor('E')
        self.ultrassonico = DistanceSensor('F')
        self.motorA = Motor('A')
        self.motorB = Motor('B')
        self.motorC = Motor('C')
        self.motorD = Motor('D')

        self.motorA.set_default_speed(50)
        self.motorB.set_default_speed(50)
        self.motorC.set_default_speed(50)
        self.motorD.set_default_speed(50)

    # Método do robô andar
    def andar(self) -> int:
        timer = Timer()
        while self.cor.get_reflected_light() >= 100:
            timer.time(5)
            self.motorA.start()
            self.motorB.start()
            self.motorC.start()
            self.motorD.start()

            if self.cor.get_color() == 'green':
                self.motorA.run_for_degrees(45, 65) # Motor A - (degrees, speed)
                self.motorB.run_for_degrees(90, 55) # Motor B - (degrees, speed)

                self.motorC.start(speed=50) # Os dois outros motores diminuem a velocidade para manter o controle na curva
                self.motorD.start(speed=50)

            else:
                self.motorA.start()
                self.motorB.start()
                self.motorC.start()
                self.motorD.start()

    def detecta_obj(self):
        distance = self.ultrassonico.get_distance_cm(short_range=True) # short_range = True funciona para o sensor agir com o range de pouco espaço à frente 

        if distance <= 5: # Se a distância for menor que cinco...
            timer = Timer() # Ativa um timer de 5 segundos
            while timer.time() <= 5: # Enquanto o timer for menor que 5s o robo vira as rodas até o timer apagar
                self.motorA.run_for_degrees(45, 65) # O robô vira e anda por 5 segundos (até o timer acabar).
                self.motorB.run_for_degrees(90, 55)

            timer.reset() # timer reseta

            self.motorA.run_for_degrees(45, -65)
            self.motorB.run_for_degrees(90, -55) # depois vira pra chegar na linha preta dnv

        self.andar()

    def run(self):
        while True:
            self.andar()
            self.detecta_obj()
            wait_for_seconds(0.5)

if __name__ == "__main__":
    robo = Robot()
    robo.run() 
