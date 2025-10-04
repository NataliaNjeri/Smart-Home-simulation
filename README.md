# 🇰🇪 Nairobi Smart Apartment Hub Simulation

This is a Python-based desktop application simulating a Smart Home Hub for a Nairobi apartment, complete with environmental sensors, actuators, security protocols, and a graphical user interface (GUI). The hub actively monitors temperature, humidity, and dust, adjusting systems like the thermostat and air purifier automatically, and manages a simple "home" or "away" security mode.

## ✨ Features

* **Environmental Monitoring:** Tracks Temperature, Humidity, and Dust levels.
* **Automated Climate Control:** Automatically adjusts the **Thermostat**, **Dehumidifier**, and **Air Purifier** based on sensor readings.
* **Security System:** Features **Arm/Disarm** modes and a **Panic Button** that triggers a **Siren**, turns on lights, and starts a **Security Camera**.
* **Routines:** Includes a **Morning Routine** to turn on bedroom lights, set the thermostat, and start the **Coffee Maker**.
* **Interactive GUI:** Built with Tkinter, featuring a dashboard view, manual controls, and a theme toggle (Dark/Light).
* **Clothing Recommendation:** Provides weather-based clothing advice based on temperature and humidity.

## 🛠️ Requirements

The project is built entirely in **Python** and relies only on standard libraries.

* Python 3.x
* `tkinter` (Usually included with standard Python installations)
* `random`, `time`, `messagebox` (Standard Python modules)

## 🚀 Installation & Setup

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/YourUsername/your-repo-name.git](https://github.com/YourUsername/your-repo-name.git)
    cd your-repo-name
    ```

2.  **Run the Application:**
    Since the project uses standard libraries, you can run the main file directly.

    ```bash
    python smart_apartment.py
    ```

    A graphical window titled "Nairobi Smart Apartment Hub" will open, and the **Morning Routine** will initiate automatically upon launch.

## 💻 Usage & Controls

The dashboard updates every **2 seconds** with simulated sensor data and device status.

| Panel | Control | Function |
| :--- | :--- | :--- |
| **Security & Routines** | `Arm Security 🛡️` | Switches the system to **'Away'** mode. Security checks are now active. |
| | `Disarm Security 🔑` | Switches the system to **'Home'** mode and deactivates any active security breach. |
| | `Panic Button 🚨` | Immediately triggers the full **security protocol** (siren, lights, camera recording). |
| | `Morning Routine 🌅` | Executes the morning sequence: lights, thermostat to 23°C, and coffee brewing. |
| **Manual Device Controls** | Toggle Buttons | Manually overrides the automation logic for the light, thermostat, air purifier, and coffee maker. |
| **Header** | `Toggle Theme 🌓` | Switches the dashboard appearance between **Dark** and **Light** modes. |

## 📐 Project Structure

The core logic is contained within a single file:

| **IT IS STILL UNDER 'EDITING 🥲'** |
