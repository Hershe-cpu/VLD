import subprocess
import sys

import streamlit as st

from AI.mentor import ask_mentor
from experiments.circular_motion import circular_motion_simulation
from experiments.free_fall import free_fall_simulation
from experiments.newtons_laws import newtons_law_simulation
from experiments.ohms_law import ohms_law_simulation
from experiments.pendulum import pendulum_simulation
from experiments.projectile import projectile_simulation
from experiments.wave_interference import wave_interference_simulation

# PAGE CONFIGURATION


st.set_page_config(page_title="Virtual Lab Director", page_icon="🔬", layout="wide")


# TITLE

st.title("🔬 Virtual Lab Director")

st.write("An AI-powered interactive physics laboratory for Classes 9–12.")

st.caption("Predict → Experiment → Observe → Explain")


# CLASS / CHAPTER / EXPERIMENT MAPPING

classes = {
    "Class 9": {
        "Motion": ["Projectile Motion", "Circular Motion"],
        "Force and Laws of Motion": ["Newton's Laws"],
        "Gravitation": ["Free Fall"],
    },
    "Class 10": {"Light": ["Optics"], "Electricity": ["Ohm's Law"]},
    "Class 11": {
        "Motion": ["Projectile Motion", "Circular Motion"],
        "Laws of Motion": ["Newton's Laws"],
        "Gravitation": ["Free Fall"],
        "Oscillations": ["SHM Pendulum"],
        "Waves": ["Wave Interference"],
    },
    "Class 12": {
        "Current Electricity": ["Ohm's Law"],
        "Ray Optics": ["Optics"],
        "Waves": ["Wave Interference"],
    },
}


# SESSION STATE

if "simulation_data" not in st.session_state:
    st.session_state.simulation_data = {}

if "ai_feedback" not in st.session_state:
    st.session_state.ai_feedback = {}


# AI MENTOR FUNCTION


def run_ai_mentor(experiment_name, parameters, simulation_results, key_prefix):

    st.divider()

    st.subheader("Prediction Challenge")

    # Prediction question

    prediction_questions = {
        "Projectile Motion": "If the launch angle changes from 30° to 60°, what do you predict will happen to the range?",
        "SHM Pendulum": "What do you predict will happen to the period if the pendulum length increases?",
        "Circular Motion": "What do you predict will happen to centripetal acceleration if velocity increases?",
        "Wave Interference": "What do you predict will happen when two waves meet in phase?",
        "Newton's Laws": "What do you predict will happen to acceleration if the applied force increases?",
        "Free Fall": "What do you predict will happen to fall time if the initial height increases?",
        "Ohm's Law": "What do you predict will happen to current if resistance increases?",
        "Optics": "What do you predict will happen to image position if the object distance changes?",
    }

    question = prediction_questions.get(
        experiment_name, "What do you predict will happen in this experiment?"
    )

    st.info(question)

    # --------------------------------------------------------
    # Student hypothesis
    # --------------------------------------------------------

    hypothesis = st.text_area(
        "Write your hypothesis:",
        key=f"{key_prefix}_hypothesis",
        placeholder="Write your prediction here...",
    )

    # --------------------------------------------------------
    # Test hypothesis
    # --------------------------------------------------------

    if st.button(" Test My Hypothesis", key=f"{key_prefix}_ai_button"):
        if not hypothesis.strip():
            st.warning("Please write your hypothesis first.")

        else:
            with st.spinner(" AI Mentor is analyzing your hypothesis..."):
                feedback = ask_mentor(
                    experiment=experiment_name,
                    parameters=parameters,
                    student_hypothesis=hypothesis,
                    simulation_results=simulation_results,
                )

            # Save AI response
            st.session_state.ai_feedback[key_prefix] = feedback

            st.success("AI Mentor analysis complete!")

    # Display AI feedback

    if key_prefix in st.session_state.ai_feedback:
        st.divider()

        st.subheader(" AI Lab Mentor")

        st.markdown(st.session_state.ai_feedback[key_prefix])


# CLASS SELECTION


selected_class = st.selectbox("Select Class", list(classes.keys()))


# CHAPTER SELECTION


