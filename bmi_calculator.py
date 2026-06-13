# ============================================================
#   BMI Calculator - Command Line Application
#   Created by : VISHNU S
#   Project    : Python Internship
#   Description: A simple CLI-based BMI calculator that takes
#                weight and height as input, calculates BMI,
#                and classifies it into health categories.
# ============================================================


def calculate_bmi(weight, height):
    bmi = weight / (height ** 2)
    return round(bmi, 2)


def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25.0:
        return "Normal Weight"
    elif 25.0 <= bmi < 30.0:
        return "Overweight"
    else:
        return "Obese"


def get_valid_input(prompt, min_val, max_val, unit):
    while True:
        try:
            value = float(input(prompt))

            if value <= 0:
                print(f"  [!] Value must be greater than zero. Try again.\n")
                continue

            if not (min_val <= value <= max_val):
                print(f"  [!] Unusual {unit} entered ({value}). "
                      f"Expected range: {min_val} - {max_val}. Try again.\n")
                continue

            return value

        except ValueError:
            print("  [!] Invalid input. Please enter a numeric value.\n")


def show_bmi_table():
    print("\n  ----- BMI Reference Scale -----")
    print("  < 18.5          -->  Underweight")
    print("  18.5 to 24.9    -->  Normal Weight")
    print("  25.0 to 29.9    -->  Overweight")
    print("  30.0 and above  -->  Obese")
    print("  --------------------------------")


def health_tip(category):
    tips = {
        "Underweight"   : "You may need to eat more nutritious food. Consider seeing a dietitian.",
        "Normal Weight" : "You're in great shape! Keep up the healthy lifestyle.",
        "Overweight"    : "Try regular exercise and a balanced diet to stay on track.",
        "Obese"         : "It is advised to consult a healthcare professional for proper guidance."
    }
    return tips[category]


def main():
    print("\n" + "=" * 45)
    print("          BMI CALCULATOR")
    print("          Created by VISHNU S")
    print("=" * 45)
    print("  This tool calculates your Body Mass Index")
    print("  and tells you which health category")
    print("  you fall into based on your BMI value.")
    print("=" * 45)

    print("\n  Please enter the following details:\n")

    weight = get_valid_input("  Enter your weight (in kg)    : ", 10, 300, "weight (kg)")
    height = get_valid_input("  Enter your height (in meters): ", 0.5, 2.5, "height (m)")

    bmi      = calculate_bmi(weight, height)
    category = classify_bmi(bmi)
    tip      = health_tip(category)

    print("\n" + "=" * 45)
    print("              YOUR RESULTS")
    print("=" * 45)
    print(f"  Weight   : {weight} kg")
    print(f"  Height   : {height} m")
    print(f"  BMI      : {bmi}")
    print(f"  Category : {category}")
    print("=" * 45)
    print(f"\n  Health Tip:\n  {tip}")

    show_bmi_table()

    print("\n  Thank you for using the BMI Calculator!")
    print("  -- VISHNU S\n")


if __name__ == "__main__":
    main()