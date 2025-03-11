# Personality Archetype Predictor
🧠 **An AI-powered quiz that predicts personality archetypes based on user responses.** Built using **Flask (backend), Streamlit (frontend), and Machine Learning (Random Forest Classifier)**, this app provides real-time insights into decision-making styles and cognitive biases.  

## **🚀 Overview**  
This project **analyzes personality traits** based on quiz responses and maps them to **10 personality archetypes**. Using a trained **Machine Learning model**, the app provides a probability-based personality breakdown along with key strengths and biases.  

### **🔹 Tech Stack:**  
- **Backend**: Flask (Python)  
- **Frontend**: Streamlit (Python)  
- **ML Model**: Random Forest Classifier  
- **Deployment**: Render (Flask API) + Streamlit Cloud (Frontend)  

## **💡 How It Works**  
1️⃣ **User answers quiz questions** → Each option influences multiple **personality traits**.  
2️⃣ **Flask backend processes responses** → Updates the user’s **trait scores** dynamically.  
3️⃣ **ML model predicts archetypes** → Based on cumulative trait scores, the model assigns a **personality match**.  
4️⃣ **Streamlit frontend updates results** → The UI shows **live updates** of personality and trait breakdowns.  

## **🌎 Deployment Guide**  
### **1️⃣ Deploy Flask Backend on Render**  
1. Push `app.py` and `requirements.txt` to **GitHub**.  
2. Deploy on [Render](https://render.com/) as a **Web Service**:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `python app.py`
   - **Port:** `0.0.0.0:5000`  

### **2️⃣ Update Streamlit to Use Render API**  
Update `quiz_ui.py`:  
```python
API_URL = "https://your-flask-app.onrender.com"
```
Push changes to GitHub.  

### **3️⃣ Deploy Streamlit on Streamlit Cloud**  
1. Push `quiz_ui.py` to **GitHub**.  
2. Deploy on [Streamlit Cloud](https://share.streamlit.io/).  
3. Set **main script file**: `quiz_ui.py`.  

## **📈 Improving the Model**  
Currently, the **Random Forest Classifier** distributes probabilities across **10 personality archetypes**, meaning the **top match usually falls between 30-40%** rather than somthing around 90%. This is because the model considers a mix of traits rather than assigning **one dominant type**.  

Potential improvements:  
- Fine-tuning the model for **stronger personality predictions**.  
- Exploring **alternative ML models** for higher confidence in predictions.  
- Expanding the dataset to **improve accuracy** based on more responses.  

## **🔍 Final Personality Insights**  
At the end of the quiz, users receive an analysis of their **top personality matches** along with key decision-making traits and biases.  

**Example Archetypes:**  
🔹 **Precision Architect 🏗️**: Excels at structured problem-solving but may suffer from analysis paralysis.  
🔹 **Instinctive Maverick ⚡**: Highly adaptable and quick to act, but may fall into emotional decision-making.  
🔹 **Fearless Gambler 🎲**: Takes bold risks, but can sometimes ignore caution and data.  

## **📌 Next Steps**  
✅ **Optimize model predictions** for more confident personality matches.  
✅ **Enhance UI/UX** with better animations and interaction.  
✅ **Expand the dataset** to refine personality classifications.  
