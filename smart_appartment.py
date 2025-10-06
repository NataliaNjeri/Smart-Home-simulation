import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import time
import random

# --- Device Classes (Sensors & Actuators) ---

class SmartSensor:
    def __init__(self, name, min_val, max_val, unit):
        self.name = name
        self.value = 0
        self.min_val = min_val
        self.max_val = max_val
        self.unit = unit

    def read_data(self):
        # Reduced variance for a more stable environment simulation
        self.value = random.uniform(self.min_val, self.max_val)
        return round(self.value, 2)

class SmartActuator:
    def __init__(self, name):
        self.name = name
        self.status = "off"
    
    def toggle(self):
        if self.status == "on":
            self.turn_off()
        else:
            self.turn_on()

    def turn_on(self):
        self.status = "on"

    def turn_off(self):
        self.status = "off"

class SmartLight(SmartActuator):
    def __init__(self, location):
        super().__init__(f"Light in the {location}")
        self.brightness = 0

    def set_brightness(self, level):
        self.brightness = level

class SmartThermostat(SmartActuator):
    def __init__(self, location):
        super().__init__(f"Thermostat in the {location}")
        self.target_temp = 24

    def set_temperature(self, temp):
        self.target_temp = temp

class SmartCoffeeMaker(SmartActuator):
    def __init__(self):
        super().__init__("Coffee Maker")
    
    # FIX: Removed self.after() call and simplified the alert mechanism
    def start_brew(self, gui_alert_func=None): 
        if self.status == "on":
            if gui_alert_func:
                gui_alert_func("Coffee Status", "Brewing delicious coffee... Your coffee is ready!")
        else:
            if gui_alert_func:
                gui_alert_func("Coffee Status", "Please turn on the coffee maker first.")

class DoorSensor(SmartSensor):
    def __init__(self, location):
        super().__init__(f"Door Sensor ({location})", 0, 1, "")
        self._is_open = False

    def is_open(self):
        # Significantly reduced chance of random security trigger (0.5% chance)
        if random.random() > 0.995:
            self._is_open = True
        else:
            self._is_open = False
        return self._is_open

class SmartSiren(SmartActuator):
    def __init__(self):
        super().__init__("Alarm Siren")

    def sound_alarm(self):
        if self.status == "on":
            pass

class SmartCamera(SmartActuator):
    def __init__(self, location):
        super().__init__(f"Camera in the {location}")
        self.is_recording = False

    def start_recording(self):
        self.is_recording = True


# --- The Smart Home Hub Backend Logic (Security Fix Applied) ---

