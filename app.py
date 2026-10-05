import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1) Page setup
st.set_page_config(page_title="Trapezoidal Rule Explorer")


st.title("Numerical Integration: Trapezoidal Rule")
st.write(
    "แอปนี้ประมาณค่าปริพันธ์ $\\int_a^b x^2\\,dx$ ด้วย **กฎสี่เหลี่ยมคางหมู (Trapezoidal rule)** "
    "โดยแบ่งพื้นที่ใต้กราฟออกเป็นสี่เหลี่ยมคางหมูย่อย ๆ "
    "เลือกฟังก์ชัน กำหนดขอบเขต $a, b$ และจำนวนช่วงย่อย $n$ ได้จากแถบด้านซ้าย ")

with st.sidebar:
    st.header("Parameters")
    a = st.slider("Lower bound a", 0.0, 10.0, 0.0)
    b = st.slider("Upper bound b", 0.0, 10.0, 3.0)
    n = st.slider("Number of subintervals n", 1, 100, 5)
    show_table = st.checkbox("Show data table", value=True)

if a > b :
    st.warning("Please choose a <= b")
    st.stop()

# 1. คำนวณความกว้างช่วงย่อย dx
dx = (b - a) / n

# 2. สร้างจุดพิกัด x และคำนวณ y = f(x) (ตัวอย่างใช้ f(x) = x^2)
x = np.linspace(a, b, n + 1)
y = x**2

# 3. คำนวณประมาณค่าด้วย Trapezoidal Rule
integral_val = (dx / 2) * (y[0] + 2 * np.sum(y[1:-1]) + y[-1])

# 4. คำนวณค่าจริงทางอินทิเกรต (Exact Value of x^2 = [x^3 / 3]) ผ่าน NumPy
exact_val = (b**3 - a**3) / 3.0

# 5. เก็บข้อมูลจุดพิกัดลง DataFrame
data = pd.DataFrame({"x": x, "f(x)": y})

# 6. วาดกราฟแสดงผล
x_fine = np.linspace(a, b, 201)
y_fine = x_fine**2

fig, ax = plt.subplots()
ax.plot(x_fine, y_fine, color="#123f6c", linewidth=2, label="f(x) = x^2")
ax.fill_between(x, 0, y, alpha=0.3, color="#dc8d29", edgecolor="red", label="Trapezoids")
ax.plot(x, y, "ro")
ax.set(xlabel="x", ylabel="f(x)", title="Trapezoidal Rule Integration")
ax.grid(alpha=0.25)
ax.legend()

st.pyplot(fig)
plt.close(fig)

col1, col2 = st.columns(2)
col1.metric("Trapezoidal Value", f"{integral_val:.4f}")
col2.metric("Exact Value", f"{exact_val:.4f}")

if show_table:
    st.dataframe(data.round(4), hide_index=True)

csv_bytes = data.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download CSV",
    csv_bytes,
    file_name="trapezoidal_integration.csv",
    mime="text/csv",
)

if st.button("Show equation"):
    st.latex(
        r"\int_a^b f(x)\,dx \approx \frac{\Delta x}{2} \left[ f(x_0) + 2 \sum_{i=1}^{n-1} f(x_i) + f(x_n) \right]"
    )