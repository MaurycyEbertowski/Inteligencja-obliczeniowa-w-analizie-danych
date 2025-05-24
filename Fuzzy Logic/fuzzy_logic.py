# Adaptacyjny tempomat dostosowujący siłę hamownia na podstawie naszej prędkości, prędkości samochodu przed nami i odległości
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Definiowanie zmiennych wejściowych i wyjściowych
my_speed = ctrl.Antecedent(np.arange(0, 201, 1), 'my_speed')
speed_car_ahead = ctrl.Antecedent(np.arange(0, 201, 1), 'speed_car_ahead')
distance = ctrl.Antecedent(np.arange(0, 151, 1), 'distance')
brake_force = ctrl.Consequent(np.arange(0, 101, 1), 'brake_force')

# Własna prędkość
my_speed['low'] = fuzz.trimf(my_speed.universe, [0, 0, 60])
my_speed['medium'] = fuzz.trimf(my_speed.universe, [40, 80, 120])
my_speed['high'] = fuzz.trimf(my_speed.universe, [100, 140, 180])
my_speed['very_high'] = fuzz.trimf(my_speed.universe, [170, 200, 200])

# Prędkość samochodu z przodu
speed_car_ahead['low'] = fuzz.trimf(speed_car_ahead.universe, [0, 0, 60])
speed_car_ahead['medium'] = fuzz.trimf(speed_car_ahead.universe, [40, 80, 120])
speed_car_ahead['high'] = fuzz.trimf(speed_car_ahead.universe, [100, 140, 180])
speed_car_ahead['very_high'] = fuzz.trimf(speed_car_ahead.universe, [170, 200, 200])

# Odległość od samochodu z przodu
distance['low'] = fuzz.trimf(distance.universe, [0, 0, 50])
distance['medium'] = fuzz.trimf(distance.universe, [40, 80, 120])
distance['high'] = fuzz.trimf(distance.universe, [110, 150, 150])

# Siła hamowania
brake_force['none'] = fuzz.trimf(brake_force.universe, [0, 0, 0])
brake_force['very_light'] = fuzz.trimf(brake_force.universe, [0, 0, 20])
brake_force['light'] = fuzz.trimf(brake_force.universe, [10, 30, 50])
brake_force['medium'] = fuzz.trimf(brake_force.universe, [40, 60, 80])
brake_force['strong'] = fuzz.trimf(brake_force.universe, [70, 100, 100])
brake_force['max'] = fuzz.trimf(brake_force.universe, [100, 100, 100])

# Wizualizacja funkcji przynależności
my_speed.view()
speed_car_ahead.view()
distance.view()
brake_force.view()
plt.show()