class SmartHome:
    def __init__(self):
        # Sensors
        self.temp_sensor = SmartSensor("Temperature Sensor", 20, 30, "°C")
        self.humidity_sensor = SmartSensor("Humidity Sensor", 40, 80, "%")
        self.dust_sensor = SmartSensor("Dust Sensor", 0, 100, "μg/m³")
        self.motion_sensor = SmartSensor("Motion Sensor", 0, 1, "")
        self.door_sensor = DoorSensor("Main Door")
        
        # Actuators
        self.living_room_thermostat = SmartThermostat("living room")
        self.dehumidifier = SmartActuator("Dehumidifier")
        self.air_purifier = SmartActuator("Air Purifier")
        self.living_room_light = SmartLight("living room")
        self.bedroom_light = SmartLight("bedroom")
        self.coffee_maker = SmartCoffeeMaker()
        self.siren = SmartSiren()
        self.security_camera = SmartCamera("living room")
        
        # System State
        self.mode = "home" # Modes: 'home', 'away'
        self.security_breach_active = False 
        
        self.breach_reasons = [
            "Unauthorized entry through a compromised lock.",
            "Motion detected in the main living area while apartment is empty.",
            "Main door sensor triggered while security is armed.",
            "Forced entry detected at a window on the ground floor."
        ]
        self.gui_alert_func = None 

    def set_gui_alerter(self, func):
        self.gui_alert_func = func

    def check_environment(self):
        temp = self.temp_sensor.read_data()
        humidity = self.humidity_sensor.read_data()
        dust = self.dust_sensor.read_data()
        
        # Automated Environmental Logic
        if temp > self.living_room_thermostat.target_temp + 1 and self.living_room_thermostat.status == "off":
            self.living_room_thermostat.turn_on()
        elif temp < self.living_room_thermostat.target_temp - 1 and self.living_room_thermostat.status == "on":
            self.living_room_thermostat.turn_off()

        if humidity > 70 and self.dehumidifier.status == "off":
            self.dehumidifier.turn_on()
        elif humidity < 50 and self.dehumidifier.status == "on":
            self.dehumidifier.turn_off()

        if dust > 50 and self.air_purifier.status == "off":
            self.air_purifier.turn_on()
        elif dust < 20 and self.air_purifier.status == "on":
            self.air_purifier.turn_off()

        return temp, humidity, dust

    def check_security(self):
        if self.security_breach_active:
            return True
            
        is_breach = False
        reason = ""
        
        if self.mode == "away":
            # Motion (simulated 1) or Door Open (simulated 1)
            if self.door_sensor.is_open() or random.random() > 0.95: 
                is_breach = True
                if self.door_sensor._is_open:
                    reason = random.choice(self.breach_reasons)
                else:
                    reason = "Motion detected in the main living area while apartment is empty."

        if is_breach:
            self.trigger_security_protocol(reason)
            return True
        return False

    def trigger_security_protocol(self, reason):
        self.security_breach_active = True 
        
        if self.gui_alert_func:
             self.gui_alert_func("SECURITY BREACH", f"INTRUDER ALERT! Reason: {reason}", is_critical=True)
        
        # Actuate systems
        self.siren.turn_on()
        self.siren.sound_alarm()
        self.living_room_light.turn_on()
        self.bedroom_light.turn_on()
        self.security_camera.turn_on()
        self.security_camera.start_recording()

    def morning_routine(self):
        if self.gui_alert_func:
            self.gui_alert_func("Routine Status", "Initiating Morning Routine...")
        self.bedroom_light.turn_on()
        self.bedroom_light.set_brightness(40)
        self.coffee_maker.turn_on()
        # FIX: Pass the GUI alert function here
        self.coffee_maker.start_brew(lambda title, msg: messagebox.showinfo(title, msg)) 
        self.living_room_thermostat.set_temperature(23)
        if self.gui_alert_func:
            self.gui_alert_func("Routine Status", "Morning routine complete.")

# --------------------------
# --- The Tkinter GUI Code (System Log Removed) ---
# --------------------------

