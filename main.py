

import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import random

# Constants for simulation
SOLAR_PANEL_TYPES = ["Monocrystalline", "Polycrystalline", "Thin-film"]
MOUNTING_TYPES = ["Roof-mounted", "Ground-mounted", "Building-integrated"]
ELECTRICAL_CONFIGS = ["Grid-tied", "Off-grid", "Hybrid"]
INCENTIVE_RATE = 0.26  # Example federal tax credit 26%
AVERAGE_LIFESPAN_YEARS = 25

def simulate_ai_rooftop_analysis(image):
    """
    Simulate Vision AI rooftop analysis by "processing" the image
    and returning:
    - solar potential % (0-100)
    - recommended solar panel type
    - mounting recommendation
    - estimated installation cost ($)
    - expected annual energy production (kWh)
    - confidence score (0-1)
    """
    # Use image properties to somewhat vary results (fake)
    width, height = image.size
    base_potential = min(100, (width * height) / 10000)  # rough guess

    solar_potential = round(random.uniform(0.5, 1.0) * base_potential, 1)
    panel_type = random.choice(SOLAR_PANEL_TYPES)
    mounting = random.choice(MOUNTING_TYPES)
    electrical = random.choice(ELECTRICAL_CONFIGS)
    installation_cost = int(random.uniform(15000, 30000) * (solar_potential / 100))
    annual_production = int(random.uniform(4000, 7000) * (solar_potential / 100))
    confidence = round(random.uniform(0.7, 0.95), 2)

    return {
        "solar_potential_percent": solar_potential,
        "recommended_panel_type": panel_type,
        "mounting_recommendation": mounting,
        "electrical_config": electrical,
        "estimated_installation_cost": installation_cost,
        "expected_annual_energy_kwh": annual_production,
        "confidence_score": confidence
    }

def calculate_roi(installation_cost, annual_production_kwh, local_energy_cost_per_kwh=0.13, incentives_rate=INCENTIVE_RATE):
    """
    Calculate estimated ROI based on installation cost,
    annual energy production, local energy cost ($/kWh),
    and incentives (percent tax credit).
    Returns payback period in years and estimated savings.
    """
    effective_cost = installation_cost * (1 - incentives_rate)
    annual_savings = annual_production_kwh * local_energy_cost_per_kwh
    if annual_savings == 0:
        payback_years = float('inf')
    else:
        payback_years = round(effective_cost / annual_savings, 1)
    lifetime_savings = annual_savings * AVERAGE_LIFESPAN_YEARS - effective_cost

    return {
        "effective_cost_after_incentives": effective_cost,
        "annual_savings": annual_savings,
        "payback_period_years": payback_years,
        "lifetime_net_savings": lifetime_savings
    }

def display_results(analysis_result, roi_result):
    """Display the analysis and ROI results prettily in Streamlit"""
    st.subheader("Solar Potential Assessment")
    st.markdown(f"**Solar Potential:** {analysis_result['solar_potential_percent']}%")
    st.markdown(f"**Recommended Solar Panel Type:** {analysis_result['recommended_panel_type']}")
    st.markdown(f"**Mounting Type Recommendation:** {analysis_result['mounting_recommendation']}")
    st.markdown(f"**Electrical Configuration:** {analysis_result['electrical_config']}")
    st.markdown(f"**Estimated Installation Cost:** ${analysis_result['estimated_installation_cost']:,}")
    st.markdown(f"**Expected Annual Energy Production:** {analysis_result['expected_annual_energy_kwh']:,} kWh")
    st.markdown(f"**AI Confidence Score:** {analysis_result['confidence_score'] * 100:.1f}%")

    st.subheader("ROI Estimate")
    st.markdown(f"**Effective Cost After Incentives:** ${roi_result['effective_cost_after_incentives']:,}")
    st.markdown(f"**Estimated Annual Savings:** ${roi_result['annual_savings']:.2f}")
    if roi_result['payback_period_years'] == float('inf'):
        st.markdown("**Payback Period:** Not available (annual savings = $0)")
    else:
        st.markdown(f"**Payback Period:** {roi_result['payback_period_years']} years")
    if roi_result['lifetime_net_savings'] > 0:
        st.markdown(f"**Estimated Lifetime Net Savings:** ${roi_result['lifetime_net_savings']:.2f}")
    else:
        st.markdown(f"**Estimated Lifetime Net Savings:** Loss of ${abs(roi_result['lifetime_net_savings']):.2f}")

def main():
    st.title("🟡 Solar Industry AI Assistant - Rooftop Solar Analysis")
    st.markdown(
        """
        Upload a satellite rooftop image or input an image URL to analyze the solar installation potential.
        Receive personalized recommendations and ROI estimates based on your rooftop.
        """
    )

    # Sidebar help
    st.sidebar.header("About")
    st.sidebar.info("""
        This tool simulates AI-powered rooftop analysis using satellite imagery.
        It provides solar potential assessments, installation recommendations, and ROI estimates.
        Developed as a demonstration project.
    """)

    # Input Image: file upload or URL input
    upload_option = st.radio("Select Image Input Method:", ("Upload Image", "Image URL"))

    image = None
    if upload_option == "Upload Image":
        uploaded_file = st.file_uploader("Upload a satellite rooftop image (jpg, png):", type=['jpg', 'jpeg', 'png'])
        if uploaded_file:
            try:
                image = Image.open(uploaded_file).convert('RGB')
                st.image(image, caption="Uploaded Image", use_column_width=True)
            except Exception:
                st.error("Failed to open uploaded image. Please upload a valid image file.")
    else:
        url = st.text_input("Enter Image URL:")
        if url:
            try:
                response = requests.get(url)
                image = Image.open(BytesIO(response.content)).convert('RGB')
                st.image(image, caption="Loaded Image from URL", use_column_width=True)
            except Exception:
                st.error("Failed to load image from URL. Please check the link and try again.")

    if image:
        if st.button("Analyze Rooftop Solar Potential"):
            with st.spinner("Analyzing rooftop..."):
                # Simulate AI rooftop analysis
                analysis_result = simulate_ai_rooftop_analysis(image)

                # Calculate ROI
                roi_result = calculate_roi(
                    installation_cost=analysis_result['estimated_installation_cost'],
                    annual_production_kwh=analysis_result['expected_annual_energy_kwh']
                )

                # Display results
                display_results(analysis_result, roi_result)

    # Future improvements section
    st.markdown("---")
    st.header("Future Improvements Suggestions")
    st.markdown("""
    - Integrate real OpenRouter or Vision AI APIs to perform true rooftop detection.
    - Support batch processing of multiple rooftop images.
    - Incorporate local regulations and incentive programs dynamically by region.
    - Include detailed shading and weather data for more accurate solar potential.
    - Add user authentication for saving reports and history.
    - Enhance UI with interactive rooftop mapping and editable parameters.
    """)

if __name__ == "__main__":
    main()


