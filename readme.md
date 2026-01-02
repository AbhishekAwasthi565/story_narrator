# 📖 Children's Story AI Narrator (Limited Memory)

A Generative AI chatbot built with **LangChain** and **Streamlit** that acts as a whimsical narrator for the story of *Little Red Riding Hood*. This project demonstrates the implementation of **Limited Memory** in AI systems.

## 🚀 Features
- **Generative AI:** Powered by the Mistral-7B-Instruct-v0.2 model.
- **Limited Memory:** Implements a sliding window memory ($k=3$), allowing the AI to maintain context without overloading its token limits.
- **Interactive UI:** A user-friendly Streamlit interface with manual API key configuration.

## 🛠️ Hugging Face API Setup
To run this project, you must use a **Fine-grained Token** from Hugging Face with specific permissions.

### Required Permissions:
1.  **Inference:** Enable "Make calls to Inference Providers".
2.  **Serverless:** Enable "Make calls to the serverless Inference API".



## 📦 Installation
1. Clone this repository:
   ```bash
   git clone [https://github.com/AbhishekAwasthi565/story_narrator](https://github.com/AbhishekAwasthi565/story_narrator.git)
   cd your-repo-name
```
Install dependencies:

```bash
pip install -r requirements.txt
```
Run the app:

```bash
streamlit run app.py
```
📓 Notebook Access
For a step-by-step technical breakdown, you can view the Google Colab Notebook included in this repository.


---

## 🔑 3. Documenting API Permissions
To ensure the evaluator doesn't get the `403 Forbidden` error you encountered, you **must** include an image in your GitHub.

1.  **Take a Screenshot:** Go to your [Hugging Face Token Settings](https://huggingface.co/settings/tokens) and take a screenshot of the "Inference" section with the checkboxes selected.
2.  **Upload to GitHub:**
    * Create a folder named `assets` in your repo.
    * Upload your screenshot as `permission.png`.
    * In the README, the code `![Permissions](assets/permission.png)` will display it.

---

## 📜 4. `requirements.txt`
Create this file so others can install the same versions you used:
```text
streamlit
langchain-huggingface
langchain-community
langchain-core
huggingface_hub
```
---
