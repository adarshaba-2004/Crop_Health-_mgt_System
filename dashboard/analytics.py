import matplotlib.pyplot as plt

def show_chart():
    labels = ["Healthy", "Mildew", "Rust", "Blight"]
    values = [12, 5, 3, 2]

    fig, ax = plt.subplots()
    ax.bar(labels, values)
    ax.set_title("Crop Disease Analytics")

    return fig