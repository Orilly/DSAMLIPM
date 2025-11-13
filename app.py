from shiny import App, render, ui
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("attendance_anonymised-1.csv")

df.rename(columns = {
    "Unit Instance Code": "Module Code",
    "Calocc Code": "Year",
    "Long Description": "Module Name",
    "Register Event ID": "Event ID",
    "Register Event Slot ID": "Event Slot ID",
    "Planned Start Date": "Date",
    "is Positive": "Has Attended",
    "Postive Marks": "Attended",
    "Negative Marks": "NotAttended",
    "Usage Code": "Attendance Code"
}, inplace = True)

df["Date"] = pd.to_datetime(df["Date"])

module = df[df["Module Name"] == "Italian"] # I picked Italian just for you Nicollò
attendance_over_time = module.groupby("Date")["Attended"].mean().reset_index()
attendance_over_time.sort_values("Date", inplace = True)

# Establishes the UI as solely being the graph
ui = ui.page_fluid(ui.output_plot("attendance_plot"))

def server(input, output, session):
    @output
    @render.plot
    def attendance_plot():
        plt.figure(figsize = (10, 5))
        plt.plot(attendance_over_time["Date"], attendance_over_time["Attended"])
        plt.title("Italian Attendance Rate Over Time")
        plt.xlabel("Date")
        plt.ylabel("Attendance Rate")
        plt.grid(True)
        return plt.gcf()
    
app = App(ui, server)