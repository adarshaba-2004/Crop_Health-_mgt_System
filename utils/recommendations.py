def get_solution(disease):
    data = {
        "Healthy": "No action needed 🌱",
        "Powdery Mildew": "Use sulfur fungicide",
        "Leaf Rust": "Apply fungicide",
        "Bacterial Blight": "Use resistant seeds"
    }
    return data.get(disease, "No solution available")