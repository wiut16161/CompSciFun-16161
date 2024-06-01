import pandas as pd
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from utilities import count_param, attribute_extraction
from const import START_YEAR, COUNTRY, END_YEAR, MID_YEAR, OBS_MATDEATHS, FINAL_ENV, FINAL_PM, FINAL_MMR, PM_PRECRISIS, MMR_PRECRISIS, TOTAL_ENV, LIVE_BIRTHS

data = pd.read_csv('main_data.csv')

# Select only the important and consistent columns
important_columns = [
    "iso_alpha_3_code",
    "year_start",
    "year_end",
    "year_mid",
    "obs_matdeaths",
    "final_env",
    "final_pm",
    "final_mmr",
    "final_pm_before_crisis",
    "final_mmr_before_crisis",
    "env_total_calculated_from_lifetables",
    "live_births_calculated_from_birthsdata"
]

# Filter the DataFrame to keep only the important columns
data_filtered = data[important_columns].copy()

# Converting date columns to numeric objects
date_columns = ["year_start", "year_end", "year_mid"]
for column in date_columns:
    data_filtered.loc[:, column] = pd.to_numeric(data_filtered[column], errors='coerce')

# Converting numeric columns to float or int
numeric_columns = [
    "obs_matdeaths",
    "final_env",
    "final_pm",
    "final_mmr",
    "final_pm_before_crisis",
    "final_mmr_before_crisis",
    "env_total_calculated_from_lifetables",
    "live_births_calculated_from_birthsdata"
]

for column in date_columns:
    data_filtered.loc[:, column] = pd.to_numeric(data_filtered[column], errors='coerce').fillna(0).astype(int)

for column in numeric_columns:
    data_filtered.loc[:, column] = pd.to_numeric(data_filtered[column], errors='coerce')

labels = {
    START_YEAR: ["Year Started", "Number of cases"],
    END_YEAR: ["Year ended", "Number of cases"],
    MID_YEAR: ["Year in the middle", "Number of cases"],
    COUNTRY: ["Countries", "Number of cases"],
    PM_PRECRISIS: ["PM Before crisis", "PM results"],
    MMR_PRECRISIS: ["MMR Before Crisis", "MMR results"],
    OBS_MATDEATHS: ["Maternal Death", "The number of cases"],
    FINAL_ENV: ["ENV Final", "Final ENV results"],
    FINAL_PM: ["PM Final", "Final PM results"],
    FINAL_MMR: ["MMR Final", "Final MMR results"],
    TOTAL_ENV: ["Total ENV", "ENV results"],
    LIVE_BIRTHS: ["Live births", "The number of births"]
}

# Initialize Tkinter
root = tk.Tk()
root.title("Dashboard")
root.geometry("1200x800")
root.state("zoomed")

# Create matplotlib axes
fig_line, ax_line = plt.subplots()
fig_hist, ax_hist = plt.subplots()
fig_bar, ax_bar = plt.subplots()
fig_pie, ax_pie = plt.subplots()

# Create upper frame for charts
upper_charts_frame = tk.Frame(root)
upper_charts_frame.pack(side="top", fill="both", expand=True)

# Create lower frame for charts
lower_charts_frame = tk.Frame(root)
lower_charts_frame.pack(side="bottom", fill="both", expand=True)

canvas_bar = FigureCanvasTkAgg(fig_bar, master=lower_charts_frame)
canvas_bar.get_tk_widget().pack(side="bottom", fill="both", expand=True)

canvas_line = FigureCanvasTkAgg(fig_line, master=upper_charts_frame)
canvas_line.get_tk_widget().pack(side="left", fill="both", expand=True)

canvas_pie = FigureCanvasTkAgg(fig_pie, master=upper_charts_frame)
canvas_pie.get_tk_widget().pack(side="left", fill="both", expand=True)

def chart_draw(data):
    if data not in labels:
        print("Unavailable")
        return
    data_to_draw = count_param(data)
    its_keys = list(data_to_draw.keys())
    in_numbers = list(data_to_draw.values())

    if data in ["year_start", "end_year", "year_mid"]:
        draw_pie(in_numbers, its_keys)
        draw_bar(its_keys, in_numbers, labels[data])
        draw_line(its_keys, in_numbers, labels[data])

    elif data in ["iso_alpha_3_code"]:
        heading_text(labels[data][0])
        draw_bar(its_keys, in_numbers, labels[data])
        draw_pie(in_numbers, its_keys)
        draw_line("", "", "", False)

    else:
        print("This category is not available")

# Function to draw pie chart
def draw_pie(values, legend):
    ax_pie.clear()
    ax_pie.pie(values, labels=None)
    ax_pie.legend(legend, loc=(-0.41, 0.5))
    canvas_pie.draw()

# Function to draw bar chart
def draw_bar(xvalues, yvalues, labels):
    ax_bar.clear()
    ax_bar.bar(xvalues, yvalues)
    ax_bar.set_xlabel(labels[0], fontsize=16)
    ax_bar.set_ylabel(labels[1], fontsize=16)
    ax_bar.tick_params(axis='x', labelrotation=90)  # Rotate x-axis labels
    canvas_bar.draw()


# Function to draw line chart
def draw_line(x, y, labels, isclear=True):
    ax_line.clear()
    if isclear:
        ax_line.plot(x, y)
        ax_line.scatter(x, y)
        ax_line.set_xlabel(labels[0], fontsize=16)
        ax_line.set_ylabel(labels[1], fontsize=16)
    canvas_line.draw()

def heading_text(new_text):
    heading.config(text=new_text)

# Create heading
heading = tk.Label(root, text="Dashboard", font=("monospace", 25))
heading.pack(side="top")

# Call chart_draw with START_YEAR as an example
chart_draw(START_YEAR)

root.protocol("WM_DELETE_WINDOW", root.quit)
root.mainloop()
