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
    END_YEAR: ["Year Ended", "Number of cases"],
    MID_YEAR: ["Year in the Middle", "Number of cases"],
    COUNTRY: ["Countries", "Number of cases"],
    PM_PRECRISIS: ["PM Before Crisis", "PM Results"],
    MMR_PRECRISIS: ["MMR Before Crisis", "MMR Results"],
    OBS_MATDEATHS: ["Maternal Death", "Number of Cases"],
    FINAL_ENV: ["ENV Final", "Final ENV Results"],
    FINAL_PM: ["PM Final", "Final PM Results"],
    FINAL_MMR: ["MMR Final", "Final MMR Results"],
    TOTAL_ENV: ["Total ENV", "ENV Results"],
    LIVE_BIRTHS: ["Live Births", "Number of Births"]
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

fig_pie, ax_pie = plt.subplots()

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

canvas_pie = FigureCanvasTkAgg(fig_pie, master=lower_charts_frame)
canvas_pie.get_tk_widget().pack(side="right", fill="both", expand=True)

def chart_draw(data, ax_line, ax_bar, canvas_line, canvas_bar):
    if data not in labels:
        print("Unavailable")
        return
    
    # Aggregate data by the specified column and sum numeric columns
    data_filtered_grouped = data_filtered.groupby(data)[numeric_columns].sum().reset_index()
    
    its_keys = list(data_filtered_grouped[data])
    in_numbers = data_filtered_grouped[numeric_columns].sum(axis=1)

    if data in ["year_start", "year_end"]:
        draw_bar(its_keys, in_numbers, labels[data], ax_bar, canvas_bar)
        draw_line(its_keys, in_numbers, labels[data], ax_line, canvas_line)
    elif data in ["iso_alpha_3_code"]:
        draw_bar(its_keys, in_numbers, labels[data], ax_bar, canvas_bar)
        ax_bar.tick_params(axis='x', labelrotation=90)  # Rotate x-axis labels
    elif data == "year_mid":
        draw_pie(in_numbers, its_keys)

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
    ax.tick_params(axis='x', labelrotation=90)  # Rotate x-axis labels
    canvas.draw()

# Function to draw pie chart
def draw_pie(values, legend):
    ax_pie.clear()
    ax_pie.pie(values, labels=None, autopct=None)
    ax_pie.legend(legend, loc=(-0.2, -0.2))
    canvas_pie.draw()

# Call chart_draw with different datasets for each chart
chart_draw(START_YEAR, ax_line_1, ax_bar_1, canvas_line_1, canvas_bar_1)
chart_draw(END_YEAR, ax_line_2, ax_bar_2, canvas_line_2, canvas_bar_2)
chart_draw(MID_YEAR, ax_pie, ax_pie, canvas_pie, canvas_pie)  # Pie chart only needs one axis
chart_draw(COUNTRY, ax_line_1, ax_bar_1, canvas_line_1, canvas_bar_1)

root.protocol("WM_DELETE_WINDOW", root.quit)
root.mainloop()