class SmartHomeGUI(tk.Tk):
    def __init__(self, smart_home_system):
        super().__init__()
        self.smart_home = smart_home_system
        self.smart_home.set_gui_alerter(self.display_alert)
        
        self.title("Nairobi Smart Apartment Hub")
        self.geometry("500x550") 
        self.current_theme = "dark" 
        
        self.create_widgets()
        self.apply_styles()
        
        self.after(2000, self.update_dashboard) # Start the update timer
        
        # Start initial routine (after GUI is ready)
        self.smart_home.morning_routine() 
        messagebox.showinfo("Routine Initiated", "The morning routine has been started!")


    def display_alert(self, title, message, is_critical=False):
        """Custom alert function to replace logging and handle critical messages."""
        if is_critical:
            messagebox.showerror(title, message)
        else:
            messagebox.showinfo(title, message)


    def toggle_theme(self):
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        self.apply_styles()

    def apply_styles(self):
        # Define Color Palette
        if self.current_theme == "dark":
            main_bg = "#1a1a2e"
            panel_bg = "#2c2b3f"
            text_color = "#e0e0e0"
            button_bg = "#0f3460"
            
        else: 
            main_bg = "#f0f0f0"
            panel_bg = "#ffffff"
            text_color = "#333333"
            button_bg = "#e0e0e0"
        
        self.config(bg=main_bg)

        # Style for Frames and Labels
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TFrame', background=main_bg)
        style.configure('Panel.TFrame', background=panel_bg, borderwidth=1, relief='solid', bordercolor=text_color)
        style.configure('TLabel', background=main_bg, foreground=text_color, font=('Arial', 10))
        style.configure('Panel.TLabel', background=panel_bg, foreground=text_color, font=('Arial', 10))
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'), background=panel_bg, foreground=text_color)
        
        button_style = {'bg': button_bg, 'fg': text_color, 'relief': 'flat', 'activebackground': button_bg, 'activeforeground': text_color}
        
        # Apply button styles
        for btn in [self.arm_btn, self.disarm_btn, self.morning_btn, self.theme_btn, 
                    self.light_btn, self.thermostat_btn, self.air_purifier_btn, self.coffee_maker_btn]:
            if btn.winfo_exists():
                btn.config(**button_style)
        
        if self.panic_btn.winfo_exists():
            self.panic_btn.config(bg="#ff4d4d", fg="white", activebackground="#cc0000")
            
        # Apply panel background to all frames
        for widget in self.winfo_children():
            if isinstance(widget, ttk.Frame) and widget.winfo_name() != "!frame":
                 widget.configure(style='Panel.TFrame')
                 for child in widget.winfo_children():
                     if isinstance(child, ttk.Label):
                         child.configure(style='Panel.TLabel')

        self.title_label.config(bg=main_bg, fg=text_color)
        self.status_label.config(bg=main_bg) 


    def create_widgets(self):
        # Main container frame
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill='both', expand=True)
        
        # --- Header with Title and Theme Toggle ---
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill='x', pady=(0, 10))
        
        self.title_label = tk.Label(header_frame, text="Nairobi Smart Apartment", font=("Arial", 24, "bold"))
        self.title_label.pack(side='left', padx=(0, 10))
        
        self.theme_btn = tk.Button(header_frame, text="Toggle Theme 🌓", command=self.toggle_theme, width=15)
        self.theme_btn.pack(side='right')

        # --- Status Label ---
        self.status_label = tk.Label(main_frame, text=f"Status: {self.smart_home.mode.capitalize()} Mode", font=("Arial", 16))
        self.status_label.pack(pady=(5, 10))

        # --- Security & Routines Panel ---
        security_frame = ttk.Frame(main_frame, padding="15")
        security_frame.pack(fill='x', pady=5)
        ttk.Label(security_frame, text="🔒 Security & Routines ☀️", style='Header.TLabel').grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        self.arm_btn = tk.Button(security_frame, text="Arm Security 🛡️", command=self.arm_security, width=20)
        self.disarm_btn = tk.Button(security_frame, text="Disarm Security 🔑", command=self.disarm_security, width=20)
        self.morning_btn = tk.Button(security_frame, text="Morning Routine 🌅", command=self.start_morning_routine, width=20)
        self.panic_btn = tk.Button(security_frame, text="Panic Button 🚨", command=self.trigger_panic, width=20)
        
        self.arm_btn.grid(row=1, column=0, padx=5, pady=5, sticky='ew')
        self.disarm_btn.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        self.morning_btn.grid(row=2, column=0, padx=5, pady=5, sticky='ew')
        self.panic_btn.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        
        security_frame.grid_columnconfigure(0, weight=1)
        security_frame.grid_columnconfigure(1, weight=1)

        # --- Environmental Dashboard Panel ---
        sensor_frame = ttk.Frame(main_frame, padding="15")
        sensor_frame.pack(fill='x', pady=5)
        ttk.Label(sensor_frame, text="📊 Environmental Dashboard", style='Header.TLabel').pack(pady=(0, 10))
        
        self.temp_label = ttk.Label(sensor_frame, text="🌡️ Temperature: -- °C")
        self.humidity_label = ttk.Label(sensor_frame, text="💧 Humidity: -- %")
        self.dust_label = ttk.Label(sensor_frame, text="💨 Dust: -- μg/m³")
        self.clothing_label = ttk.Label(sensor_frame, text="👕 Recommended Clothing: --", wraplength=450)
        
        self.temp_label.pack(fill='x', pady=2)
        self.humidity_label.pack(fill='x', pady=2)
        self.dust_label.pack(fill='x', pady=2)
        self.clothing_label.pack(fill='x', pady=5)

        # --- Manual Device Controls Panel ---
        device_frame = ttk.Frame(main_frame, padding="15")
        device_frame.pack(fill='x', pady=5)
        ttk.Label(device_frame, text="⚙️ Manual Device Controls", style='Header.TLabel').grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        self.light_btn = tk.Button(device_frame, text="💡 Living Room Light", command=self.toggle_light, width=20)
        self.thermostat_btn = tk.Button(device_frame, text="❄️ Thermostat", command=self.toggle_thermostat, width=20)
        self.air_purifier_btn = tk.Button(device_frame, text="🌬️ Air Purifier", command=self.toggle_air_purifier, width=20)
        self.coffee_maker_btn = tk.Button(device_frame, text="☕ Coffee Maker", command=self.toggle_coffee_maker, width=20)

        self.light_btn.grid(row=1, column=0, padx=5, pady=5, sticky='ew')
        self.thermostat_btn.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        self.air_purifier_btn.grid(row=2, column=0, padx=5, pady=5, sticky='ew')
        self.coffee_maker_btn.grid(row=2, column=1, padx=5, pady=5, sticky='ew')

        device_frame.grid_columnconfigure(0, weight=1)
        device_frame.grid_columnconfigure(1, weight=1)


    def update_dashboard(self):
        """Called by the timer to update sensor readings and run logic."""
        temp, humidity, dust = self.smart_home.check_environment()
        
        # Update Sensor Data
        self.temp_label.config(text=f"🌡️ Temperature: {temp}°C")
        self.humidity_label.config(text=f"💧 Humidity: {humidity}%")
        self.dust_label.config(text=f"💨 Dust: {dust} μg/m³")
        self.update_clothing_recommendation(temp, humidity)
        
        # Check Security
        if self.smart_home.check_security():
            self.status_label.config(text="Status: ⚠️ SECURITY BREACH!", fg="red", font=("Arial", 16, "bold"))
        else:
            self.status_label.config(text=f"Status: {self.smart_home.mode.capitalize()} Mode")
            if self.smart_home.mode == "home":
                self.status_label.config(fg="#aaffaa", font=("Arial", 16, "bold"))
            else:
                self.status_label.config(fg="#ffcc00", font=("Arial", 16, "bold"))

        # Update Device Button States
        self.light_btn.config(text=f"💡 Light: {'ON' if self.smart_home.living_room_light.status == 'on' else 'OFF'}")
        self.thermostat_btn.config(text=f"❄️ Thermostat: {'ON' if self.smart_home.living_room_thermostat.status == 'on' else 'OFF'}")
        self.air_purifier_btn.config(text=f"🌬️ Air Purifier: {'ON' if self.smart_home.air_purifier.status == 'on' else 'OFF'}")
        self.coffee_maker_btn.config(text=f"☕ Coffee Maker: {'ON' if self.smart_home.coffee_maker.status == 'on' else 'OFF'}")
        
        # Schedule the next update
        self.after(2000, self.update_dashboard)

    def update_clothing_recommendation(self, temp, humidity):
        if temp >= 25:
            rec_text = "Light, loose-fitting clothes. Avoid heavy fabrics to stay cool. ☀️"
            if humidity > 70:
                rec_text = "Light, loose-fitting clothes. High humidity makes it feel warmer. 🥵"
        elif 15 <= temp < 25:
            rec_text = "Light jacket or sweater recommended. Layers are a great idea. 👕"
        else:
            rec_text = "A jacket, long pants, and layers are a must. Avoid light clothing. 🧥"
        self.clothing_label.config(text=f"👕 Recommended Clothing: {rec_text}")

    def arm_security(self):
        self.smart_home.mode = "away"
        self.update_dashboard()
        messagebox.showinfo("Security Alert", "Security System Armed.")
        
    def disarm_security(self):
        self.smart_home.mode = "home"
        self.smart_home.security_breach_active = False 
        self.smart_home.siren.turn_off() 
        self.smart_home.living_room_light.turn_off()
        self.smart_home.bedroom_light.turn_off()
        self.update_dashboard()
        messagebox.showinfo("Security Alert", "Security System Disarmed.")

    def start_morning_routine(self):
        self.smart_home.morning_routine()
        
    def trigger_panic(self):
        self.smart_home.trigger_security_protocol("Panic button activated by resident.")
        messagebox.showwarning("Alert Sent", "The authorities have been alerted. Please hang tight.")
        self.after(5000, self.issue_resolved_message) 
        
    def issue_resolved_message(self):
        self.disarm_security()
        messagebox.showinfo("Security Status Update", "Issue sorted out. Your apartment is SAFE.")
        
    # --- Toggle Functions (Manual Controls) ---
    def toggle_light(self):
        self.smart_home.living_room_light.toggle()
        self.update_dashboard()
            
    def toggle_thermostat(self):
        self.smart_home.living_room_thermostat.toggle()
        self.update_dashboard()

    def toggle_air_purifier(self):
        self.smart_home.air_purifier.toggle()
        self.update_dashboard()
            
    def toggle_coffee_maker(self):
        if self.smart_home.coffee_maker.status == "on":
            # FIX: Pass the GUI alert function here
            self.smart_home.coffee_maker.start_brew(lambda title, msg: messagebox.showinfo(title, msg))
        else:
            self.smart_home.coffee_maker.turn_on()
            messagebox.showinfo("Coffee Status", "Coffee Maker turned ON, ready to brew.")
        self.update_dashboard()

# --- Main Application Launch ---
if __name__ == "__main__":
    app = SmartHomeGUI(SmartHome())
    app.mainloop()
