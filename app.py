import os
import sys

# Add root directory to python path for direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import streamlit as st
import asyncio
import pandas as pd
import altair as alt
import json

from graph.workflow import run_travel_plan

# Page Config
st.set_page_config(
    page_title="CeylonTrip AI — Sri Lanka Travel Operations",
    page_icon="🇱🇰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern light theme with white and green palette (Inlined Streamlit Theme)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    /* Streamlit Base Light Theme & Color System Variables */
    :root {
        --primary-color: #059669 !important;
        --background-color: #ffffff !important;
        --secondary-background-color: #f0fdf4 !important;
        --text-color: #0f172a !important;
        --font: 'Outfit', sans-serif !important;
    }

    html, body, .stApp {
        font-family: 'Outfit', sans-serif !important;
        color: #0f172a !important;
        color-scheme: light !important;
    }

    /* Preserve Material Icons font family for Streamlit icons & sidebar collapse toggle */
    [data-testid="stIconMaterial"],
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarCollapseButton"] *,
    [data-testid="stSidebarHeader"] *,
    button[data-testid="stSidebarCollapseButton"] span,
    button[data-testid="stSidebarCollapseButton"] i,
    span[data-testid="stHeaderNav"] *,
    .stIconMaterial,
    [class*="Material"] {
        font-family: "Material Symbols Rounded", "Material Symbols Outlined", "Material Icons" !important;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #f0fdf4 50%, #ecfdf5 100%) !important;
        background-color: #ffffff !important;
        color: #0f172a !important;
    }

    /* Top Navigation Header & Toolbar */
    header[data-testid="stHeader"],
    [data-testid="stHeader"],
    .stAppHeader,
    div[data-testid="stHeaderNav"] {
        background-color: transparent !important;
        background: transparent !important;
    }

    /* Hide default red decoration bar at top */
    div[data-testid="stDecoration"],
    [data-testid="stDecoration"] {
        display: none !important;
        background: none !important;
    }
    
    /* Header icons & toolbar buttons */
    header button,
    [data-testid="stHeader"] button,
    [data-testid="stToolbar"] button {
        color: #0f172a !important;
    }
    
    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        color: #065f46 !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0 !important;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #065f46 !important;
    }

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span {
        color: #0f172a !important;
    }

    /* Hero Banner Container */
    .hero-container {
        padding: 2.2rem;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(12px);
        border: 1px solid #dcfce7;
        border-radius: 18px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(5, 150, 105, 0.07);
    }
    
    .hero-title {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(90deg, #065f46 0%, #059669 50%, #10b981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    
    .hero-subtitle {
        font-size: 1.15rem;
        color: #475569;
        margin-bottom: 0.5rem;
        font-weight: 400;
    }
    
    .glass-card {
        background: #ffffff;
        border-radius: 14px;
        padding: 1.4rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
        margin-bottom: 1rem;
    }
    
    /* Status Badges */
    .status-badge-online {
        background: #dcfce7;
        color: #065f46;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        border: 1px solid #a7f3d0;
    }
    
    .status-badge-estimated {
        background: #fef3c7;
        color: #92400e;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        border: 1px solid #fde68a;
    }

    .status-badge-unavailable {
        background: #fee2e2;
        color: #991b1b;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        border: 1px solid #fca5a5;
    }

    /* Metric Cards */
    div[data-testid="stMetric"] {
        background-color: #ffffff !important;
        border: 1.5px solid #dcfce7 !important;
        border-radius: 14px !important;
        padding: 0.75rem 0.8rem !important;
        box-shadow: 0 4px 15px rgba(5, 150, 105, 0.05) !important;
        min-width: 0 !important;
    }

    div[data-testid="stMetricLabel"] label,
    div[data-testid="stMetricLabel"] p {
        color: #065f46 !important;
        font-weight: 600 !important;
        font-size: 0.825rem !important;
    }

    div[data-testid="stMetricValue"],
    div[data-testid="stMetricValue"] > div,
    div[data-testid="stMetricValue"] * {
        color: #065f46 !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        line-height: 1.3 !important;
    }

    div[data-testid="stMetricDelta"],
    div[data-testid="stMetricDelta"] * {
        font-size: 0.75rem !important;
    }
    
    /* OVERRIDE ALL BUTTONS TO EMERALD GREEN */
    button[kind="primary"],
    button[kind="secondary"],
    button[data-testid="stBaseButton-primary"],
    button[data-testid="stBaseButton-secondary"],
    .stButton > button,
    .stButton > button[kind="primary"],
    div[data-testid="stFormSubmitButton"] > button,
    div[data-baseweb="button"] {
        background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
        background-color: #059669 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 12px rgba(5, 150, 105, 0.25) !important;
        transition: all 0.2s ease-in-out !important;
    }
    
    button[kind="primary"]:hover,
    button[kind="secondary"]:hover,
    button[data-testid="stBaseButton-primary"]:hover,
    button[data-testid="stBaseButton-secondary"]:hover,
    .stButton > button:hover,
    .stButton > button[kind="primary"]:hover,
    div[data-testid="stFormSubmitButton"] > button:hover,
    div[data-baseweb="button"]:hover {
        background: linear-gradient(135deg, #047857 0%, #065f46 100%) !important;
        background-color: #047857 !important;
        color: #ffffff !important;
        box-shadow: 0 6px 18px rgba(5, 150, 105, 0.35) !important;
        transform: translateY(-1px);
    }

    button[kind="primary"]:focus,
    button[data-testid="stBaseButton-primary"]:focus,
    .stButton > button:focus {
        box-shadow: 0 0 0 3px rgba(5, 150, 105, 0.4) !important;
        color: #ffffff !important;
    }

    button[kind="primary"] p,
    button[data-testid="stBaseButton-primary"] p,
    .stButton > button p {
        color: #ffffff !important;
    }
    
    /* Stepper (+/-) buttons in st.number_input (Duration, Travelers, Total Budget) */
    /* Stepper (+/-) buttons in st.number_input (Duration, Travelers, Total Budget) */
    .stNumberInput button,
    div[data-testid="stNumberInput"] button,
    [data-testid="stNumberInput"] button,
    button[data-testid="stNumberInputStepDownButton"],
    button[data-testid="stNumberInputStepUpButton"] {
        background: #ffffff !important;
        background-color: #ffffff !important;
        border: none !important;
        border-left: 1.5px solid #d1fae5 !important;
        color: #059669 !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        height: 100% !important;
        min-height: 38px !important;
        padding: 0 10px !important;
        transition: all 0.2s ease-in-out !important;
    }
    
    .stNumberInput button:hover,
    div[data-testid="stNumberInput"] button:hover,
    [data-testid="stNumberInput"] button:hover,
    button[data-testid="stNumberInputStepDownButton"]:hover,
    button[data-testid="stNumberInputStepUpButton"]:hover {
        background: #f0fdf4 !important;
        background-color: #f0fdf4 !important;
        color: #047857 !important;
        border-left-color: #10b981 !important;
    }

    .stNumberInput button:focus,
    div[data-testid="stNumberInput"] button:focus,
    [data-testid="stNumberInput"] button:focus {
        outline: none !important;
        box-shadow: none !important;
    }
    
    /* Outer st.number_input container - keep block layout so heading sits cleanly on top */
    div[data-testid="stNumberInput"],
    .stNumberInput {
        border: none !important;
        background: transparent !important;
        box-shadow: none !important;
        display: block !important;
    }

    /* Enclose st.number_input input container (below label) in a single unified box matching st.selectbox */
    div[data-testid="stNumberInput"] > div[data-baseweb="input"],
    div[data-testid="stNumberInput"] > div[data-baseweb="base-input"],
    div[data-testid="stNumberInput"] > div:not([data-testid="stWidgetLabel"]),
    div[data-testid="stNumberInputContainer"] {
        border: 1.5px solid #10b981 !important;
        border-radius: 12px !important;
        background-color: #ffffff !important;
        background: #ffffff !important;
        box-shadow: 0 2px 8px rgba(5, 150, 105, 0.05) !important;
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        overflow: hidden !important;
        transition: all 0.2s ease-in-out !important;
        min-height: 42px !important;
    }

    /* Target all inner wrapper elements and input inside stNumberInput to be solid white background */
    div[data-testid="stNumberInput"] div,
    div[data-testid="stNumberInput"] input,
    div[data-testid="stNumberInputContainer"] div,
    div[data-testid="stNumberInputContainer"] input,
    div[data-baseweb="input"] div,
    div[data-baseweb="base-input"] div {
        background-color: #ffffff !important;
        background: #ffffff !important;
        color: #0f172a !important;
        border: none !important;
    }

    div[data-testid="stNumberInput"] > div:not([data-testid="stWidgetLabel"]):hover,
    div[data-testid="stNumberInputContainer"]:hover {
        border-color: #059669 !important;
        box-shadow: 0 4px 12px rgba(5, 150, 105, 0.12) !important;
    }

    div[data-testid="stNumberInput"] > div:not([data-testid="stWidgetLabel"]):focus-within,
    div[data-testid="stNumberInputContainer"]:focus-within {
        border: 2px solid #059669 !important;
        box-shadow: 0 0 0 4px rgba(5, 150, 105, 0.18) !important;
    }

    /* Strip internal sub-borders inside number input box */
    div[data-testid="stNumberInput"] div[data-testid="stNumberInputStepControls"],
    .stNumberInputStepControls,
    [data-testid="stNumberInputStepControls"] {
        border: none !important;
        background: #ffffff !important;
        box-shadow: none !important;
    }

    /* Form Inputs, Text Areas, Selectboxes, Multiselects & Chat Input - Common Unified Style */
    .stTextInput > div > div,
    .stTextArea > div > div,
    .stSelectbox > div > div,
    .stMultiSelect > div > div,
    [data-testid="stSelectbox"] div[data-baseweb="select"] > div,
    [data-testid="stMultiSelect"] div[data-baseweb="select"] > div,
    .stDateInput > div > div,
    .stTimeInput > div > div,
    .stTextInput div[data-baseweb="input"],
    div[data-baseweb="textarea"],
    div[data-testid="stChatInput"] {
        border: 1.5px solid #10b981 !important;
        border-radius: 12px !important;
        background-color: #ffffff !important;
        background: #ffffff !important;
        box-shadow: 0 2px 8px rgba(5, 150, 105, 0.05) !important;
        transition: all 0.2s ease-in-out !important;
    }

    /* Prevent default nested/outer borders in BaseWeb select components */
    [data-testid="stSelectbox"] div[data-baseweb="select"],
    [data-testid="stMultiSelect"] div[data-baseweb="select"],
    div[data-baseweb="select"] {
        border: none !important;
        background: transparent !important;
        box-shadow: none !important;
    }

    /* Common Hover State for all input containers */
    .stTextInput > div > div:hover,
    .stTextArea > div > div:hover,
    .stNumberInput > div:hover,
    [data-testid="stNumberInput"] > div:hover,
    .stSelectbox > div > div:hover,
    .stMultiSelect > div > div:hover,
    [data-testid="stSelectbox"] div[data-baseweb="select"] > div:hover,
    [data-testid="stMultiSelect"] div[data-baseweb="select"] > div:hover,
    .stDateInput > div > div:hover,
    .stTimeInput > div > div:hover,
    div[data-baseweb="input"]:hover,
    div[data-baseweb="base-input"]:hover,
    div[data-baseweb="textarea"]:hover,
    div[data-testid="stChatInput"]:hover {
        border-color: #059669 !important;
        box-shadow: 0 4px 12px rgba(5, 150, 105, 0.12) !important;
    }

    /* Common Focus State for all input fields */
    .stTextInput > div > div:focus-within,
    .stTextArea > div > div:focus-within,
    .stNumberInput > div:focus-within,
    [data-testid="stNumberInput"] > div:focus-within,
    .stSelectbox > div > div:focus-within,
    .stMultiSelect > div > div:focus-within,
    [data-testid="stSelectbox"] div[data-baseweb="select"] > div:focus-within,
    [data-testid="stMultiSelect"] div[data-baseweb="select"] > div:focus-within,
    .stDateInput > div > div:focus-within,
    .stTimeInput > div > div:focus-within,
    div[data-baseweb="input"]:focus-within,
    div[data-baseweb="base-input"]:focus-within,
    div[data-baseweb="textarea"]:focus-within,
    div[data-testid="stChatInput"]:focus-within {
        border: 2px solid #059669 !important;
        box-shadow: 0 0 0 4px rgba(5, 150, 105, 0.18) !important;
        outline: none !important;
    }

    /* Common Input Text & Textarea Typography */
    input, 
    textarea,
    div[data-baseweb="input"] input,
    div[data-baseweb="textarea"] textarea,
    div[data-baseweb="select"] input,
    div[data-baseweb="base-input"] input,
    div[data-baseweb="base-input"] textarea {
        color: #0f172a !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        background-color: transparent !important;
        background: transparent !important;
        line-height: 1.5 !important;
    }

    /* Specific Text Area formatting */
    textarea,
    div[data-baseweb="textarea"] textarea,
    [data-testid="stTextArea"] textarea {
        padding: 10px 14px !important;
        min-height: 90px !important;
        resize: vertical !important;
        border-radius: 12px !important;
    }

    /* Common Placeholder styling */
    input::placeholder,
    textarea::placeholder,
    div[data-baseweb="select"] div[aria-hidden="true"] {
        color: #94a3b8 !important;
        opacity: 1 !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 400 !important;
    }

    /* Common Input Labels */
    .stTextInput label, 
    .stTextArea label,
    .stNumberInput label, 
    .stSelectbox label, 
    .stMultiSelect label, 
    .stDateInput label,
    .stTimeInput label,
    [data-testid="stWidgetLabel"], 
    [data-testid="stWidgetLabel"] p, 
    [data-testid="stWidgetLabel"] span {
        color: #065f46 !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        letter-spacing: 0.01em !important;
        background: transparent !important;
        background-color: transparent !important;
        margin-bottom: 0.35rem !important;
    }

    /* Multiselect tag badge styling */
    span[data-baseweb="tag"],
    div[data-baseweb="tag"],
    [data-testid="stMultiSelect"] span[data-baseweb="tag"],
    [data-testid="stMultiSelect"] div[data-baseweb="tag"] {
        background-color: #f0fdf4 !important;
        background: #f0fdf4 !important;
        color: #065f46 !important;
        border: 1px solid #a7f3d0 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 2px 8px !important;
        margin: 2px !important;
    }

    /* Text inside multiselect tags */
    span[data-baseweb="tag"] span,
    div[data-baseweb="tag"] span,
    [data-testid="stMultiSelect"] span[data-baseweb="tag"] span {
        color: #065f46 !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 0.88rem !important;
    }

    /* Close 'x' icon on multiselect tags */
    span[data-baseweb="tag"] svg,
    div[data-baseweb="tag"] svg,
    span[data-baseweb="tag"] [data-baseweb="icon"],
    span[data-baseweb="tag"] [role="button"],
    [data-testid="stMultiSelect"] span[data-baseweb="tag"] svg path {
        fill: #065f46 !important;
        color: #065f46 !important;
        stroke: #065f46 !important;
    }

    /* Hover state for multiselect close 'x' icon */
    span[data-baseweb="tag"] span[role="button"]:hover,
    div[data-baseweb="tag"] span[role="button"]:hover {
        background-color: #dcfce7 !important;
        border-radius: 50% !important;
    }

    /* Selectbox & Multiselect specific container alignment */
    [data-testid="stSelectbox"] > div > div,
    [data-testid="stMultiSelect"] > div > div {
        min-height: 42px !important;
        align-items: center !important;
    }

    /* Dropdown popover menu styling for selectbox & multiselect */
    ul[data-baseweb="menu"],
    div[data-baseweb="popover"] ul,
    div[data-baseweb="menu"] {
        background-color: #ffffff !important;
        border: 1px solid #a7f3d0 !important;
        border-radius: 10px !important;
        box-shadow: 0 10px 25px rgba(5, 150, 105, 0.15) !important;
    }

    /* Dropdown items / options */
    li[data-baseweb="option"],
    div[data-baseweb="option"],
    ul[data-baseweb="menu"] li,
    div[role="option"] {
        color: #0f172a !important;
        background-color: #ffffff !important;
        font-family: 'Outfit', sans-serif !important;
    }

    /* Selected / Focused dropdown options */
    li[data-baseweb="option"][aria-selected="true"],
    div[data-baseweb="option"][aria-selected="true"],
    ul[data-baseweb="menu"] li[aria-selected="true"],
    li[data-baseweb="option"]:hover,
    div[data-baseweb="option"]:hover,
    ul[data-baseweb="menu"] li:hover,
    div[role="option"]:hover {
        background-color: #f0fdf4 !important;
        color: #065f46 !important;
        font-weight: 600 !important;
    }

    /* Checkmark / icons inside select options & dropdown arrows */
    ul[data-baseweb="menu"] svg,
    li[data-baseweb="option"] svg,
    div[role="option"] svg,
    div[data-baseweb="select"] svg,
    [data-testid="stSelectbox"] svg,
    [data-testid="stMultiSelect"] svg,
    .stMultiSelect svg,
    .stSelectbox svg {
        fill: #059669 !important;
        color: #059669 !important;
    }

    /* Radio buttons, Checkboxes & Sliders */
    div[data-baseweb="radio"] input:checked + div,
    input[type="radio"]:checked {
        background-color: #059669 !important;
        border-color: #059669 !important;
    }

    .stCheckbox input:checked + div,
    input[type="checkbox"]:checked {
        background-color: #059669 !important;
        border-color: #059669 !important;
    }

    .stSlider [data-baseweb="slider"] div {
        background-color: #059669 !important;
    }

    /* Links & Accents */
    a, a:visited {
        color: #059669 !important;
    }
    
    /* TAB CONTAINER & BUTTONS - LIGHT THEME OVERRIDES */
    div[data-baseweb="tab-list"] {
        background-color: #ffffff !important;
        border-bottom: 2px solid #a7f3d0 !important;
        border-radius: 12px 12px 0 0 !important;
        padding: 4px 8px !important;
        gap: 6px !important;
    }

    button[data-baseweb="tab"] {
        color: #334155 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        background-color: transparent !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        opacity: 1 !important;
    }

    button[data-baseweb="tab"] p,
    button[data-baseweb="tab"] span,
    button[data-baseweb="tab"] div {
        color: #334155 !important;
        opacity: 1 !important;
    }

    button[data-baseweb="tab"]:hover {
        background-color: #f0fdf4 !important;
        color: #065f46 !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #059669 !important;
        background-color: #f0fdf4 !important;
        font-weight: 700 !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] p,
    button[data-baseweb="tab"][aria-selected="true"] span,
    button[data-baseweb="tab"][aria-selected="true"] div {
        color: #059669 !important;
    }

    /* Tab content panel bottom padding */
    div[data-testid="stTabPanel"],
    div[data-baseweb="tab-panel"] {
        padding-bottom: 0.625rem !important;
        margin-bottom: 0.5rem !important;
    }

    /* Expander header styling */
    div[data-testid="stExpander"] {
        border: 1px solid #dcfce7 !important;
        border-radius: 12px !important;
        background-color: #ffffff !important;
        box-shadow: 0 2px 8px rgba(5, 150, 105, 0.03) !important;
    }

    .streamlit-expanderHeader,
    div[data-testid="stExpander"] summary {
        background-color: #f0fdf4 !important;
        border-radius: 10px !important;
        color: #065f46 !important;
        font-weight: 600 !important;
    }

    /* DATAFRAMES & DATA TABLES LIGHT THEME OVERRIDES */
    div[data-testid="stDataFrame"],
    div[data-testid="stTable"],
    div[data-testid="stElementContainer"] [data-testid="stDataFrame"],
    .glideDataEditor {
        background-color: #ffffff !important;
        background: #ffffff !important;
        border: 1.5px solid #dcfce7 !important;
        border-radius: 12px !important;
        color: #0f172a !important;
        --gd-bg-cell: #ffffff !important;
        --gd-bg-cell-medium: #f8fafc !important;
        --gd-bg-header: #f0fdf4 !important;
        --gd-bg-header-has-focus: #dcfce7 !important;
        --gd-text-dark: #0f172a !important;
        --gd-text-medium: #334155 !important;
        --gd-text-light: #64748b !important;
        --gd-accent-color: #059669 !important;
        --gd-accent-light: #dcfce7 !important;
        --gd-border-color: #e2e8f0 !important;
    }

    .glideDataEditor * {
        background-color: #ffffff !important;
        color: #0f172a !important;
    }

    /* Info Callout Box Styling */
    div[data-testid="stAlert"] {
        border-radius: 12px !important;
        border: 1px solid #a7f3d0 !important;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #f8fafc;
    }
    ::-webkit-scrollbar-thumb {
        background: #a7f3d0;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #059669;
    }

    /* Progress Bar & Spinners */
    div[data-testid="stProgressBar"] > div > div {
        background-color: #059669 !important;
    }

    div[data-testid="stSpinner"] > div {
        border-top-color: #059669 !important;
    }

    ::selection {
        background-color: #a7f3d0 !important;
        color: #065f46 !important;
    }
</style>
""", unsafe_allow_html=True)

# App Header
st.markdown("""
<div class="hero-container">
    <div class="hero-title">CeylonTrip AI</div>
    <div class="hero-subtitle">Your AI Travel Operations Agent for Sri Lanka • Online-First Multi-Agent Engine</div>
</div>
""", unsafe_allow_html=True)

# Sidebar Options & Controls
with st.sidebar:
    st.title("CeylonTrip AI")
    
    # Sri Lanka 25 Administrative Districts ONLY
    SRI_LANKA_DISTRICTS = [
        "Ampara", "Anuradhapura", "Badulla", "Batticaloa", "Colombo", 
        "Galle", "Gampaha", "Hambantota", "Jaffna", "Kalutara", 
        "Kandy", "Kegalle", "Kilinochchi", "Kurunegala", "Mannar", 
        "Matale", "Matara", "Monaragala", "Mullaitivu", "Nuwara Eliya", 
        "Polonnaruwa", "Puttalam", "Ratnapura", "Trincomalee", "Vavuniya"
    ]

    origin = st.selectbox("Origin Location (District)", SRI_LANKA_DISTRICTS, index=4)
    
    destinations_input = st.multiselect(
        "Select Sri Lanka Destinations (Districts)",
        SRI_LANKA_DISTRICTS,
        default=["Badulla", "Nuwara Eliya"]
    )
    
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        duration_days = st.number_input("Duration (Days)", min_value=1, max_value=30, value=5)
    with col_d2:
        travelers = st.number_input("Travelers", min_value=1, max_value=20, value=2)
        
    currency = "LKR"
    budget_amt = st.number_input("Total Budget (LKR)", min_value=1000.0, value=150000.0, step=5000.0)
        
    travel_style = st.selectbox("Travel Style", ["Balanced", "Budget", "Luxury"], index=0)
    
    preferences = st.multiselect(
        "Preferences",
        ["Nature", "Adventure", "Beach", "Culture", "Wildlife", "Hiking", "Food", "History", "Photography", "Relaxation"],
        default=["Nature", "Culture", "Hiking"]
    )

# Main Query Area
st.subheader("Where would you like to travel in Sri Lanka?")

dest_str = ", ".join(destinations_input) if destinations_input else "Sri Lanka destinations"
default_query = f"Plan a {int(duration_days)}-day trip from {origin} to {dest_str} for {int(travelers)} people under LKR {budget_amt:,.0f}."

query_preset = st.text_input(
    "Describe your desired trip or ask a travel question:",
    value=default_query
)

def find_weather_for_location(dest_name: str, weather_list: list) -> dict:
    """Robustly matches a destination to weather report using exact, partial, district, or fallback logic."""
    if not weather_list:
        return {}
    if not dest_name:
        return weather_list[0]
        
    d_clean = dest_name.strip().lower()
    
    # 1. Exact match
    for w in weather_list:
        w_dest = w.get("destination", "").strip().lower()
        if w_dest == d_clean:
            return w
            
    # 2. Substring / Partial match
    for w in weather_list:
        w_dest = w.get("destination", "").strip().lower()
        if d_clean in w_dest or w_dest in d_clean:
            return w

    # 3. Known Sri Lanka district & regional city aliases
    DISTRICT_ALIASES = {
        "badulla": ["ella", "haputale", "bandarawela"],
        "ella": ["badulla"],
        "matale": ["sigiriya", "dambulla"],
        "gampaha": ["negombo"],
        "matara": ["mirissa", "weligama"],
        "galle": ["hikkaduwa", "unawatuna", "bentota"],
        "hambantota": ["tangalle", "yala", "udawalawe"],
        "nuwara eliya": ["horton plains", "hakgala", "hatton"],
        "kandy": ["peradeniya", "katugastota"]
    }
    aliases = DISTRICT_ALIASES.get(d_clean, [])
    for alias in aliases:
        for w in weather_list:
            w_dest = w.get("destination", "").strip().lower()
            if alias in w_dest:
                return w
                
    # 4. Fallback to first available weather report
    return weather_list[0]


col_btn, col_help = st.columns([1, 4])
with col_btn:
    generate_clicked = st.button("🚀 Generate Travel Operations Plan", type="primary", width="stretch")

if generate_clicked or "plan_data" in st.session_state:
    
    if generate_clicked:
        form_payload = {
            "origin": origin,
            "destinations": destinations_input,
            "duration_days": int(duration_days),
            "travelers": int(travelers),
            "budget": float(budget_amt),
            "currency": "LKR",
            "travel_style": travel_style,
            "preferences": preferences
        }
        
        with st.spinner("🤖 CeylonTrip AI Multi-Agent Network executing live queries..."):
            try:
                # Run graph workflow asynchronously
                res_state = asyncio.run(run_travel_plan(query_preset, form_payload))
                st.session_state["plan_data"] = res_state
            except Exception as e:
                st.error(f"Error executing agent workflow: {str(e)}")
                st.stop()

    data = st.session_state.get("plan_data", {})
    req_summary = data.get("travel_request", {})

    # Check Sri Lanka location rejection
    if not req_summary.get("is_sri_lanka", True):
        st.warning(req_summary.get("message", "CeylonTrip AI currently supports travel planning exclusively within Sri Lanka."))
        st.stop()

    # Result Navigation Tabs
    tab_overview, tab_itinerary, tab_budget, tab_transport, tab_hotels, tab_activities, tab_weather, tab_emergency = st.tabs([
        "📋 Overview", "📅 Day-by-Day Itinerary", "💰 Budget Engine", "🚗 Transport & Routes", 
        "🏨 Accommodations", "🧗 Activities", "🌤️ Weather Forecast", "🚑 Emergency Info"
    ])

    # 1. OVERVIEW TAB
    with tab_overview:
        st.markdown("## CeylonTrip AI — Travel Summary")
        
        b_data = data.get("budget", {})
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Total Budget", f"LKR {b_data.get('total_budget', 0):,.2f}")
        with c2:
            st.metric("Estimated Total Cost", f"LKR {b_data.get('total_estimated_cost', 0):,.2f}")
        with c3:
            rem = b_data.get("remaining_budget", 0)
            st.metric("Remaining Budget", f"LKR {rem:,.2f}", delta=f"LKR {rem:,.2f}")
        with c4:
            st.metric("Destination Count", len(data.get("destinations", [])))

        # Route Display
        st.markdown("### 🗺️ Planned Travel Route")
        dest_names = [d.get("name") for d in data.get("destinations", []) if d.get("name")]
        if dest_names:
            route_str = f"**{origin}** ➔ " + " ➔ ".join(dest_names) + f" ➔ **{origin}**"
            st.info(route_str)

        # Interactive Map if coordinates exist
        map_points = []
        for dest in data.get("destinations", []):
            coords = dest.get("coordinates")
            if coords and coords.get("latitude") and coords.get("longitude"):
                map_points.append({"lat": coords["latitude"], "lon": coords["longitude"], "name": dest.get("name")})
        
        if map_points:
            df_map = pd.DataFrame(map_points)
            st.map(df_map, zoom=7)

        st.markdown("<div style='padding-bottom: 0.625rem;'></div>", unsafe_allow_html=True)

    # 2. ITINERARY TAB
    with tab_itinerary:
        itin = data.get("itinerary", {})
        st.markdown(f"### 📅 {itin.get('title', 'Day-by-Day Itinerary')}")
        st.write(itin.get("overall_summary", ""))
        
        weather_list = data.get("weather", [])
        
        for day in itin.get("days", []):
            day_num = day.get("day_number", 1)
            dest = day.get("destination", "")
            
            w_info_str = None
            w_report = find_weather_for_location(dest, weather_list)
            if w_report:
                forecast_items = w_report.get("forecast", [])
                idx = min(day_num - 1, len(forecast_items) - 1) if forecast_items else -1
                if idx >= 0:
                    f = forecast_items[idx]
                    t_max = f.get("temperature_max", 27.5)
                    t_min = f.get("temperature_min", 22.0)
                    r_chance = f.get("rain_probability", 20)
                    cond_str = f.get("condition", "Partly cloudy")
                    adv_str = f.get("advisory", "")
                    w_info_str = f"🌤️ **Day {day_num} Weather ({dest}):** {t_max}°C max / {t_min}°C min | 🌧️ Rain: {r_chance}% | {cond_str}"
                    if adv_str:
                        w_info_str += f" — *{adv_str}*"

            with st.expander(f"📌 {day.get('title')} ({dest})", expanded=True):
                if w_info_str:
                    st.info(w_info_str)
                if day.get("travel_segment"):
                    st.caption(f"🚆 **Travel:** {day['travel_segment']}")
                
                m = day.get("morning", {})
                st.markdown(f"**Morning:** {m.get('title')} — *{m.get('description')}*")
                
                a = day.get("afternoon", {})
                st.markdown(f"**Afternoon:** {a.get('title')} — *{a.get('description')}*")
                
                e = day.get("evening", {})
                st.markdown(f"**Evening:** {e.get('title')} — *{e.get('description')}*")

        st.markdown("<div style='padding-bottom: 0.625rem;'></div>", unsafe_allow_html=True)

    # 3. BUDGET TAB
    with tab_budget:
        st.markdown("### 💰 Deterministic Budget Breakdown")
        b_info = data.get("budget", {})
        
        col_b_summary, col_b_chart = st.columns([1, 1])
        with col_b_summary:
            st.write(f"**Budget Currency:** {b_info.get('currency', 'LKR')}")
            st.write(f"**Total Cost:** LKR {b_info.get('total_estimated_cost_lkr', 0):,.2f}")
            
            if b_info.get("is_within_budget"):
                st.success("✅ Your trip cost is strictly within your specified budget!")
            else:
                st.error("⚠️ Estimated costs exceed specified budget!")

        with col_b_chart:
            cats = b_info.get("categories", {})
            if cats:
                df_cat = pd.DataFrame(list(cats.items()), columns=["Category", "Cost (LKR)"])
                chart = (
                    alt.Chart(df_cat)
                    .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, color="#059669")
                    .encode(
                        x=alt.X("Category:N", sort=None, axis=alt.Axis(labelAngle=0, labelColor="#0f172a", titleColor="#065f46", labelFontWeight="bold")),
                        y=alt.Y("Cost (LKR):Q", axis=alt.Axis(labelColor="#0f172a", titleColor="#065f46")),
                        tooltip=["Category", alt.Tooltip("Cost (LKR):Q", format=",")]
                    )
                    .properties(height=260)
                    .configure_view(strokeWidth=0, fill="#ffffff")
                    .configure_axis(gridColor="#e2e8f0", domainColor="#cbd5e1", labelColor="#0f172a", titleColor="#065f46")
                    .configure(background="#ffffff")
                )
                st.altair_chart(chart, width="stretch")

        st.markdown("#### Itemized Cost Details & Status Transparency")
        items = b_info.get("items", [])
        if items:
            df_items = pd.DataFrame(items)
            display_cols = [c for c in ["item", "cost", "currency", "source", "status"] if c in df_items.columns]
            st.dataframe(df_items[display_cols], width="stretch")

        st.markdown("<div style='padding-bottom: 0.625rem;'></div>", unsafe_allow_html=True)

    # 4. TRANSPORT TAB
    with tab_transport:
        st.markdown("### 🚗 Intercity Routes & Transport Options")
        for route in data.get("transport", []):
            st.markdown(f"#### 🛣️ {route.get('origin')} ➔ {route.get('destination')}")
            
            c_cost = route.get('estimated_cost_lkr', 0.0)
            rec_mode = route.get('recommended_mode', 'taxi').upper()
            cost_range = route.get('cost_range_lkr', {})
            min_c = cost_range.get('min', 0.0) if cost_range else 0.0
            max_c = cost_range.get('max', 0.0) if cost_range else 0.0
            
            caption_str = f"📏 Distance: {route.get('distance_km')} km | ⏱️ Travel Time: ~{route.get('duration_minutes')} mins | 💵 Recommended Cost ({rec_mode}): LKR {c_cost:,.2f}"
            if min_c > 0 and max_c > 0:
                caption_str += f" (Option Range: LKR {min_c:,.0f} – LKR {max_c:,.0f})"
            caption_str += f" | Source: {route.get('source')}"
            
            st.caption(caption_str)
            
            opts = route.get("options", [])
            if opts:
                df_opts = pd.DataFrame(opts)
                disp_cols = [c for c in ["mode", "name", "estimated_cost_lkr", "currency", "duration_minutes", "status", "source"] if c in df_opts.columns]
                st.dataframe(df_opts[disp_cols], width="stretch")

        st.markdown("<div style='padding-bottom: 0.625rem;'></div>", unsafe_allow_html=True)

    # 5. HOTELS TAB
    with tab_hotels:
        st.markdown("### 🏨 Accommodation Options")
        for h_dest in data.get("hotels", []):
            dest_name = h_dest.get("destination", "Destination")
            st.markdown(f"#### Accommodations in {dest_name}")
            st.caption(f"Source: {h_dest.get('source')} | Status: {h_dest.get('status')}")
            
            if h_dest.get("status") == "unavailable":
                st.warning(h_dest.get("message", "Hotel live-search unavailable."))
            else:
                h_list = h_dest.get("hotels", [])
                if h_list:
                    df_h = pd.DataFrame(h_list)
                    h_cols = [c for c in ["name", "price_lkr", "currency", "rating", "reviews", "amenities", "status"] if c in df_h.columns]
                    st.dataframe(df_h[h_cols], width="stretch")

        st.markdown("<div style='padding-bottom: 0.625rem;'></div>", unsafe_allow_html=True)

    # 6. ACTIVITIES TAB
    with tab_activities:
        st.markdown("### 🧗 Activities & Experiences")
        acts = data.get("activities", [])
        if acts:
            df_acts = pd.DataFrame(acts)
            st.dataframe(df_acts[["title", "destination", "category", "estimated_cost", "currency", "source", "status"]], width="stretch")

        st.markdown("<div style='padding-bottom: 0.625rem;'></div>", unsafe_allow_html=True)

    # 7. WEATHER TAB
    with tab_weather:
        st.markdown("### 🌤️ Live Weather Forecast for All Trip Locations (Open-Meteo API)")
        weather_list = data.get("weather", [])
        itin_days = data.get("itinerary", {}).get("days", [])
        
        if not weather_list:
            st.info("No weather data available for the selected destinations.")
        else:
            # 1. Master Trip Schedule
            if itin_days:
                st.markdown("#### 📅 Master Trip Daily Weather Schedule")
                master_schedule = []
                
                for day in itin_days:
                    day_num = day.get("day_number", 1)
                    dest = day.get("destination", "")
                    w_report = find_weather_for_location(dest, weather_list)
                    
                    forecast_items = w_report.get("forecast", []) if w_report else []
                    idx = min(day_num - 1, len(forecast_items) - 1) if forecast_items else -1
                    
                    d_str = ""
                    t_max = "27.5 °C"
                    t_min = "22.0 °C"
                    r_prob = "20%"
                    cond = "Partly cloudy"
                    adv = "Good weather for sightseeing"
                    
                    if idx >= 0:
                        f = forecast_items[idx]
                        d_str = f.get("date", "")
                        if f.get("temperature_max") is not None:
                            t_max = f"{f.get('temperature_max')} °C"
                        if f.get("temperature_min") is not None:
                            t_min = f"{f.get('temperature_min')} °C"
                        if f.get("rain_probability") is not None:
                            r_prob = f"{f.get('rain_probability')}%"
                        if f.get("condition"):
                            cond = f.get("condition")
                        if f.get("advisory"):
                            adv = f.get("advisory")
                    
                    master_schedule.append({
                        "Day": f"Day {day_num}",
                        "Date": d_str,
                        "Location / Destination": dest,
                        "Max Temp": t_max,
                        "Min Temp": t_min,
                        "Rain Chance": r_prob,
                        "Condition": cond,
                        "Travel Advisory": adv
                    })
                
                if master_schedule:
                    st.dataframe(pd.DataFrame(master_schedule), width="stretch", hide_index=True)
                st.divider()

            # 2. Location Breakdown
            st.markdown("#### 📍 Weather & Full Stay Forecast by Location")
            for w in weather_list:
                dest_name = w.get("destination", "Destination")
                st.markdown(f"##### Weather Forecast in **{dest_name}**")
                
                temp_c = w.get("temperature_celsius", 27.0)
                rain_p = w.get("rain_probability", 20)
                cond = w.get("condition", "Partly cloudy")
                total_days = w.get("total_days_forecasted", len(w.get("forecast", [])))
                
                col_w1, col_w2, col_w3, col_w4 = st.columns(4)
                with col_w1:
                    st.metric("Temperature", f"{temp_c:.1f} °C" if isinstance(temp_c, (int, float)) else f"{temp_c} °C")
                with col_w2:
                    st.metric("Rain Probability", f"{rain_p}%" if isinstance(rain_p, (int, float)) else f"{rain_p}")
                with col_w3:
                    st.metric("Condition", str(cond))
                with col_w4:
                    st.metric("Stay Days Covered", f"{total_days} Days")
                
                forecast = w.get("forecast", [])
                if forecast:
                    df_w = pd.DataFrame(forecast)
                    # Rename columns for pristine UI display if present
                    rename_map = {
                        "day": "Day",
                        "date": "Date",
                        "temperature_max": "Max Temp (°C)",
                        "temperature_min": "Min Temp (°C)",
                        "rain_probability": "Rain Chance (%)",
                        "condition": "Condition",
                        "advisory": "Travel Advisory"
                    }
                    df_w = df_w.rename(columns={k: v for k, v in rename_map.items() if k in df_w.columns})
                    st.dataframe(df_w, width="stretch", hide_index=True)
                    
                    # Highlight rainy days if any day rain_probability > 50%
                    rainy_days = [row.get("day", row.get("Day", "")) for row in forecast if row.get("rain_probability", row.get("Rain Chance (%)", 0)) > 50]
                    if rainy_days:
                        st.warning(f"🌧️ **Rain Alert:** High chance of rain on **{', '.join(rainy_days)}**. Pack rain gear!")
                else:
                    st.caption("No daily forecast details returned.")
                st.divider()

        st.markdown("<div style='padding-bottom: 0.625rem;'></div>", unsafe_allow_html=True)

    # 8. EMERGENCY TAB
    with tab_emergency:
        st.markdown("### 🚑 Sri Lanka Emergency Services & Hotlines")
        em = data.get("emergency", {})
        
        st.markdown("#### National Hotlines")
        hotlines = em.get("general_hotlines", {})
        for name, num in hotlines.items():
            st.write(f"📞 **{name}:** `{num}`")

        dest_facs = em.get("destinations_facilities", {})
        for dname, fac_data in dest_facs.items():
            st.markdown(f"#### Emergency Facilities near {dname}")
            hosp = fac_data.get("hospitals", [])
            pol = fac_data.get("police_stations", [])
            if hosp:
                st.caption("Hospitals:")
                st.dataframe(pd.DataFrame(hosp), width="stretch")
            if pol:
                st.caption("Police Stations:")
                st.dataframe(pd.DataFrame(pol), width="stretch")

        st.markdown("<div style='padding-bottom: 0.625rem;'></div>", unsafe_allow_html=True)
