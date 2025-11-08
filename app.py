import os
import cv2
import face_recognition
import numpy as np
import base64
from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone  # <-- CHANGE 1: 'timezone' is imported

# --- 1. App & DB Initialization ---
app = Flask(__name__)

# Set a secret key to use Flask's session feature
app.config['SECRET_KEY'] = 'your_super_secret_key_change_me_later' 

# Set the database connection string for Laragon (MySQL)
# Connects to the 'py_project' database as 'root' with no password
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/py_project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Disables a warning
db = SQLAlchemy(app)


# --- 2. Database Model ---
class LoginHistory(db.Model):
    """A model for the login history table."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    
    # --- CHANGE 2: Using 'datetime.now(timezone.utc)' for compatibility ---
    timestamp = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<LoginHistory {self.username} @ {self.timestamp}>'


# --- 3. Load Known Faces (Global Variables) ---
known_face_encodings = []
known_face_names = []

def load_known_faces():
    """
    Loads face encodings and names from the 'known_faces' directory.
    This runs once at startup.
    """
    global known_face_encodings, known_face_names
    
    known_face_encodings = []
    known_face_names = []
    
    print("Loading known faces...")
    for filename in os.listdir('known_faces'):
        if filename.endswith(('.jpg', '.png', '.jpeg')):
            try:
                # Load the image
                image_path = os.path.join('known_faces', filename)
                known_image = face_recognition.load_image_file(image_path)
                
                # Get the face encoding
                encodings = face_recognition.face_encodings(known_image)
                
                if len(encodings) > 0:
                    encoding = encodings[0]
                    # Get the name from the filename (e.g., "me.jpg" -> "me")
                    name = os.path.splitext(filename)[0]
                    
                    # Add to our lists
                    known_face_encodings.append(encoding)
                    known_face_names.append(name)
                    print(f"Loaded encoding for: {name}")
                else:
                    print(f"Warning: No face found in {filename}")
            except Exception as e:
                print(f"Error loading {filename}: {e}")

# --- 4. Flask Routes (Web Pages) ---

@app.route('/')
def index():
    """Serves the login page (index.html)."""
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Serves the new dashboard page."""
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/logout')
def logout():
    """Logs the user out and redirects to the login page."""
    session.pop('username', None) # Clear the session
    return redirect(url_for('index'))

# --- 5. API Endpoints (Data) ---

@app.route('/api/login', methods=['POST'])
def api_login():
    """Handles the face recognition login."""
    try:
        data = request.json
        image_data_url = data['image']
        
        # Decode the Base64 Image
        header, image_data = image_data_url.split(',', 1)
        image_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Perform Face Recognition
        face_locations = face_recognition.face_locations(img, model="hog")
        face_encodings = face_recognition.face_encodings(img, face_locations)
        
        found_name = "Unknown"
        is_match = False
        
        for face_encoding in face_encodings:
            # Compare with all known faces
            # Adjust tolerance here: 0.6 is a good default.
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
            
            if True in matches:
                first_match_index = matches.index(True)
                found_name = known_face_names[first_match_index]
                is_match = True
                break 
        
        if is_match:
            # --- SUCCESS! ---
            session['username'] = found_name
            
            # Record the login in the database
            new_log = LoginHistory(username=found_name)
            db.session.add(new_log)
            db.session.commit()
            
            # Tell the frontend to redirect
            return jsonify({
                'success': True,
                'redirect': url_for('dashboard')
            })
        else:
            # --- FAILURE ---
            return jsonify({'success': False, 'message': 'Access Denied: Face not recognized.'})
            
    except Exception as e:
        print(f"Error in /api/login: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/logins')
def api_logins():
    """Provides login history data to the dashboard."""
    if 'username' not in session:
        return jsonify([]), 401 # Unauthorized
    
    # Get the last 20 logins, most recent first
    logs = db.session.execute(db.select(LoginHistory).order_by(LoginHistory.timestamp.desc()).limit(20)).scalars()
    
    log_list = []
    for log in logs:
        log_list.append({
            'id': log.id,
            'username': log.username,
            'timestamp': log.timestamp.strftime("%Y-%m-%d %I:%M:%S %p")
        })
        
    return jsonify(log_list)

# --- 6. Run the Server ---
if __name__ == '__main__':
    # Create the database tables if they don't exist
    with app.app_context():
        db.create_all()
    
    # Load the faces *before* starting the server
    load_known_faces()
    
    # Start the Flask server
    print("Starting Flask server... Open http://127.0.0.1:5000 in your browser.")
    app.run(debug=True)