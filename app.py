import streamlit as st
import pandas as pd
import joblib
import shap
import matplotlib.pyplot as plt

st.set_page_config(menu_items={'Get Help': None, 'Report a bug': None, 'About': None})

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="EduPredict AI", page_icon="🎓", layout="wide")

# Soft Custom CSS for a modern look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #4CAF50; color: white; border: none; }
    .stButton>button:hover { background-color: #45a049; }
    .prediction-card { padding: 20px; border-radius: 15px; background-color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    [data-testid="stMetricValue"] { font-size: 28px; color: #4CAF50; }
    .sidebar-contact { padding: 10px; border-top: 1px solid #ccc; margin-top: 20px; font-size: 0.9em; background-color: #d4fae0; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}        
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOAD ASSETS ---
@st.cache_resource
def load_assets():
    model = joblib.load('final_slim_model.pkl')
    features = joblib.load('top_10_features.pkl')
    explainer = shap.TreeExplainer(model)
    return model, features, explainer

try:
    model, top_10_features, explainer = load_assets()
except Exception as e:
    st.error(f"Error loading model files: {e}")
    st.stop()

# --- 3. SIDEBAR NAVIGATION & CONTACT FORM ---
st.sidebar.title("🛠️ Control Panel")
app_mode = st.sidebar.radio("Choose Analysis Mode", ["Single Student", "Batch Processing"])

  # --- CONTACT SUPPORT FORM , CONTACT & BIO---
st.sidebar.markdown("---")
st.sidebar.subheader("📩 Send a Message")

  # EMBEDDED CONTACT FORM
st.sidebar.markdown(f"""
    <form action="https://formspree.io/f/mgonpepg" method="POST">
        <label>
         Your email:
         <input type="email" name="email" placeholder="Your Email" required 
            style="width: 100%; padding: 10px; margin-bottom: 10px; border-radius: 5px; border: 1px solid #ccc;">
         </label>
         <label>
         Your message:
         <textarea name="message" placeholder="How can I help you?" required 
            style="width: 100%; padding: 10px; margin-bottom: 10px; border-radius: 5px; border: 1px solid #ccc; height: 100px;"></textarea>
         </label>
         <button type="submit" style="width: 50%; border-radius: 20px; height: 3em; background-color: #4CAF50; color: white; border: none;">Send</button>
         <input type="hidden" name="_next" value="https://edupredict-ai.streamlit.app">
    </form>
    """, unsafe_allow_html=True)

    #  PROFESSIONAL BIO CARD
st.sidebar.markdown(f"""
    <div style="padding: 10px; border-top: 1px solid #ccc; margin-top: 20px; font-size: 0.9em; background-color: #d4fae0; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <p style="margin-bottom:2px; font-size:1.0em; color:#666;">Developed by:</p>
        <h3 style="margin:0; color:#2E7D32; font-size:1.3em;">Emmanuel NIYIGENA</h3>
        <p style="margin:5px 0; font-weight:bold; color:#333;">📞 +250 781 068 599</p>
        <p style="font-size:0.95em; font-weight:bold; color:#0c2369; line-height:1.2;">
            University of Rwanda - College of Education<br><br>
            <span style="color:#666; font-style:italic;">AI Performance Model v3.0</span>
        </p>
    </div>
    """, unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.info("Model Accuracy: **86.4%**\n\nLast Updated: March 2026")




# --- 4. MODE: SINGLE STUDENT ---
if app_mode == "Single Student":
    st.title("🎓 Student Performance Predictor")
    st.write("Determine a student's academic standing based on classroom behavior (86.4% Accuracy).")

    col1, col2 = st.columns([1, 1.5], gap="large")

    with col1:
        st.subheader("📊 Engagement Metrics")
        visited = st.slider("Visited Resources", 0, 100, 70)
        hands = st.slider("Raised Hands", 0, 100, 60)
        announcements = st.slider("Announcements Viewed", 0, 100, 40)
        discussion = st.slider("Discussion Participation", 0, 100, 50)
        
        st.subheader("📋 Student Profile")
        absence = st.selectbox("Absence Days", ["Under-7", "Above-7"])
        relation = st.selectbox("Primary Contact", ["Mum", "Father"])
        survey = st.selectbox("Parent Answered Survey?", ["Yes", "No"])
        satisfaction = st.selectbox("Parent Satisfaction", ["Good", "Bad"])
        gender = st.selectbox("Gender", ["M", "F"])
        section = st.selectbox("Section", ["A", "B", "C"])

    with col2:
        if st.button("✨ Run AI Analysis"):
            raw_data = {
                'VisITedResources': visited, 'raisedhands': hands,
                'AnnouncementsView': announcements, 'Discussion': discussion,
                'StudentAbsenceDays': absence, 'Relation': relation,
                'ParentAnsweringSurvey': survey, 'ParentschoolSatisfaction': satisfaction,
                'gender': gender, 'SectionID': section
            }
            df_input = pd.DataFrame([raw_data])
            df_encoded = pd.get_dummies(df_input).reindex(columns=top_10_features, fill_value=0)
            
            prediction = model.predict(df_encoded)[0]
            class_map = {'H': 'High Success 🌟', 'M': 'Medium (Steady) 📘', 'L': 'Low (At Risk) ⚠️'}
            result_label = class_map.get(prediction, prediction)
            
            advice = []
            if visited < 40: advice.append("Access to online materials is low.")
            if hands < 30: advice.append("Classroom participation needs encouragement.")
            if absence == 'Above-7': advice.append("High absenteeism is hindering progress.")
            
            st.markdown(f'<div class="prediction-card"><h3>Prediction: {result_label}</h3></div>', unsafe_allow_html=True)
            
            if advice:
                st.warning("**Intervention Required:**\n- " + "\n- ".join(advice))
            else:
                st.success("**Perfect!** The student shows healthy engagement patterns.")

            


            st.write("---")
            st.write("### 🧠 AI Decision Reasoning")
            
            try:
                # 1. Get the SHAP values
                s_values = explainer.shap_values(df_encoded)
                
                # 2. Determine the correct index for the predicted class
                # (H=2, M=1, L=0)
                # target_idx = 2 if prediction == 'H' else (1 if prediction == 'M' else 0)

                # This automatically finds the correct index for whatever the model predicted
                target_idx = list(model.classes_).index(prediction)
                
                # 3. Create a SHAP Explanation Object (Vertical Layout)
                # This handles the overlapping labels perfectly!
                exp = shap.Explanation(
                    values=s_values[:, :, target_idx] if not isinstance(s_values, list) else s_values[target_idx],
                    base_values=explainer.expected_value[target_idx],
                    data=df_encoded.values,
                    feature_names=top_10_features
                )

                # 4. Plot the Waterfall
                fig, ax = plt.subplots(figsize=(10, 6))
                # We use exp[0] because we are explaining the 1st (and only) student row
                shap.plots.waterfall(exp[0], show=False) 
                
                plt.title(f"Reasoning for {result_label}", fontsize=14, pad=20)
                st.pyplot(fig)
                plt.clf() # Clean up memory
                
            except Exception as e:
                st.info("Visual explanation is loading background patterns...")
                # Optional: print(e) to your console if you need to debug
                print(e)


# --- 5. MODE: BATCH PROCESSING ---
else:
    st.title("📂 Batch Analysis Dashboard")
    st.write("Upload a CSV file to analyze multiple students instantly.")
    
    uploaded_file = st.file_uploader("Upload CSV/Excel", type=["csv", "xlsx"])
    
    if uploaded_file:
        data = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        
        if st.button("🚀 Process All Students"):
            progress_bar = st.progress(0)
            
            df_batch_encoded = pd.get_dummies(data).reindex(columns=top_10_features, fill_value=0)
            progress_bar.progress(50)
            
            preds = model.predict(df_batch_encoded)
            data['AI_Prediction'] = preds
            progress_bar.progress(100)
            
            st.success("Analysis Complete!")

            # --- NEW: SUMMARY STATS SECTION ---
            st.write("### 📈 Classroom Summary Statistics")
            total_students = len(data)
            high_count = (preds == 'H').sum()
            med_count = (preds == 'M').sum()
            low_count = (preds == 'L').sum()

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Total Students", total_students)
            m2.metric("High Performers", high_count)
            m3.metric("Medium Level", med_count)
            m4.metric("At Risk (Low)", low_count, delta=f"{low_count/total_students*100:.1f}%", delta_color="inverse")
            
            st.write("---")

            # --- PREVIEW & DISTRIBUTION ---
            col_table, col_chart = st.columns([2, 1])

            with col_table:
                st.write("### 📋 Prediction Details")
                st.dataframe(data, use_container_width=True)

            with col_chart:
                st.write("### 📊 Distribution")
                counts = pd.Series(preds).value_counts()
                # Ensure correct order if possible
                fig_pie, ax_pie = plt.subplots()
                colors = {'H': '#99ff99', 'M': '#66b3ff', 'L': '#ff9999'}
                # Sort colors based on labels present in counts
                current_colors = [colors.get(label, '#eeeeee') for label in counts.index]
                
                ax_pie.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=90, colors=current_colors)
                ax_pie.axis('equal')
                st.pyplot(fig_pie)
            
            csv = data.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Full Results", data=csv, file_name="batch_analysis.csv")