chapters = classes[selected_class]

selected_chapter = st.selectbox("Select Chapter", list(chapters.keys()))


# EXPERIMENT SELECTION


experiments = chapters[selected_chapter]

selected_experiment = st.selectbox("Select Experiment", experiments)

# SELECTED EXPERIMENT


st.divider()

st.subheader(" Selected Experiment")

st.info(f"{selected_class} → {selected_chapter} → {selected_experiment}")

# 1. PROJECTILE MOTION


if selected_experiment == "Projectile Motion":
    st.subheader("Projectile Motion")

    col1, col2 = st.columns(2)

    with col1:
        velocity = st.slider(
            "Initial Velocity (m/s)", 1.0, 50.0, 20.0, key="projectile_velocity"
        )

        angle = st.slider(
            "Launch Angle (degrees)", 5.0, 85.0, 45.0, key="projectile_angle"
        )

    with col2:
        gravity = st.slider("Gravity (m/s²)", 1.0, 20.0, 9.81, key="projectile_gravity")

        height = st.slider(
            "Initial Height (m)", 0.0, 20.0, 0.0, key="projectile_height"
        )

    with col1:
        if st.button(" Run Projectile Simulation", key="projectile_run"):
            fig, animation, results = projectile_simulation(
                velocity, angle, gravity, height
            )

            st.session_state.simulation_data["projectile"] = {
                "fig": fig,
                "results": results,
                "parameters": {
                    "Initial velocity": f"{velocity} m/s",
                    "Launch angle": f"{angle}°",
                    "Gravity": f"{gravity} m/s²",
                    "Initial height": f"{height} m",
                },
            }

            # New simulation = remove previous AI response
            st.session_state.ai_feedback.pop("projectile", None)

    with col2:
        if st.button("🎮 Launch Animation", key="projectile_pygame"):
            subprocess.Popen(
                [
                    sys.executable,
                    "experiments/projectile_pygame.py",
                    str(velocity),
                    str(angle),
                    str(gravity),
                    str(height),
                ]
            )

    if "projectile" in st.session_state.simulation_data:
        data = st.session_state.simulation_data["projectile"]

        results = data["results"]

        st.pyplot(data["fig"])

        st.subheader(" Simulation Results")

        col1, col2, col3 = st.columns(3)

        col1.metric("Flight Time", f"{results['flight_time']:.2f} s")

        col2.metric("Maximum Height", f"{results['maximum_height']:.2f} m")

        col3.metric("Range", f"{results['range']:.2f} m")

        run_ai_mentor(
            experiment_name="Projectile Motion",
            parameters=data["parameters"],
            simulation_results={
                "Flight time": f"{results['flight_time']:.2f} s",
                "Maximum height": f"{results['maximum_height']:.2f} m",
                "Range": f"{results['range']:.2f} m",
            },
            key_prefix="projectile",
        )


# 2. SHM PENDULUM


elif selected_experiment == "SHM Pendulum":
    st.subheader("Simple Pendulum")

    length = st.slider("Pendulum Length (m)", 0.2, 5.0, 1.0, key="pendulum_length")

    gravity = st.slider("Gravity (m/s²)", 1.0, 20.0, 9.81, key="pendulum_gravity")

    angle = st.slider("Initial Angle (degrees)", 5, 45, 15, key="pendulum_angle")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🕐 Run Pendulum Simulation", key="pendulum_run"):
            fig, animation, results = pendulum_simulation(length, gravity, angle)

            st.session_state.simulation_data["pendulum"] = {
                "fig": fig,
                "results": results,
                "parameters": {
                    "Pendulum length": f"{length} m",
                    "Gravity": f"{gravity} m/s²",
                    "Initial angle": f"{angle}°",
                },
            }

            st.session_state.ai_feedback.pop("pendulum", None)
    with col2:
        if st.button("🎮 Launch Animation", key="pendulum_pygame"):
            subprocess.Popen(
                [
                    sys.executable,
                    "experiments/pendulum_pygame.py",
                    str(length),
                    str(gravity),
                    str(angle),
                ]
            )

    if "pendulum" in st.session_state.simulation_data:
        data = st.session_state.simulation_data["pendulum"]

        results = data["results"]

        st.pyplot(data["fig"])

        st.subheader(" Simulation Results")

        st.metric("Period", f"{results['period']:.2f} s")

        run_ai_mentor(
            experiment_name="SHM Pendulum",
            parameters=data["parameters"],
            simulation_results={
                "Period": f"{results['period']:.2f} s",
                "Length": f"{results['length']} m",
                "Gravity": f"{results['gravity']} m/s²",
            },
            key_prefix="pendulum",
        )

