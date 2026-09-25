import ollama


MODEL_NAME = "qwen3:4b"


def ask_mentor(
    experiment,
    parameters,
    student_hypothesis,
    simulation_results
):

    prompt = f"""
You are an AI Physics Lab Mentor inside a virtual physics laboratory.

The student performed this experiment:

EXPERIMENT:
{experiment}

EXPERIMENT PARAMETERS:
{parameters}

STUDENT HYPOTHESIS:
{student_hypothesis}

ACTUAL PYTHON SIMULATION RESULTS:
{simulation_results}

IMPORTANT RULES:

1. The Python simulation is the source of truth.
2. Do not invent or modify numerical results.
3. Compare the student's hypothesis with the actual simulation.
4. Explain the physics in simple student-friendly language.
5. If the prediction is wrong, correct it gently.
6. Mention the important physics equation or concept.
7. Ask exactly ONE follow-up conceptual question.
8. Keep the response concise.

Return exactly this structure:

### PREDICTION
Was the student's prediction consistent with the simulation?

### OBSERVATION
What did the simulation actually show?

### WHY
Explain why this happened using physics.

### IMPORTANT CONCEPT
Give the key physics concept/equation.

### FOLLOW-UP QUESTION
Ask one conceptual question to make the student think further.
"""

    try:

        response = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]

    except Exception as e:

        return (
            "⚠️ AI Mentor is unavailable.\n\n"
            f"Error: {e}\n\n"
            "The physics simulation itself is still valid."
        )