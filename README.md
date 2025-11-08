# Secure Office Login: Facial Recognition System

This is a web application built with Flask and `face_recognition` that provides a secure, biometric login system. Users can authenticate by showing their face to a webcam. Successful logins are recorded in a MySQL database and displayed on a user dashboard.

---

## 🚀 Features

* **Real-time Facial Recognition:** Uses your webcam to grant access.
* **User Dashboard:** A secure dashboard page is shown after a successful login.
* **Session Management:** Uses Flask sessions to keep users logged in.
* **Login History:** Records all successful login attempts (user and timestamp) into a MySQL database.
* **Dynamic History Display:** The dashboard fetches and displays the 20 most recent login events from the database.

---

## 🛠️ Technologies Used

* **Backend:** Flask, Flask-SQLAlchemy
* **Database:** MySQL (connected with `pymysql`)
* **Face Recognition:** `face_recognition`, `opencv-python`, `numpy`
* **Frontend:** HTML, CSS, vanilla JavaScript (with `fetch` API)

---

## 📖 Installation & Setup Guide

Follow these steps to get the project running locally on your machine.

### 1. Clone the Repository

```bash
git clone [https://github.com/shabanask12/facial-login-app.git](https://github.com/shabanask12/facial-login-app.git)
cd facial-login-app
```

### 2. Create a Virtual Environment (Recommended)

```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies

This project relies on `face_recognition`, which can be tricky to install. It's best to install `dlib` and `cmake` first.

```bash
# Install dependencies
pip install flask flask_sqlalchemy pymysql opencv-python numpy face_recognition
```

> **Note:** If `face_recognition` fails, you may need to install C++ build tools or `cmake` first.
> `pip install cmake`
> `pip install dlib`
> Then try `pip install face_recognition` again.

### 4. Set Up the MySQL Database

This application is configured to connect to a local MySQL database with the following settings:
* **Database Name:** `py_project`
* **Username:** `root`
* **Password:** (empty)
* **Host:** `localhost`
* **Port:** `3306`

You must create the `py_project` database yourself using a tool like Laragon, XAMPP, or MySQL Workbench.

The application will **automatically create the `login_history` table** when you run `app.py` for the first time.

### 5. Add Your Known Faces

You must provide the images for the recognition system.

1.  Create a folder named `known_faces` in the root of the project.
2.  Add `.jpg` or `.png` images of the users you want to grant access.
3.  **Important:** Rename each image file to the user's name. The filename (without the extension) is used as the `username`.

    * `shabanask12.jpg` will be recognized as `"shabanask12"`
    * `jane.png` will be recognized as `"jane"`

---

## 🏃‍♂️ How to Use

1.  **Run the Server:**
    Once all dependencies are installed and your `known_faces` are added, run the main application:
    ```bash
    python app.py
    ```

2.  **Access the Application:**
    Open your web browser and go to:
    **`http://127.0.0.1:5000`**

3.  **Log In:**
    * Allow your browser to access the webcam.
    * Center your face in the camera.
    * Click the **"Login Now"** button.

4.  **View Dashboard:**
    * If your face is recognized, you will be redirected to the dashboard.
    * Here, you can see your username and a table of recent login history.

5.  **Log Out:**
    * Click the **"Logout"** button on the dashboard to end your session and return to the login page.