# 3. CIRCULAR MOTION


elif selected_experiment == "Circular Motion":
    st.subheader(" Circular Motion")

    radius = st.slider("Radius (m)", 0.5, 10.0, 2.0, key="circular_radius")

    velocity = st.slider("Velocity (m/s)", 1.0, 30.0, 5.0, key="circular_velocity")

    if st.button(" Run Circular Motion Simulation", key="circular_run"):
        fig, animation, results = circular_motion_simulation(radius, velocity)

        st.session_state.simulation_data["circular"] = {
            "fig": fig,
            "results": results,
            "parameters": {"Radius": f"{radius} m", "Velocity": f"{velocity} m/s"},
        }

        st.session_state.ai_feedback.pop("circular", None)

    if "circular" in st.session_state.simulation_data:
        data = st.session_state.simulation_data["circular"]

        results = data["results"]

        st.pyplot(data["fig"])

        st.subheader("Simulation Results")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Centripetal Acceleration",
            f"{results['centripetal_acceleration']:.2f} m/s²",
        )

        col2.metric("Angular Velocity", f"{results['angular_velocity']:.2f} rad/s")

        col3.metric("Period", f"{results['period']:.2f} s")

        run_ai_mentor(
            experiment_name="Circular Motion",
            parameters=data["parameters"],
            simulation_results={
                "Centripetal acceleration": f"{results['centripetal_acceleration']:.2f} m/s²",
                "Angular velocity": f"{results['angular_velocity']:.2f} rad/s",
                "Period": f"{results['period']:.2f} s",
            },
            key_prefix="circular",
        )


# 4. WAVE INTERFERENCE


elif selected_experiment == "Wave Interference":
    st.subheader(" Wave Interference")

    amplitude = st.slider("Amplitude", 0.5, 2.0, 1.0, key="wave_amplitude")

    wavelength = st.slider("Wavelength (m)", 0.5, 5.0, 2.0, key="wave_wavelength")

    frequency = st.slider("Frequency (Hz)", 0.5, 5.0, 1.0, key="wave_frequency")

    if st.button("Run Wave Simulation", key="wave_run"):
        fig, animation, results = wave_interference_simulation(
            amplitude, wavelength, frequency
        )

        st.session_state.simulation_data["wave"] = {
            "fig": fig,
            "results": results,
            "parameters": {
                "Amplitude": amplitude,
                "Wavelength": f"{wavelength} m",
                "Frequency": f"{frequency} Hz",
            },
        }

        st.session_state.ai_feedback.pop("wave", None)

    if "wave" in st.session_state.simulation_data:
        data = st.session_state.simulation_data["wave"]

        results = data["results"]

        st.pyplot(data["fig"])

        st.subheader(" Simulation Results")

        st.metric("Resultant Amplitude", f"{results['resultant_amplitude']:.2f}")

        st.info("This simulation demonstrates constructive interference.")

        run_ai_mentor(
            experiment_name="Wave Interference",
            parameters=data["parameters"],
            simulation_results={
                "Amplitude of each wave": results["amplitude_each_wave"],
                "Resultant amplitude": results["resultant_amplitude"],
                "Wavelength": results["wavelength"],
                "Frequency": results["frequency"],
                "Interference": results["interference_type"],
            },
            key_prefix="wave",
        )


# 5. NEWTON'S LAWS


