import streamlit as st
import json
from pathlib import Path

# Define image paths
IMAGE_PATHS = {
    1: "optimium.png",  # Initial Step
    3: "optimium2.png",  # Remote Configuration Step
    # Add more images for other steps if needed
}

# Define the default template
default_template = {
    "device_name": "YOUR_DEVICE_ALIAS",
    "model": {"framework": "YOUR_FRAMEWORK"},
    "remote": {"address": "YOUR_REMOTE_IP_ADDRESS", "port": "YOUR_REMOTE_PORT"},
    "target_devices": {"host": {"arch": "ARM64", "os": "LINUX", "mattr": "auto"}},
    "runtime": {"num_threads": 1},
    "optimization": {"opt_log_key": "USER_LOG_KEY", "enable_tuning": False},
}

# Initialize session state for step tracking and data storage
if "step" not in st.session_state:
    st.session_state.step = 1
if "template" not in st.session_state:
    st.session_state.template = default_template

def save_json(template, filepath):
    with open(filepath, "w") as f:
        json.dump(template, f, indent=4)    
    st.success(f"Configuration saved to {filepath}")

# Display dynamic image based on the current step
current_image = IMAGE_PATHS.get(st.session_state.step, "optimium.png")
st.image(current_image, use_container_width=True)

def increment_step():
    st.session_state.step += 1

def decrement_step():
    st.session_state.step -= 1

# Step 1: Device Information
if st.session_state.step == 1:
    st.header("Step 1: Device Information")
    device_name = st.text_input("Device Name", st.session_state.template.get("device_name", "YOUR_DEVICE_ALIAS"))
    st.session_state.template["device_name"] = device_name

# Step 2: Model Information
if st.session_state.step == 2:
    st.header("Step 2: Model Information")
    framework = st.selectbox("Framework", ["torch", "tflite"], index=0)
    st.session_state.template["model"]["framework"] = framework

# Step 3: Remote Configuration
if st.session_state.step == 3:
    st.header("Step 3: Remote Configuration")
    remote_address = st.text_input(
        "Remote Address (leave empty for localhost)",
        st.session_state.template["remote"].get("address", ""),
    )
    remote_port = st.text_input(
        "Remote Port", 
        str(st.session_state.template["remote"].get("port", "32264"))
    )
    st.session_state.template["remote"]["address"] = "localhost" if remote_address == "" else remote_address
    st.session_state.template["remote"]["port"] = int(remote_port) if remote_port.isdigit() else 32264

# Step 4: Target Device
if st.session_state.step == 4:
    st.header("Step 4: Target Device")
    arch = st.selectbox("Architecture", ["X86_64", "ARM64"], index=0)
    os = st.selectbox("OS", ["LINUX", "ANDROID"], index=0)
    st.session_state.template["target_devices"]["host"]["arch"] = arch
    st.session_state.template["target_devices"]["host"]["os"] = os

# Step 5: Runtime Configuration
if st.session_state.step == 5:
    st.header("Step 5: Runtime Configuration")
    num_threads = st.number_input(
        "Number of Threads", 
        min_value=1, 
        value=st.session_state.template["runtime"]["num_threads"],
    )
    st.session_state.template["runtime"]["num_threads"] = num_threads

# Step 6: Optimization Options
if st.session_state.step == 6:
    st.header("Step 6: Optimization Options")
    opt_log_key = st.text_input(
        "Optimization Log Key",
        st.session_state.template["optimization"].get("opt_log_key", "USER_LOG_KEY"),
    )
    enable_tuning = st.checkbox(
        "Enable Hardware-Specific Auto-Tuning",
        value=st.session_state.template["optimization"].get("enable_tuning", False),
    )
    st.session_state.template["optimization"]["opt_log_key"] = opt_log_key
    st.session_state.template["optimization"]["enable_tuning"] = enable_tuning

    config_json = json.dumps(st.session_state.template, indent = 4)
    # save_filepath = st.text_input("Save Filepath", "user_arguments.json")
    col1, _, col2 = st.columns([5, 4, 1])
    with col1:
        # if st.button("Save Configuration"):
        #     save_json(st.session_state.template, Path(save_filepath))
        
            st.download_button(
                label="Download Configuration",
                data=config_json,
                file_name="user_arguments.json",
                mime="application/json"
            )
    with col2:
        st.button("Prev", on_click=decrement_step)

# Navigation Buttons
total_steps = 6  # Total number of steps in the process

if st.session_state.step == 1:
    col1, col2 = st.columns([9,1])
    with col2:
        st.button("Next", on_click=increment_step)
elif 1 < st.session_state.step < total_steps:
    col1, col2, col3 = st.columns([8,1,1])
    with col2:
        st.button("Prev", on_click=decrement_step)
    with col3:
        st.button("Next", on_click=increment_step)
else:
    st.empty()
# elif st.session_state.step == total_steps:
#     st.button("Prev", on_click=decrement_step)

