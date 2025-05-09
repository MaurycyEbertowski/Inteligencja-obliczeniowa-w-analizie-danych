from webapp import *

st.set_page_config(layout="centered")
st.title("Algorytm genetyczny – Problem Komiwojażera")

# Parametry
n_cities = st.slider("Liczba miast", 5, 50, 20)
population_size = st.slider("Liczebność populacji", 10, 300, 100)
mutation_rate = st.slider("Prawdopodobieństwo mutacji", 0.0, 1.0, 0.05)
crossover_rate = st.slider("Prawdopodobieństwo krzyżowania", 0.0, 1.0, 0.9)
generations = st.select_slider("Liczba pokoleń", options=list(range(100, 1001, 100)))
radius = 250
center = (0, 0)

if st.button("Start"):
    #status = st.empty()
    #status.subheader('Trwają obliczenia')
    cities = generate_cities(n_cities, radius=radius, center=center)
    run_genetic_algorithm_streamlit(
        cities,
        population_size=population_size,
        generations=generations,
        mutation_rate=mutation_rate,
        crossover_rate=crossover_rate,
        center=center,
        radius=radius
    )
    #status.subheader('Obliczenia zakończone')