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
    data_filtered.loc[:, column] = pd.to_numeric(data_filtered[column], errors='coerce').fillna(0).astype(int)

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

# Create matplotlib axes for four different charts
fig_line_1, ax_line_1 = plt.subplots()
fig_line_2, ax_line_2 = plt.subplots()
fig_bar_1, ax_bar_1 = plt.subplots()
fig_bar_2, ax_bar_2 = plt.subplots()

# Create upper frame for charts
upper_charts_frame = tk.Frame(root)
upper_charts_frame.pack(side="top", fill="both", expand=True)

# Create lower frame for charts
lower_charts_frame = tk.Frame(root)
lower_charts_frame.pack(side="bottom", fill="both", expand=True)

canvas_bar_1 = FigureCanvasTkAgg(fig_bar_1, master=upper_charts_frame)
canvas_bar_1.get_tk_widget().pack(side="left", fill="both", expand=True)

canvas_line_1 = FigureCanvasTkAgg(fig_line_1, master=upper_charts_frame)
canvas_line_1.get_tk_widget().pack(side="right", fill="both", expand=True)

canvas_bar_2 = FigureCanvasTkAgg(fig_bar_2, master=lower_charts_frame)
canvas_bar_2.get_tk_widget().pack(side="left", fill="both", expand=True)

canvas_line_2 = FigureCanvasTkAgg(fig_line_2, master=lower_charts_frame)
canvas_line_2.get_tk_widget().pack(side="right", fill="both", expand=True)

def chart_draw(data, ax_line, ax_bar, canvas_line, canvas_bar):
    if data not in labels:
        print("Unavailable")
        return
    
    # Aggregate data by year and sum numeric columns
    data_filtered_grouped = data_filtered.groupby(data)[numeric_columns].sum().reset_index()
    
    its_keys = list(data_filtered_grouped[data])
    in_numbers = list(data_filtered_grouped.sum(axis=1))

    if data in ["year_start", "year_end", "year_mid"]:
        draw_bar(its_keys, in_numbers, labels[data], ax_bar, canvas_bar)
        draw_line(its_keys, in_numbers, labels[data], ax_line, canvas_line)

    elif data in ["iso_alpha_3_code"]:
        heading_text(labels[data][0])
        draw_bar(its_keys, in_numbers, labels[data], ax_bar, canvas_bar)
        draw_line(its_keys, in_numbers, labels[data], ax_line, canvas_line)

    else:
        print("This category is not available")

# Function to draw bar chart
def draw_bar(xvalues, yvalues, labels, ax, canvas):
    ax.clear()
    ax.bar(xvalues, yvalues)
    ax.set_xlabel(labels[0], fontsize=16)
    ax.set_ylabel(labels[1], fontsize=16)
    ax.tick_params(axis='x', labelrotation=90)  # Rotate x-axis labels
    canvas.draw()

# Function to draw line chart
def draw_line(x, y, labels, ax, canvas):
    ax.clear()
    ax.plot(x, y)
    ax.scatter(x, y)
    ax.set_xlabel(labels[0], fontsize=16)
    ax.set_ylabel(labels[1], fontsize=16)
    canvas.draw()

def heading_text(new_text):
    heading.config(text=new_text)

# Create heading
heading = tk.Label(root, text="Dashboard", font=("monospace", 25))
heading.pack(side="top")

# Call chart_draw with different datasets for each chart
chart_draw(START_YEAR, ax_line_1, ax_bar_1, canvas_line_1, canvas_bar_1)
chart_draw(END_YEAR, ax_line_2, ax_bar_2, canvas_line_2, canvas_bar_2)
chart_draw(MID_YEAR, ax_line_1, ax_bar_1, canvas_line_1, canvas_bar_1)
chart_draw(COUNTRY, ax_line_2, ax_bar_2, canvas_line_2, canvas_bar_2)

root.protocol("WM_DELETE_WINDOW", root.quit)
root.mainloop()