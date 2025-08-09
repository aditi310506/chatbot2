def estimate_efficiency(base_eff, temp_c, humidity):
    """
    Simulates plant efficiency based on environmental conditions.
    A simple rule-based model for a hackathon.
    """
    # Simple model: efficiency decreases with higher temperature and humidity
    eff = base_eff - 0.002 * (temp_c - 25) - 0.0005 * (humidity - 50)
    return max(0.2, eff)  # Ensure efficiency doesn't drop below 20%

def compute_gen_adjustment(efficiency, base_gen_capacity_mw=1000):
    """
    Calculates the generation output based on the new efficiency.
    """
    return base_gen_capacity_mw * efficiency

def create_simulation_response(efficiency_change, new_gen_mw):
    """
    Formats the simulation results into a structured JSON response.
    """
    response_data = {
        "type": "simulation",
        "payload": {
            "efficiency_change": f"{efficiency_change:.2f}%",
            "new_generation_mw": f"{new_gen_mw:.2f}",
            "kpis": {
                "fuel_saved": "placeholder",
                "cost_saved": "placeholder",
                "co2_saved": "placeholder"
            },
            "message": f"Based on your inputs, the plant's efficiency has changed, resulting in a new generation output of {new_gen_mw:.2f} MW."
        }
    }
    return response_data