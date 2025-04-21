import streamlit as st

def show_home_page():
    # Add custom CSS for the home page
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
        
        /* Global Styles */
        * {
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
        
        /* Streamlit Components - Use Default Font */
        .stApp h1, 
        .stApp h2, 
        .stApp h3, 
        .stApp h4, 
        .stApp h5, 
        .stApp h6,
        .stApp p,
        .stApp div,
        .stApp span,
        .stApp button,
        .stApp input,
        .stApp select,
        .stApp textarea,
        .stApp label,
        .stApp .stButton > button,
        .stApp .stSelectbox > div > div,
        .stApp .stTabs [data-baseweb="tab"],
        .stApp .stFileUploader > div,
        .stApp .sidebar .sidebar-content {
            font-family: inherit !important;
        }
        
        /* Hero Section */
        .hero-section {
            text-align: center;
            padding: 4rem 2rem;
            background: linear-gradient(135deg, #f8f9fa 0%, #e3f2fd 100%);
            border-radius: 16px;
            margin: 1rem 0 3rem 0;
            animation: fadeIn 0.8s ease-out;
        }
        
        .hero-title {
            font-size: 3.5rem;
            font-weight: 700;
            background: linear-gradient(120deg, #1a237e 0%, #2196F3 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1.5rem;
            letter-spacing: -0.02em;
        }
        
        .hero-subtitle {
            font-size: 1.25rem;
            color: #424242;
            margin-bottom: 2rem;
            line-height: 1.6;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }
        
        /* Features Section */
        .features-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 2rem;
            margin: 3rem 0;
            animation: slideUp 0.8s ease-out;
        }
        
        .feature-card {
            background: white;
            padding: 2rem;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.05);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border: 1px solid rgba(0,0,0,0.05);
        }
        
        .feature-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 12px 30px rgba(0,0,0,0.1);
            border-color: #2196F3;
        }
        
        .feature-icon {
            font-size: 2.5rem;
            margin-bottom: 1.5rem;
           
            display: inline-block;
        }
        
        .feature-title {
            font-size: 1.25rem;
            font-weight: 600;
            color: #424242;;
            margin-bottom: 1rem;
            letter-spacing: -0.01em;
        }
        
        .feature-description {
            color: #424242;
            font-size: 1rem;
            line-height: 1.6;
        }
        
        /* Target Audience Section */
        .section-title {
            font-size: 2rem;
            font-weight: 700;
            color: #424242;
            margin: 4rem 0 2rem 0;
            text-align: center;
            letter-spacing: -0.02em;
        }
        
        .audience-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1.5rem;
            margin: 2rem 0;
            animation: slideUp 1s ease-out;
        }
        
        .audience-card {
            background: white;
            padding: 2rem 1.5rem;
            border-radius: 16px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.05);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border: 1px solid rgba(0,0,0,0.05);
        }
        
        .audience-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 30px rgba(0,0,0,0.1);
            border-color: #2196F3;
        }
        
        .audience-icon {
            font-size: 2.5rem;
            margin-bottom: 1rem;
            display: inline-block;
            animation: bounce 2s infinite;
        }
        
        .audience-title {
            font-weight: 600;
            color: #424242;;
            font-size: 1.1rem;
            letter-spacing: -0.01em;
        }
        
        /* Call to Action Section */
        .cta-section {
            background: linear-gradient(135deg, #1a239e 0%, #2196F3 100%);
            padding: 3rem 2rem;
            border-radius: 16px;
            text-align: center;
            margin: 4rem 0;
            animation: fadeIn 1s ease-out;
        }
        
        .cta-title {
            font-size: 1.7rem;
            font-weight: 700;
            color: white;
            margin-bottom: 1.5rem;
            letter-spacing: -0.02em;
        }
        
        .cta-description {
            color: rgba(255,255,255,0.9);
            margin-bottom: 2rem;
            font-size: 1rem;
            line-height: 1.6;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }

        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes bounce {
            0%, 100% {
                transform: translateY(0);
            }
            50% {
                transform: translateY(-10px);
            }
        }
        </style>
    """, unsafe_allow_html=True)

    # # Hero Section
    # st.markdown("""
    #     <div class="hero-section">
    #         <div class="hero-title">Welcome to AutoEDA</div>
    #         <div class="hero-subtitle">
    #             Transform your data analysis workflow with powerful automated exploratory data analysis. 
    #             Discover insights faster, visualize better, and make data-driven decisions with confidence.
    #         </div>
    #     </div>
    # """, unsafe_allow_html=True)

    # Features Section
    st.markdown("""
        <div class="section-title">Features</div>
        <div class="features-grid">
            <div class="feature-card">
                <div class="feature-icon">🔍</div>
                <div class="feature-title">Smart Exploration</div>
                <div class="feature-description">
                    Intelligent analysis tools that automatically identify patterns, correlations, and insights in your data.
                </div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📊</div>
                <div class="feature-title">Dynamic Visualization</div>
                <div class="feature-description">
                    Create stunning, interactive charts and graphs that bring your data stories to life.
                </div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">⚡</div>
                <div class="feature-title">Automated Preprocessing</div>
                <div class="feature-description">
                    Clean, transform, and prepare your data with intelligent automation tools.
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Target Audience Section
    st.markdown("""
        <div class="section-title">Who can use this tool ?</div>
        <div class="audience-grid">
            <div class="audience-card">
                <div class="audience-icon">📊</div>
                <div class="audience-title">Data Analysts</div>
            </div>
            <div class="audience-card">
                <div class="audience-icon">🔬</div>
                <div class="audience-title">Data Scientists</div>
            </div>
            <div class="audience-card">
                <div class="audience-icon">💼</div>
                <div class="audience-title">Business Analysts</div>
            </div>
            <div class="audience-card">
                <div class="audience-icon">🎓</div>
                <div class="audience-title">Researchers</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Call to Action Section
    st.markdown("""
        <div class="cta-section">
            <div class="cta-title">Start Exploring Your Data</div>
            <div class="cta-description">
                Upload your dataset or try our example dataset to experience the power of automated analysis. 
                Let AutoEDA handle the complexity while you focus on discovering meaningful insights.
            </div>
        </div>
    """, unsafe_allow_html=True)

def custom_css():
    # Define custom CSS styles
    custom_css = """
    <style>
    body {
        background-color: #f5f5f5;
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
    }

    .container {
        max-width: 800px;
        margin: 0 auto;
        text-align: center;
        padding: 40px;
    }

    .header {
        font-size: 48px;
        font-weight: bold;
        color: #333;
        margin-bottom: 16px;
    }

    .tagline {
        font-size: 24px;
        color: #666;
        margin-bottom: 32px;
    }

    .features {
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
        margin-bottom: 40px;
    }

    .feature {
        flex: 1;
        text-align: center;
        padding: 20px;
        background-color: #ff;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin: 8px;
        transition: transform 0.3s ease-in-out;
    }

    .feature:hover {
        transform: scale(1.05);
    }

    .feature-icon {
        font-size: 36px;
        
    }

    .feature-title {
        font-size: 18px;
        font-weight: bold;
        margin-top: 16px;
    }

    .action-button {
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
        font-weight: bold;
        padding: 16px 32px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        transition: background-color 0.3s;
    }

    .action-button:hover {
        background-color: #45a049;
    }

    </style>
    """

    return custom_css