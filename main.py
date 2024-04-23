import tkinter as tk
from tkinter import simpledialog, Listbox
import pyautogui
import time
from tkinter import ttk
from pynput import mouse
import keyboard
import threading

class AutoClicker:
    def __init__(self):
        self.locations = []
        self.thread = None
        self.running = False

    def add_location(self, x, y):
        self.locations.append((x, y))
        return f"Location added: {x}, {y}"

    def delete_location(self, index):
        if 0 <= index < len(self.locations):
            del self.locations[index]

    def execute_thread(self, count, interval):
        try:
            for i in range(count):
                if not self.running:
                    break
                for loc in self.locations:
                    pyautogui.click(x=loc[0], y=loc[1])
                    sleep_time = 0
                    while sleep_time < interval and self.running:
                        time.sleep(min(0.1, interval - sleep_time))
                        sleep_time += 0.1
        except KeyboardInterrupt:
            print("Program exited.")
        finally:
            self.running = False

    def execute(self, count, interval):
        if not self.thread or not self.thread.is_alive():
            self.running = True
            self.thread = threading.Thread(target=self.execute_thread, args=(count, interval))
            self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

class AutoClickerGUI:
    def __init__(self, root):
        self.root = root
        self.autoclicker = AutoClicker()
        self.stop_key = "F6"

        self.x_var = tk.StringVar(value="0")
        self.y_var = tk.StringVar(value="0")
        self.click_interval_var = tk.StringVar(value="5")
        self.count_var = tk.StringVar(value="10")
        self.locations_frame = tk.Frame(root)
        self.setup_ui()
        self.bind_stop_key()


    def setup_ui(self):
        root = self.root
        root.title("AutoClicker GUI")

        # Frame for entries and buttons
        frame = tk.Frame(root)
        frame.pack()

        entry_width = 6
        # Entry for X coordinate
        x_label = ttk.Label(frame, text="X:")
        x_label.grid(row=0, column=0)
        x_entry = ttk.Entry(frame, textvariable=self.x_var, width=entry_width)
        x_entry.grid(row=0, column=1)

        # Entry for Y coordinate
        y_label = ttk.Label(frame, text="Y:")
        y_label.grid(row=0, column=2)
        y_entry = ttk.Entry(frame, textvariable=self.y_var, width=entry_width)
        y_entry.grid(row=0, column=3)

        # Pick location button
        pick_location_btn = tk.Button(frame, text="Pick Location", command=self.pick_location)
        pick_location_btn.grid(row=1, column=0, columnspan=2)

        # Add location button
        add_location_btn = tk.Button(frame, text="Add Location", command=self.add_location)
        add_location_btn.grid(row=1, column=2, columnspan=2)

        # Set click interval entry
        interval_label = tk.Label(frame, text="Click Interval (s):")
        interval_label.grid(row=2, column=0)
        interval_entry = ttk.Entry(frame, textvariable=self.click_interval_var, width=entry_width)
        interval_entry.grid(row=2, column=1)

        # Set count entry
        count_label = tk.Label(frame, text="Counts:")
        count_label.grid(row=3, column=0)
        count_entry = ttk.Entry(frame, textvariable=self.count_var, width=entry_width)
        count_entry.grid(row=3, column=1)

        # Execute button
        self.execute_btn = tk.Button(frame, text="Execute", command=self.execute)
        self.execute_btn.grid(row=4, columnspan=2)

        # Stop button
        self.stop_btn = tk.Button(frame, text=f"Stop ({self.stop_key})", command=self.stop)
        self.stop_btn.config(state=tk.DISABLED)
        self.stop_btn.grid(row=4, column=2, columnspan=2)

        # Location display panel
        self.locations_frame.pack()

    def bind_stop_key(self):
        # Binding the stop function to the stop key
        keyboard.add_hotkey(self.stop_key, self.stop)

    def stop(self):
        print('stopped')
        self.autoclicker.stop()
        self.execute_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)

    def start_mouse_listener(self):
        listener = mouse.Listener(on_click=self.on_click)
        listener.start()

    def on_click(self, x, y, button, pressed):
        print('{0} at {1}'.format(
            'Pressed' if pressed else 'Released',
            (x, y)))
        if pressed:
            x, y = pyautogui.position()
            picked_location = (x, y)
            self.autoclicker.add_location(x, y)
            self.update_locations_display()
            return False

    def pick_location(self):
        self.start_mouse_listener()


    def add_location(self):
        x = int(self.x_var.get())
        y = int(self.y_var.get())
        self.autoclicker.add_location(x, y)
        self.update_locations_display()

    def delete_location(self, index):
        self.autoclicker.delete_location(index)
        self.update_locations_display()

    def update_locations_display(self):
        # Clear the current display
        for widget in self.locations_frame.winfo_children():
            widget.destroy()

        locations_label = tk.Label(self.locations_frame, text=f'Added Locations ({len(self.autoclicker.locations)})')
        locations_label.grid(row=0, column=0, columnspan=2)
        # Add updated list of locations with delete buttons
        for index, loc in enumerate(self.autoclicker.locations):
            loc_label = tk.Label(self.locations_frame, text=f"[{index+1}]: {loc[0]}, {loc[1]}")
            loc_label.grid(row=index+1, column=0)
            del_btn = tk.Button(self.locations_frame, text="Delete", command=lambda idx=index: self.delete_location(idx))
            del_btn.grid(row=index+1, column=1)

    def execute(self):
        print('running...')
        interval = float(self.click_interval_var.get())
        count = int(self.count_var.get())
        self.autoclicker.execute(count, interval)
        self.execute_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x300")
    app = AutoClickerGUI(root)
    root.attributes('-topmost', True)

    root.mainloop()

