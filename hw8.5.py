import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.title("Logistic curve explorer")

beta0 = st.slider("beta0 (intercept)", -10.0, 10.0, 0.0, 0.1)
beta1 = st.slider("beta1 (slope)", -5.0, 5.0, 1.0, 0.1)

x = np.linspace(-10, 10, 200)
f = np.exp(beta0 + beta1 * x) / (1 + np.exp(beta0 + beta1 * x))

fig, ax = plt.subplots()
ax.plot(x, f)
ax.set_ylim(-0.05, 1.05)
ax.set_xlabel("x")
ax.set_ylabel("f(x)")
st.pyplot(fig)