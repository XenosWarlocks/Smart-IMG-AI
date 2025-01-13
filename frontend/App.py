# frontend/app.py
import streamlit as st
import requests
import json
from PIL import Image
import io

# API endpoint
API_BASE_URL = "http://localhost:8000"

def get_api_usage():
    """Fetch current API usage statistics"""
    response = requests.get(f"{API_BASE_URL}/api/usage")
    return response.json()

def update_usage_display():
    """Display API usage metrics"""
    usage_stats = get_api_usage()
    
    st.markdown("""
        <style>
        .metric-container {
            background-color: #f0f2f6;
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
        }
        .metric-title {
            font-weight: bold;
            margin-bottom: 5px;
        }
        .progress-bar-container {
            width: 100%;
            background-color: #ddd;
            border-radius: 5px;
            margin: 5px 0;
        }
        .progress-bar {
            height: 20px;
            border-radius: 5px;
            text-align: center;
            line-height: 20px;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    for i, (key, stats) in enumerate(usage_stats.items(), 1):
        col = col1 if i == 1 else col2
        with col:
            requests = stats['requests']
            tokens = stats['tokens']
            progress = (requests / 60) * 100
            
            st.markdown(f"""
                <div class="metric-container">
                    <div class="metric-title">API Key {i}</div>
                    <div>Requests (last minute): {requests}/60</div>
                    <div class="progress-bar-container">
                        <div class="progress-bar" style="width: {min(progress, 100)}%; 
                             background-color: {'#ff4b4b' if progress >= 100 else '#00cc00'}">
                            {min(round(progress), 100)}%
                        </div>
                    </div>
                    <div>Total Tokens Used: {tokens:,}</div>
                    <div>Status: {'Rate Limited' if progress >= 100 else 'Active'}</div>
                </div>
            """, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="Advanced Image Captioning System",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("🖼️ Advanced Image Captioning System")

    # API Configuration
    with st.expander("🔑 API Configuration", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            gemini_key1 = st.text_input("Enter first Gemini API key", type="password")
        with col2:
            gemini_key2 = st.text_input("Enter second Gemini API key", type="password")

    if not (gemini_key1 and gemini_key2):
        st.warning("⚠️ Please enter both Gemini API keys to proceed.")
        return

    # Display API usage metrics
    update_usage_display()

    # Image input section
    st.markdown("### 📤 Upload Image")
    input_method = st.radio(
        "Choose input method:",
        ["File Upload", "URL"],
        horizontal=True
    )

    if input_method == "File Upload":
        image_file = st.file_uploader(
            "Drop your image here",
            type=['png', 'jpg', 'jpeg']
        )
        if image_file:
            try:
                # Display image
                image = Image.open(image_file)
                st.image(image, caption="Input Image", use_container_width=True)

                if st.button("🔍 Analyze Image"):
                    files = {
                        'file': ('image.jpg', image_file, 'image/jpeg'),
                    }
                    params = {
                        'api_key1': gemini_key1,
                        'api_key2': gemini_key2
                    }
                    
                    with st.spinner("🔄 Analyzing image..."):
                        response = requests.post(
                            f"{API_BASE_URL}/api/analyze-image-upload",
                            files=files,
                            params=params
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            components = data['components']
                            
                            # Update usage display
                            update_usage_display()
                            
                            # Display results
                            display_results(components)
                        else:
                            st.error(f"Error: {response.text}")

            except Exception as e:
                st.error(f"Error: {str(e)}")

    else:
        image_url = st.text_input("🔗 Enter image URL:")
        if image_url:
            try:
                # Display image
                st.image(image_url, caption="Input Image", use_container_width=True)

                if st.button("🔍 Analyze Image"):
                    payload = {
                        "url": image_url,
                        "key1": gemini_key1,
                        "key2": gemini_key2
                    }
                    
                    with st.spinner("🔄 Analyzing image..."):
                        response = requests.post(
                            f"{API_BASE_URL}/api/analyze-image-url",
                            json=payload
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            components = data['components']
                            
                            # Update usage display
                            update_usage_display()
                            
                            # Display results
                            display_results(components)
                        else:
                            st.error(f"Error: {response.text}")

            except Exception as e:
                st.error(f"Error: {str(e)}")

def display_results(components):
    """Display analysis results in tabs"""
    tab1, tab2 = st.tabs(["📋 Detailed Analysis", "📝 Summary"])
    
    with tab1:
        st.subheader("📝 Basic Description")
        st.write(components['base_description'])
        
        st.subheader("🔍 Detailed Analysis")
        st.write(components['detailed_analysis'])
    
    with tab2:
        st.subheader("📊 Final Summary")
        st.write(components['final_summary'])
    
    # Export option
    st.download_button(
        "📥 Export Analysis",
        '\n\n'.join([f"{k.upper()}:\n{v}" for k, v in components.items()]),
        file_name="image_analysis.txt",
        mime="text/plain"
    )

if __name__ == "__main__":
    main()

# streamlit run frontend/App.py
