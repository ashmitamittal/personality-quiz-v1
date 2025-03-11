import streamlit as st
import requests

# Backend API URL
API_URL = "http://127.0.0.1:5000"

# ✅ Page Title
st.title("🧠 AI-Powered Personality Quiz")

# ✅ Style Customization (CSS)
st.markdown(
    """
    <style>
        .quiz-container {
            text-align: center;
            font-size: 18px;
        }
        .stButton button {
            width: 100%;
            height: 50px;
            font-size: 16px;
        }
        .progress-container {
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 10px;
        }
        .trait-container {
            padding: 10px;
            border-radius: 10px;
            margin-top: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ✅ Initialize session state variables
if "question_index" not in st.session_state:
    st.session_state.question_index = 0

if "user_scores" not in st.session_state:
    st.session_state.user_scores = {}

if "top_archetypes" not in st.session_state:
    st.session_state.top_archetypes = {}

if "answered_questions" not in st.session_state:
    st.session_state.answered_questions = 0

# ✅ Fetch the current question
def get_question(index):
    try:
        response = requests.get(f"{API_URL}/get_question/{index}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"API Error: {str(e)}"}

# ✅ Submit the user's answer and update personality scores
def submit_answer(index, choice):
    try:
        response = requests.post(f"{API_URL}/submit_answer", json={"question_index": index, "chosen_option": choice})
        response.raise_for_status()
        response_data = response.json()

        # ✅ Accumulate trait scores instead of replacing them
        if "updated_scores" in response_data:
            for trait, value in response_data["updated_scores"].items():
                if trait in st.session_state.user_scores:
                    st.session_state.user_scores[trait] += value
                else:
                    st.session_state.user_scores[trait] = value

        # ✅ Update archetypes as usual
        st.session_state.top_archetypes = response_data["top_archetypes"]
        st.session_state.question_index += 1
        st.session_state.answered_questions += 1
        st.rerun()

    except requests.exceptions.RequestException as e:
        return {"error": f"API Error: {str(e)}"}

# ✅ Fetch the current question
question_index = st.session_state.question_index
question_data = get_question(question_index)

# ✅ If the quiz is complete, display the final breakdown
if "message" in question_data:
    st.success("🎉 Quiz Complete! Your final personality type has been calculated.")

    # ✅ Final Personality Breakdown
    st.subheader("🔍 **Final Personality Breakdown**")
    total_score = sum(st.session_state.top_archetypes.values())
    normalized_scores = {k: (v / total_score) * 100 for k, v in st.session_state.top_archetypes.items()} if total_score > 0 else {}
    sorted_archetypes = sorted(normalized_scores.items(), key=lambda x: x[1], reverse=True)

    for archetype, percentage in sorted_archetypes:
        if percentage > 0:
            st.progress(percentage / 100)
            st.write(f"**{archetype}**: {percentage:.2f}% match")

    # ✅ Final Trait Breakdown (Cumulative)
    st.subheader("📊 **Final Trait Breakdown**")
    total_traits = sum(st.session_state.user_scores.values())
    normalized_traits = {k: (v / total_traits) * 100 for k, v in st.session_state.user_scores.items()} if total_traits > 0 else {}
    sorted_traits = sorted(normalized_traits.items(), key=lambda x: x[1], reverse=True)

    for trait, percentage in sorted_traits:
        if percentage > 0:
            st.progress(percentage / 100)
            st.write(f"**{trait.replace('_', ' ')}**: {percentage:.2f}% match")

    # ✅ Show Insights for Top Archetypes
    st.subheader("🔎 **Archetype Insights for Your Results**")
    archetype_analysis = {
        "Trailblazer 🔥": "Balances visionary thinking with structured analysis, reducing overconfidence bias.",
        "Precision Architect 🏗️": "Excels at structured problem-solving but may suffer from analysis paralysis.",
        "Fearless Gambler 🎲": "Takes bold risks, but can sometimes ignore caution and data.",
        "Strategic Guardian 🛡️": "Makes cautious, well-calculated decisions but may avoid necessary risks.",
        "Diplomatic Orchestrator 🎭": "Great at relationship-building but may suffer from groupthink.",
        "Instinctive Maverick ⚡": "Highly adaptable and quick to act, but may fall into emotional decision-making.",
        "Perfectionist Engineer 🛠️": "Optimizes precision but may delay action waiting for perfection.",
        "Pragmatic Solver 🔍": "Finds efficient solutions but may accept suboptimal outcomes.",
        "Rebel Thinker 🧩": "Challenges the status quo but may resist authority even when unnecessary.",
        "Ethical Compass ⚖️": "Ensures integrity in leadership but may believe past ethical choices justify future ones."
    }

    for archetype, _ in sorted_archetypes:
        if archetype in archetype_analysis:
            st.write(f"**{archetype}**: {archetype_analysis[archetype]}")

else:
    # ✅ Display Question & Options First
    st.markdown('<div class="quiz-container">', unsafe_allow_html=True)
    if "question" in question_data and "options" in question_data:
        st.subheader(f"**Q{question_index + 1}:** {question_data['question']}")

        col1, col2 = st.columns(2)
        options = list(question_data["options"].items())

        for i, (key, option) in enumerate(options):
            button_label = option["description"]
            col = col1 if i % 2 == 0 else col2  

            if col.button(button_label, key=f"option_{i}"):
                submit_answer(question_index, key)

    st.markdown('</div>', unsafe_allow_html=True)

    # ✅ Live Personality Breakdown (After Question & Options)
    if st.session_state.top_archetypes:
        st.subheader("🔍 **Your Personality Breakdown (Live Updates)**")
        total_score = sum(st.session_state.top_archetypes.values())
        normalized_scores = {k: (v / total_score) * 100 for k, v in st.session_state.top_archetypes.items()} if total_score > 0 else {}
        sorted_archetypes = sorted(normalized_scores.items(), key=lambda x: x[1], reverse=True)

        for archetype, percentage in sorted_archetypes:
            if percentage > 0:
                st.progress(percentage / 100)
                st.write(f"**{archetype}**: {percentage:.2f}% match")

    # ✅ Live Trait Breakdown (After Question & Options)
    if st.session_state.user_scores:
        st.subheader("📊 **Your Trait Breakdown (Live Updates)**")
        total_traits = sum(st.session_state.user_scores.values())
        normalized_traits = {k: (v / total_traits) * 100 for k, v in st.session_state.user_scores.items()} if total_traits > 0 else {}
        sorted_traits = sorted(normalized_traits.items(), key=lambda x: x[1], reverse=True)

        for trait, percentage in sorted_traits:
            if percentage > 0:
                st.progress(percentage / 100)
                st.write(f"**{trait.replace('_', ' ')}**: {percentage:.2f}% match")
