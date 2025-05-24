# Adaptacyjny tempomat dostosowujący siłę hamownia na podstawie naszej prędkości, prędkości samochodu przed nami i odległości
from fuzzy_logic import *

while True:
    try:
        v = get_valid_input("Twoja prędkość (0-200 km/h): ", 0, 200)
        va = get_valid_input("Prędkość samochodu przed Tobą (0-200 km/h): ", 0, 200)
        d = get_valid_input("Odległość (0-150 m): ", 0, 150)

        brake_force = calculate_brake_force(v, va, d)

        print(f"\nDane wejściowe:")
        print(f"Prędkość Twojego samochodu: {v} km/h")
        print(f"Prędkość samochodu przed Tobą: {va} km/h")
        print(f"Odległość: {d} m")
        print(f"Siła hamowania: {brake_force:.2f}%")

    except Exception as e:
        print(f"Błąd: {e}")
        print("Spróbuj ponownie.")

    cont = input("\nKontynuować? [naciśnij Enter, aby kontynuować, wpisz 'q' aby zakończyć]: ")
    if cont.lower() == 'q':
        print("Zakończono program.")
        break