elif selected_experiment == "Newton's Laws":
    st.subheader(" Newton's Second Law")

    mass = st.slider("Mass (kg)", 0.5, 20.0, 5.0, key="newton_mass")

    force = st.slider("Applied Force (N)", 0.0, 100.0, 20.0, key="newton_force")

    if st.button(" Run Newton's Law Simulation", key="newton_run"):
        fig, animation, results = newtons_law_simulation(mass, force)

        st.session_state.simulation_data["newton"] = {
            "fig": fig,
            "results": results,
            "parameters": {"Mass": f"{mass} kg", "Applied force": f"{force} N"},
        }

        st.session_state.ai_feedback.pop("newton", None)

    if "newton" in st.session_state.simulation_data:
        data = st.session_state.simulation_data["newton"]

        results = data["results"]

        st.pyplot(data["fig"])

        st.subheader("Simulation Results")

        col1, col2, col3 = st.columns(3)

        col1.metric("Acceleration", f"{results['acceleration']:.2f} m/s²")

        col2.metric("Final Velocity", f"{results['final_velocity']:.2f} m/s")

        col3.metric("Final Position", f"{results['final_position']:.2f} m")

        run_ai_mentor(
            experiment_name="Newton's Laws",
            parameters=data["parameters"],
            simulation_results={
                "Acceleration": f"{results['acceleration']:.2f} m/s²",
                "Final velocity": f"{results['final_velocity']:.2f} m/s",
                "Final position": f"{results['final_position']:.2f} m",
            },
            key_prefix="newton",
        )

# 6. FREE FALL


elif selected_experiment == "Free Fall":
    st.subheader(" Free Fall")

    height = st.slider("Initial Height (m)", 1.0, 100.0, 20.0, key="freefall_height")

    gravity = st.slider("Gravity (m/s²)", 1.0, 20.0, 9.81, key="freefall_gravity")

    if st.button(" Run Free Fall Simulation", key="freefall_run"):
        fig, animation, results = free_fall_simulation(height, gravity)

        st.session_state.simulation_data["freefall"] = {
            "fig": fig,
            "results": results,
            "parameters": {
                "Initial height": f"{height} m",
                "Gravity": f"{gravity} m/s²",
            },
        }

        st.session_state.ai_feedback.pop("freefall", None)

    if "freefall" in st.session_state.simulation_data:
        data = st.session_state.simulation_data["freefall"]

        results = data["results"]

        st.pyplot(data["fig"])

        st.subheader(" Simulation Results")

        col1, col2 = st.columns(2)

        col1.metric("Fall Time", f"{results['fall_time']:.2f} s")

        col2.metric("Final Velocity", f"{results['final_velocity']:.2f} m/s")

        run_ai_mentor(
            experiment_name="Free Fall",
            parameters=data["parameters"],
            simulation_results={
                "Initial height": f"{results['initial_height']} m",
                "Gravity": f"{results['gravity']} m/s²",
                "Fall time": f"{results['fall_time']:.2f} s",
                "Final velocity": f"{results['final_velocity']:.2f} m/s",
            },
            key_prefix="freefall",
        )

# 7. OHM'S LAW

elif selected_experiment == "Ohm's Law":
    st.subheader(" Ohm's Law")

    voltage = st.slider("Voltage (V)", 0.0, 20.0, 10.0, key="ohm_voltage")

    resistance = st.slider("Resistance (Ω)", 1.0, 100.0, 10.0, key="ohm_resistance")

    if st.button(" Run Ohm's Law Simulation", key="ohm_run"):
        fig, animation, results = ohms_law_simulation(voltage, resistance)

        st.session_state.simulation_data["ohm"] = {
            "fig": fig,
            "results": results,
            "parameters": {"Voltage": f"{voltage} V", "Resistance": f"{resistance} Ω"},
        }

        st.session_state.ai_feedback.pop("ohm", None)

    if "ohm" in st.session_state.simulation_data:
        data = st.session_state.simulation_data["ohm"]

        results = data["results"]

        st.pyplot(data["fig"])

        st.subheader("Simulation Results")

        st.metric("Current", f"{results['current']:.3f} A")

        run_ai_mentor(
            experiment_name="Ohm's Law",
            parameters=data["parameters"],
            simulation_results={
                "Voltage": f"{results['voltage']} V",
                "Resistance": f"{results['resistance']} Ω",
                "Current": f"{results['current']:.3f} A",
            },
            key_prefix="ohm",
        )
