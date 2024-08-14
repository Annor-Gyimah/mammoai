# MammoAI

MammoAI is a web application built with Django, designed to assist radiologists in predicting and assessing breast cancer from mammogram images. It utilizes advanced machine learning models to determine whether an image is benign or malignant, and generates a heatmap to highlight the affected areas. Additionally, it provides a comprehensive risk assessment to aid in clinical decision-making.

## Features

- **User Authentication**: Secure sign-up and sign-in features for radiologists.
- **Patient Data Management**: Easy addition and management of patient data.
- **Mammogram Image Upload**: Seamless uploading of mammogram images for analysis.
- **AI Predictions**: Automatic classification of mammogram images as benign or malignant.
- **Heatmap Generation**: Visual representation of affected areas in mammogram images.
- **Risk Assessment**: Detailed risk analysis to support radiological evaluations.
- **Profile Management**: Options for updating personal information and changing passwords.
- **Dashboard**: User-friendly dashboard displaying all essential features and results.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/mammoai.git
   cd mammoai
   ```
2 Create a virtual environment and activate it:
  ```bash
  python3 -m venv env
  source env/bin/activate
  ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Apply migrations:
   ```bash
   python manage.py migrate
   ```
   
5. Start the development server:
   ```bash
   python manage.py runserver
   ```
## Usage
Sign Up: Create a new account using your professional email.
Log In: Access your dashboard by logging in with your credentials.
Add Patient Data: Navigate to the patient section and add relevant data.
Upload Mammogram: Upload mammogram images for analysis.
View Results: Check the AI predictions, heatmap, and risk assessment in your dashboard.
Profile Settings: Update your profile and password as needed.
Email Verification: Edit the .env file with the necessary email configurations to enable email verification for new users.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

