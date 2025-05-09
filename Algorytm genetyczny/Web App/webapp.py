from genetics import *
import streamlit as st
import plotly.graph_objects as go

def run_genetic_algorithm_streamlit(
        cities,
        population_size,
        generations,
        mutation_rate,
        crossover_rate,
        center,
        radius
):
    status = st.subheader('Trwają obliczenia')
    paths, distances, seconds = genetic_algorithm(
        cities=cities,
        population_size=population_size,
        generations=generations,
        crossover_rate=crossover_rate,
        mutation_rate=mutation_rate,
        elite_size=0.05)
    status.subheader('Obliczenia zakończone')
    optimal_distance = round(optimal_path_distance(cities))
    st.success(f"Czas działania: {seconds:.2f} sekundy")
    st.metric('Długość optymalnej trasy', optimal_distance)

    chart_title = st.subheader('Trwa ładowanie wykresu')

    fig = go.Figure()
    fig.add_trace(go.Scatter(y=distances, mode='lines'))
    fig.add_hline(y=optimal_distance, line_dash="dash", line_color="red")
    fig.update_layout(
        xaxis_title='Pokolenie',
        yaxis_title='Długość trasy',
        yaxis_range=[0, distances[0]]
    )
    st.plotly_chart(fig)
    chart_title.subheader('Zmiana długość trasy w kolejnych pokoleniach')

    animation_status = st.subheader('Trwa ładowanie animacji')
    gif_path = "evolution.gif"
    create_route_animation(cities, paths, center=center, radius=radius, filename=gif_path)

    animation_status.subheader("Zmiana trasy w nowych generacjach")
    with open(gif_path, "rb") as f:
        st.image(f.read(), output_format="gif")