# Definicja reguł rozmytych dla każdej możliwej kombinacji
rules = [
    ctrl.Rule(distance['high'] & my_speed['low'] & speed_car_ahead['low'], brake_force['none']),
    ctrl.Rule(distance['high'] & my_speed['low'] & speed_car_ahead['medium'], brake_force['none']),
    ctrl.Rule(distance['high'] & my_speed['low'] & speed_car_ahead['high'], brake_force['none']),
    ctrl.Rule(distance['high'] & my_speed['low'] & speed_car_ahead['very_high'], brake_force['none']),
    ctrl.Rule(distance['high'] & my_speed['medium'] & speed_car_ahead['low'], brake_force['none']),
    ctrl.Rule(distance['high'] & my_speed['medium'] & speed_car_ahead['medium'], brake_force['none']),
    ctrl.Rule(distance['high'] & my_speed['medium'] & speed_car_ahead['high'], brake_force['none']),
    ctrl.Rule(distance['high'] & my_speed['medium'] & speed_car_ahead['very_high'], brake_force['none']),
    ctrl.Rule(distance['high'] & my_speed['high'] & speed_car_ahead['low'], brake_force['medium']),
    ctrl.Rule(distance['high'] & my_speed['high'] & speed_car_ahead['medium'], brake_force['light']),
    ctrl.Rule(distance['high'] & my_speed['high'] & speed_car_ahead['high'], brake_force['none']),
    ctrl.Rule(distance['high'] & my_speed['high'] & speed_car_ahead['very_high'], brake_force['none']),
    ctrl.Rule(distance['high'] & my_speed['very_high'] & speed_car_ahead['low'], brake_force['strong']),
    ctrl.Rule(distance['high'] & my_speed['very_high'] & speed_car_ahead['medium'], brake_force['medium']),
    ctrl.Rule(distance['high'] & my_speed['very_high'] & speed_car_ahead['high'], brake_force['very_light']),
    ctrl.Rule(distance['high'] & my_speed['very_high'] & speed_car_ahead['very_high'], brake_force['none']),

    ctrl.Rule(distance['medium'] & my_speed['low'] & speed_car_ahead['low'], brake_force['none']),
    ctrl.Rule(distance['medium'] & my_speed['low'] & speed_car_ahead['medium'], brake_force['none']),
    ctrl.Rule(distance['medium'] & my_speed['low'] & speed_car_ahead['high'], brake_force['none']),
    ctrl.Rule(distance['medium'] & my_speed['low'] & speed_car_ahead['very_high'], brake_force['none']),
    ctrl.Rule(distance['medium'] & my_speed['medium'] & speed_car_ahead['low'], brake_force['very_light']),
    ctrl.Rule(distance['medium'] & my_speed['medium'] & speed_car_ahead['medium'], brake_force['none']),
    ctrl.Rule(distance['medium'] & my_speed['medium'] & speed_car_ahead['high'], brake_force['none']),
    ctrl.Rule(distance['medium'] & my_speed['medium'] & speed_car_ahead['very_high'], brake_force['none']),
    ctrl.Rule(distance['medium'] & my_speed['high'] & speed_car_ahead['low'], brake_force['strong']),
    ctrl.Rule(distance['medium'] & my_speed['high'] & speed_car_ahead['medium'], brake_force['light']),
    ctrl.Rule(distance['medium'] & my_speed['high'] & speed_car_ahead['high'], brake_force['none']),
    ctrl.Rule(distance['medium'] & my_speed['high'] & speed_car_ahead['very_high'], brake_force['none']),
    ctrl.Rule(distance['medium'] & my_speed['very_high'] & speed_car_ahead['low'], brake_force['max']),
    ctrl.Rule(distance['medium'] & my_speed['very_high'] & speed_car_ahead['medium'], brake_force['strong']),
    ctrl.Rule(distance['medium'] & my_speed['very_high'] & speed_car_ahead['high'], brake_force['medium']),
    ctrl.Rule(distance['medium'] & my_speed['very_high'] & speed_car_ahead['very_high'], brake_force['none']),

    ctrl.Rule(distance['low'] & my_speed['low'] & speed_car_ahead['low'], brake_force['light']),
    ctrl.Rule(distance['low'] & my_speed['low'] & speed_car_ahead['medium'], brake_force['none']),
    ctrl.Rule(distance['low'] & my_speed['low'] & speed_car_ahead['high'], brake_force['none']),
    ctrl.Rule(distance['low'] & my_speed['low'] & speed_car_ahead['very_high'], brake_force['none']),
    ctrl.Rule(distance['low'] & my_speed['medium'] & speed_car_ahead['low'], brake_force['strong']),
    ctrl.Rule(distance['low'] & my_speed['medium'] & speed_car_ahead['medium'], brake_force['very_light']),
    ctrl.Rule(distance['low'] & my_speed['medium'] & speed_car_ahead['high'], brake_force['none']),
    ctrl.Rule(distance['low'] & my_speed['medium'] & speed_car_ahead['very_high'], brake_force['none']),
    ctrl.Rule(distance['low'] & my_speed['high'] & speed_car_ahead['low'], brake_force['max']),
    ctrl.Rule(distance['low'] & my_speed['high'] & speed_car_ahead['medium'], brake_force['strong']),
    ctrl.Rule(distance['low'] & my_speed['high'] & speed_car_ahead['high'], brake_force['very_light']),
    ctrl.Rule(distance['low'] & my_speed['high'] & speed_car_ahead['very_high'], brake_force['none']),
    ctrl.Rule(distance['low'] & my_speed['very_high'] & speed_car_ahead['low'], brake_force['max']),
    ctrl.Rule(distance['low'] & my_speed['very_high'] & speed_car_ahead['medium'], brake_force['max']),
    ctrl.Rule(distance['low'] & my_speed['very_high'] & speed_car_ahead['high'], brake_force['strong']),
    ctrl.Rule(distance['low'] & my_speed['very_high'] & speed_car_ahead['very_high'], brake_force['very_light']),
]

# Tworzenie i symulacja systemu sterowania
system_hamowania = ctrl.ControlSystem(rules)
braking = ctrl.ControlSystemSimulation(system_hamowania)


# Obliczanie siły hamowania
def calculate_brake_force(my_v, v_ahead, dist):
    braking.input['my_speed'] = my_v
    braking.input['speed_car_ahead'] = v_ahead
    braking.input['distance'] = dist
    braking.compute()

    plt.close('all')
    brake_force.view(sim=braking)
    plt.show()
    return braking.output['brake_force']

# Walidacja danych wejściowych
def get_valid_input(prompt, min_val, max_val):
    while True:
        try:
            value = int(input(prompt))
            if min_val <= value <= max_val:
                return value
            else:
                print(f"Wartość musi być w zakresie [{min_val}, {max_val}]. Spróbuj ponownie.")
        except ValueError:
            print("Wprowadź poprawną liczbę całkowitą. Spróbuj ponownie.")

print("Wprowadź dane, aby obliczyć siłę hamowania. Wpisz 'q' aby zakończyć.")