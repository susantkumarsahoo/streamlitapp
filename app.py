import streamlit as st

class Calculator:

    def __init__(self):
        self.num1 = 0
        self.num2 = 0

    def set_values(self, num1, num2):
        self.num1 = num1
        self.num2 = num2

    def add(self):
        r = self.num1 + self.num2
        result = f' Addition Total {r}'
        return result

    def subtract(self):
        r = self.num1 - self.num2
        result = f'Subtraction Total {r}'
        return result

    def multiply(self):
        r = self.num1 * self.num2
        result = f'Multiplication Total {r}'
        return result

    def divide(self):
        if self.num2 != 0:
            r = self.num1 / self.num2
            result = f'Division Total {r}'
        else:
            result = "Division by zero is not allowed."
        return result

# Streamlit app
st.title("Simple Calculator")

# Input fields for numbers
num1 = st.number_input("Enter the first number:", value=None, step=1, format="%d")
num2 = st.number_input("Enter the second number:", value=None, step=1, format="%d")

# Initialize the calculator
calculator = Calculator()

# Display buttons side by side with different colors
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Addition", key="sum", help="Click to calculate sum", use_container_width=True):
        calculator.set_values(num1, num2)
        result = calculator.add()
        st.success(result)

with col2:
    if st.button("Subtraction", key="subtract", help="Click to calculate difference", use_container_width=True):
        calculator.set_values(num1, num2)
        result = calculator.subtract()
        st.success(result)

with col3:
    if st.button("Multiplication", key="multiply", help="Click to calculate product", use_container_width=True):
        calculator.set_values(num1, num2)
        result = calculator.multiply()
        st.success(result)

with col4:
    if st.button("Division", key="divide", help="Click to calculate division", use_container_width=True):
        calculator.set_values(num1, num2)
        result = calculator.divide()
        st.success(result)


### 222
















