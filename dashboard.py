import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import altair as alt
from scipy.special import gamma

# Configuración de la página
st.set_page_config(page_title="Sistema: Osciladores Armónicos Unidimensionales (Clásicos)", layout="wide")
kB = 1.0

# Menú lateral
with st.sidebar:
    st.title("Menú")
    seleccion = st.radio("Ir a:", ["Inicio", "Osciladores Armónicos", "Configuración"])
    st.markdown("---")

    if seleccion == "Osciladores Armónicos":
        st.subheader("🔧 Parámetros del sistema")
        modo = st.radio("Elige la forma de cálculo para \( \Gamma_N(E) \)", 
                        ["Completa con unidades", "Adimensional (E / hν)^N"])
        N = st.slider("Número de osciladores (N)", min_value=1, max_value=100, value=3)
        E = st.number_input("Energía total (E)", value=10.0, format="%.2f")
        m = st.number_input("Masa de cada partícula (m)", value=1.0, format="%.2f")
        nu = st.number_input("Frecuencia natural (ν)", value=1.0, format="%.2f")
        h = st.number_input("Constante de Planck (h)", value=1.0, format="%.2f")

    elif seleccion == "Configuración":
        opcion_extra = st.checkbox("Activar modo avanzado")

# Área principal
st.title("🌐 Dashboard for Statistical Physics")

if seleccion == "Inicio":
    st.subheader("Bienvenido al Dashboard")
    st.write("Selecciona una opción del menú para comenzar.")

elif seleccion == "Osciladores Armónicos":
    st.markdown("## Sistema: Osciladores Armónicos Unidimensionales (Clásicos)")

    st.latex(r"H = \sum_{i=1}^N \left( \frac{p_i^2}{2m} + \frac{1}{2} m (2\pi \nu)^2 x_i^2 \right)")
    st.write("La región accesible del espacio fásico está dada por \( H \leq E \), formando una hiperesfera en \(2N\) dimensiones.")
    st.markdown("### Formas de \( \Gamma_N(E) \):")
    st.latex(r"\Gamma_N(E) = \frac{E^N}{h^N (m \omega)^N \Gamma(N+1)} \quad \text{donde } \omega = 2\pi \nu")
    st.latex(r"\Gamma_N(E) = \frac{1}{\Gamma(N+1)} \left( \frac{E}{h \nu} \right)^N")

    omega = 2 * np.pi * nu

    def volumen_fasico_completo(N, E, m, omega, h):
        return E**N / ((h**N) * (m * omega)**N * gamma(N + 1))

    def densidad_estados_completo(N, E, m, omega, h):
        return N * E**(N - 1) / ((h**N) * (m * omega)**N * gamma(N))

    def volumen_fasico_adimensional(N, E, nu, h):
        return (E / (h * nu))**N / gamma(N + 1)

    def densidad_estados_adimensional(N, E, nu, h):
        return N * (E / (h * nu))**(N - 1) / (h * nu * gamma(N))

    def entropia(Omega):
        return kB * np.log(Omega)

    # Cálculo
    if modo == "Completa con unidades":
        Gamma = volumen_fasico_completo(N, E, m, omega, h)
        Omega = densidad_estados_completo(N, E, m, omega, h)
    else:
        Gamma = volumen_fasico_adimensional(N, E, nu, h)
        Omega = densidad_estados_adimensional(N, E, nu, h)

    S = entropia(Omega)

    st.subheader("📈 Resultados")
    st.write(f"Volumen fásico \u0393(E): **{Gamma:.4e}**")
    st.write(f"Densidad de estados \u03a9(E): **{Omega:.4e}**")
    st.write(f"Entropía S(E): **{S:.4f}**")

    # Gráficas
    E_vals = np.linspace(0.01, 2 * E, 500)
    if modo == "Completa con unidades":
        Omega_vals = densidad_estados_completo(N, E_vals, m, omega, h)
        Gamma_vals = volumen_fasico_completo(N, E_vals, m, omega, h)
    else:
        Omega_vals = densidad_estados_adimensional(N, E_vals, nu, h)
        Gamma_vals = volumen_fasico_adimensional(N, E_vals, nu, h)

    fig1, ax1 = plt.subplots()
    ax1.plot(E_vals, Omega_vals, label="Ω(E)")
    ax1.set_xlabel("Energía E")
    ax1.set_ylabel("Ω(E)")
    ax1.set_title(f"Densidad de estados para N = {N}")
    ax1.grid(True)
    ax1.legend()
    st.pyplot(fig1)

    fig2, ax2 = plt.subplots()
    ax2.plot(E_vals, Gamma_vals, label="Γ(E)", color="green")
    ax2.set_xlabel("Energía E")
    ax2.set_ylabel("Γ(E)")
    ax2.set_title(f"Volumen fásico para N = {N}")
    ax2.grid(True)
    ax2.legend()
    st.pyplot(fig2)

    if N == 1:
        x_max = np.sqrt(2 * E / (m * omega**2))
        p_max = np.sqrt(2 * m * E)
        theta = np.linspace(0, 2 * np.pi, 500)
        x = x_max * np.cos(theta)
        p = p_max * np.sin(theta)

        fig3, ax3 = plt.subplots()
        ax3.plot(x, p, label="H(p, x) = E")
        ax3.set_xlabel("x (posición)")
        ax3.set_ylabel("p (momento)")
        ax3.set_title("Contorno de energía en el espacio fásico (N = 1)")
        ax3.grid(True)
        ax3.legend()
        st.pyplot(fig3)
    else:
        st.info("La representación del espacio fásico solo está disponible para N = 1.")

elif seleccion == "Configuración":
    st.subheader("⚙️ Configuración")
    st.write("Ajusta los parámetros según tus necesidades.")
    if opcion_extra:
        st.success("Modo avanzado activado.")
