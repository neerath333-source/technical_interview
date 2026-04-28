# Project Structure Breakdown (கோப்பு கட்டமைப்பு விளக்கம்)

This document explains the role of each file in the project. / இந்த ஆவணத்தில் ப்ராஜெக்ட்டில் உள்ள ஒவ்வொரு கோப்பின் வேலையும் விளக்கப்பட்டுள்ளது.

---

### 1. `backend/run.py`
- **English:** The entry point of the application. It initializes the app using the factory and starts the Flask development server. It also handles the 'Testing Mode' switch.
- **Tamil:** இது தான் ஆப்-இன் நுழைவாயில். இதிலிருந்து தான் பிளாஸ்க் (Flask) சர்வர் ஆரம்பமாகும். நாம் டெஸ்டிங் மோடில் இருக்கிறோமா இல்லையா என்பதை இதுதான் முடிவு செய்யும்.

### 2. `backend/app/__init__.py`
- **English:** Implements the **Application Factory Pattern**. It sets up Flask, registers Blueprints, initializes Swagger and the Database, and defines global error handlers (404, 500).
- **Tamil:** இது ஆப்-இன் மூளை போன்றது. லாகின், டாஸ்க் போன்ற பிரிவுகளை (Blueprints) இணைப்பது, மற்றும் எரர்-களை கையாள்வது இதன் முக்கிய வேலை.

### 3. `backend/app/config.py`
- **English:** Centralized configuration management. It reads sensitive data from the `.env` file and provides them to the rest of the application.
- **Tamil:** ஆப்புக்கு தேவையான ரகசிய சாவிகள் (Keys) மற்றும் டேட்டாபேஸ் முகவரிகளை இது சேமித்து வைக்கும்.

### 4. `backend/app/database.py`
- **English:** Handles the MongoDB connection using the `PyMongo` library.
- **Tamil:** இது டேட்டாபேஸுடன் (MongoDB) தொடர்பை ஏற்படுத்த உதவும் ஒரு சிறிய கோப்பு.

### 5. `backend/app/auth/routes.py`
- **English:** Contains the API endpoints for User Registration and Login. It handles incoming JSON data and communicates with MongoDB.
- **Tamil:** பயனர் பதிவு (Register) மற்றும் உள்நுழைவுக்கான (Login) வழிகளை இது கொண்டுள்ளது.

### 6. `backend/app/auth/utils.py`
- **English:** The security hub. Contains functions for password hashing (Bcrypt), JWT token generation/decoding, input validation (Regex), and the `@token_required` decorator.
- **Tamil:** இது தான் பாதுகாப்பு மையம். பாஸ்வேர்டை மாற்றுவது, டோக்கனை சரிபார்ப்பது மற்றும் இமெயில் போன்ற தகவல்களை சோதிப்பது இதன் வேலை.

### 7. `backend/app/tasks/routes.py`
- **English:** Implements the core business logic. Contains secure CRUD operations for tasks, ensuring strict multi-tenant data isolation using the user's `tenant_id`.
- **Tamil:** இது தான் ஆப்-இன் முக்கிய பகுதி. இங்குதான் டாஸ்க்குகளை உருவாக்குவது, பார்ப்பது, மாற்றுவது மற்றும் நீக்குவது போன்ற வேலைகள் பாதுகாப்பான முறையில் நடக்கும்.

### 8. `backend/tests/test_pytest_flow.py`
- **English:** Automated integration tests using `pytest`. It simulates the entire user journey to ensure everything is working correctly.
- **Tamil:** இது ஒரு தானியங்கி சோதனை கோப்பு. நாம் எழுதிய கோட் சரியாக வேலை செய்கிறதா என்று இதுவே செக் செய்துவிடும்.

### 9. `backend/requirements.txt`
- **English:** List of all Python libraries needed to run the project.
- **Tamil:** இந்த ப்ராஜெக்ட் இயங்குவதற்கு தேவையான அனைத்து பைதான் லைப்ரரிகளின் பட்டியல்.

### 10. `backend/.env`
- **English:** Stores sensitive environment variables like database URIs and secret keys. Not meant to be shared publicly.
- **Tamil:** ரகசியமான பாஸ்வேர்ட்கள் மற்றும் ரகசிய குறியீடுகளை பாதுகாப்பாக வைக்க இது உதவும்.
