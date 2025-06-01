import tkinter as tk
from tkinter import ttk
import time
import timeit
import random

class SortingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Algorithm Visualizer")
        self.root.geometry("1000x600")
        self.root.configure(bg="black")

        self.data = []
        self.speed = tk.DoubleVar()
        self.algo = tk.StringVar()

        self.setup_ui()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TFrame", background="black")
        style.configure("TLabel", background="black", foreground="white")
        style.configure("TButton", background="gray", foreground="white")
        style.configure("TCombobox", fieldbackground="black", background="gray", foreground="white")
        style.map("TButton", background=[("active", "darkgray")])
        style.configure("TEntry", fieldbackground="black", foreground="white")

        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=10)

        ttk.Label(control_frame, text="Input (comma-separated):").grid(row=0, column=0, padx=5)
        self.input_entry = ttk.Entry(control_frame, width=30)
        self.input_entry.grid(row=0, column=1, padx=5)

        ttk.Button(control_frame, text="Generate Random", command=self.generate_random_input).grid(row=0, column=2, padx=5)

        ttk.Label(control_frame, text="Algorithm:").grid(row=0, column=3, padx=5)
        algo_menu = ttk.Combobox(control_frame, textvariable=self.algo,
                                 values=["Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort", "Quick Sort"],
                                 state="readonly")
        algo_menu.grid(row=0, column=4, padx=5)
        algo_menu.current(0)

        ttk.Label(control_frame, text="Speed:").grid(row=0, column=5, padx=5)
        speed_slider = ttk.Scale(control_frame, variable=self.speed, from_=0.01, to=1.0,
                                 length=100, orient='horizontal', command=self.update_speed_label)
        speed_slider.grid(row=0, column=6, padx=5)
        self.speed.set(0.1)

        self.speed_label = ttk.Label(control_frame, text=f"{self.speed.get():.2f}s")
        self.speed_label.grid(row=0, column=7, padx=5)

        ttk.Button(control_frame, text="Visualize", command=self.start_sort).grid(row=0, column=8, padx=5)

        self.canvas = tk.Canvas(self.root, width=900, height=300, bg='black', highlightthickness=0)
        self.canvas.pack(pady=10)

        self.log_box = tk.Text(self.root, height=10, wrap='word', bg='black', fg='white', insertbackground='white')
        self.log_box.pack(padx=10, fill='x')

        self.status = ttk.Label(self.root, text="Complexity Info:")
        self.status.pack(pady=5)

    def update_speed_label(self, val):
        self.speed_label.config(text=f"{float(val):.2f}s")

    def draw_data(self, data, color_array):
        self.canvas.delete("all")
        c_height = 300
        c_width = 900
        x_width = c_width / (len(data) + 1)
        offset = 10
        spacing = 5

        max_val = max(data) if data else 1
        normalized_data = [(i / max_val if max_val != 0 else 0) for i in data]

        for i, height in enumerate(normalized_data):
            x0 = i * x_width + offset + spacing
            y0 = c_height - height * 250
            x1 = (i + 1) * x_width + offset
            y1 = c_height

            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color_array[i], outline="")
            self.canvas.create_text(x0 + 2, y0, anchor=tk.SW, text=str(data[i]), fill='white', font=("Arial", 10))

        self.root.update_idletasks()

    def log(self, message):
        self.log_box.insert(tk.END, message + '\n')
        self.log_box.see(tk.END)

    def generate_random_input(self):
        random_data = [random.randint(1, 100) for _ in range(random.randint(5, 20))]
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, ','.join(map(str, random_data)))

    def start_sort(self):
        self.log_box.delete(1.0, tk.END)
        raw = self.input_entry.get()

        if not raw.strip():
            self.log("Input is empty. Please enter or generate a list of integers.")
            return

        try:
            self.data = list(map(int, raw.strip().split(',')))
        except ValueError:
            self.log("Invalid input. Please enter comma-separated integers.")
            return

        if not self.data:
            self.log("No data to sort.")
            return

        algorithm = self.algo.get()
        speed_val = self.speed.get()
        start_time = timeit.default_timer()

        if algorithm == "Bubble Sort":
            self.bubble_sort(self.data)
            self.status.config(text="Bubble Sort | Time: O(n²) | Space: O(1)")
        elif algorithm == "Selection Sort":
            self.selection_sort(self.data)
            self.status.config(text="Selection Sort | Time: O(n²) | Space: O(1)")
        elif algorithm == "Insertion Sort":
            self.insertion_sort(self.data)
            self.status.config(text="Insertion Sort | Time: O(n²) | Space: O(1)")
        elif algorithm == "Merge Sort":
            self.merge_sort(self.data, 0, len(self.data) - 1)
            self.draw_data(self.data, ['green'] * len(self.data))
            self.status.config(text="Merge Sort | Time: O(n log n) | Space: O(n)")
        elif algorithm == "Quick Sort":
            self.quick_sort(self.data, 0, len(self.data) - 1)
            self.draw_data(self.data, ['green'] * len(self.data))
            self.status.config(text="Quick Sort | Time: O(n log n) avg | Space: O(log n)")

        end_time = timeit.default_timer()
        runtime = end_time - start_time
        self.log(f"Total Runtime: {runtime:.6f} seconds")

    

    def bubble_sort(self, data):
        for i in range(len(data)):
            for j in range(len(data) - i - 1):
                self.log(f"Comparing {data[j]} and {data[j + 1]}")
                if data[j] > data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]
                    self.log(f"Swapped {data[j]} and {data[j + 1]}")
                    self.draw_data(data, ['blue' if x == j or x == j + 1 else 'gray' for x in range(len(data))])
                    time.sleep(self.speed.get())
        self.draw_data(data, ['green'] * len(data))

    def selection_sort(self, data):
        for i in range(len(data)):
            min_idx = i
            for j in range(i + 1, len(data)):
                self.log(f"Comparing {data[j]} and {data[min_idx]}")
                if data[j] < data[min_idx]:
                    min_idx = j
            self.log(f"Swapping {data[i]} and {data[min_idx]}")
            data[i], data[min_idx] = data[min_idx], data[i]
            self.draw_data(data, ['blue' if x == i or x == min_idx else 'gray' for x in range(len(data))])
            time.sleep(self.speed.get())
        self.draw_data(data, ['green'] * len(data))

    def insertion_sort(self, data):
        for i in range(1, len(data)):
            key = data[i]
            j = i - 1
            self.log(f"Inserting {key} into sorted part")
            while j >= 0 and data[j] > key:
                self.log(f"{data[j]} > {key}, shifting {data[j]} to the right")
                data[j + 1] = data[j]
                j -= 1
                self.draw_data(data, ['blue' if x == j + 1 else 'gray' for x in range(len(data))])
                time.sleep(self.speed.get())
            data[j + 1] = key
            self.log(f"Placed {key} at position {j + 1}")
        self.draw_data(data, ['green'] * len(data))

    def merge_sort(self, data, left, right):
        if left < right:
            mid = (left + right) // 2
            self.merge_sort(data, left, mid)
            self.merge_sort(data, mid + 1, right)
            self.merge(data, left, mid, right)

    def merge(self, data, left, mid, right):
        self.log(f"Merging from {left} to {right}")

        L = data[left:mid + 1]
        R = data[mid + 1:right + 1]

        i = j = 0
        k = left

        while i < len(L) and j < len(R):
            if L[i] <= R[j]:
                self.log(f"Placing {L[i]} from left")
                data[k] = L[i]
                i += 1
            else:
                self.log(f"Placing {R[j]} from right")
                data[k] = R[j]
                j += 1
            k += 1  

        while i < len(L):
            self.log(f"Placing remaining {L[i]} from left")
            data[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            self.log(f"Placing remaining {R[j]} from right")
            data[k] = R[j]
            j += 1
            k += 1

        
        self.draw_data(data, [
            'blue' if left <= x <= right else 'gray'
            for x in range(len(data))
        ])
        time.sleep(self.speed.get())



    def quick_sort(self, data, low, high):
        if low < high:
            pi = self.partition(data, low, high)
            self.quick_sort(data, low, pi - 1)
            self.quick_sort(data, pi + 1, high)

    def partition(self, data, low, high):
        pivot = data[high]
        i = low - 1
        self.log(f"Pivot is {pivot}")
        for j in range(low, high):
            self.log(f"Comparing {data[j]} with pivot {pivot}")
            if data[j] < pivot:
                i += 1
                data[i], data[j] = data[j], data[i]
                self.log(f"Swapped {data[i]} and {data[j]}")
                self.draw_data(data, ['blue' if x == i or x == j else 'gray' for x in range(len(data))])
                time.sleep(self.speed.get())
        data[i + 1], data[high] = data[high], data[i + 1]
        self.log(f"Swapped pivot {data[i + 1]} with {data[high]}")
        self.draw_data(data, ['blue' if x == i + 1 or x == high else 'gray' for x in range(len(data))])
        time.sleep(self.speed.get())
        return i + 1


if __name__ == '__main__':
    root = tk.Tk()
    app = SortingVisualizer(root)
    root.mainloop()
