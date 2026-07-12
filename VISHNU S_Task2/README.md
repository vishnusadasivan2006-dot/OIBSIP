# ⚖️ BMI Calculator (Body Mass Index)

A user-friendly Python application designed to calculate Body Mass Index (BMI) based on user inputs for weight and height, offering classification and practical health advice.

Created by **[Vishnu S](https://github.com/vishnusadasivan2006)** as part of the **Oasis Infobyte Internship Project (OIBSIP)**.

---

## 🌟 Key Features

- 🧮 **Accurate Calculation**: Automatically calculates the Body Mass Index rounded to 2 decimal places.
- 📊 **Official BMI Reference Scale**: Classifies the results into the standard World Health Organization (WHO) categories:
  - **Underweight** (< 18.5)
  - **Normal Weight** (18.5 – 24.9)
  - **Overweight** (25.0 – 29.9)
  - **Obese** (30.0 and above)
- 🛡️ **Robust Input Validation**: 
  - Prevents non-numeric values.
  - Ensures inputs are greater than zero.
  - Detects outlier inputs (e.g. height outside 0.5m – 2.5m, weight outside 10kg – 300kg) to avoid typos.
- 💡 **Personalized Health Tips**: Provides helpful next steps based on your results.

---

## 🚀 Running the Calculator

No external Python dependencies are needed. Simply run the script using:

```bash
python "VISHNU S_2.py"
```

---

## 💬 Sample Execution

```text
=============================================
              BMI CALCULATOR
              Created by VISHNU S
=============================================
  This tool calculates your Body Mass Index
  and tells you which health category
  you fall into based on your BMI value.
=============================================

  Please enter the following details:

  Enter your weight (in kg)    : 70
  Enter your height (in meters): 1.75

=============================================
                  YOUR RESULTS
=============================================
  Weight   : 70.0 kg
  Height   : 1.75 m
  BMI      : 22.86
  Category : Normal Weight
=============================================

  Health Tip:
  You're in great shape! Keep up the healthy lifestyle.

  ----- BMI Reference Scale -----
  < 18.5          -->  Underweight
  18.5 to 24.9    -->  Normal Weight
  25.0 to 29.9    -->  Overweight
  30.0 and above  -->  Obese
  --------------------------------

  Thank you for using the BMI Calculator!
  -- VISHNU S
```

---

## 📂 Folder Structure

```text
├── VISHNU S_Task2/
│   ├── VISHNU S_2.py       # Main Python BMI calculation script
│   └── README.md           # Project documentation (this file)
```
