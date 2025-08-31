import cv2
import numpy as np
import os
from PIL import Image
import io
import base64
import pickle

class FaceRecognitionModel:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.known_face_encodings = []
        self.known_face_names = []
        self.known_face_ids = []
        self.model_file = 'face_model.yml'
        self.labels_file = 'face_labels.pkl'
        self.model_loaded = False
    
    def load_known_faces(self):
        """Load semua wajah yang sudah terdaftar dari database"""
        if self.model_loaded:
            return
            
        try:
            # Try to load existing model first
            if self.load_model():
                self.model_loaded = True
                return
        except:
            pass
        
        from database import db, Mahasiswa
        
        # Ambil semua mahasiswa dari database
        mahasiswa_list = Mahasiswa.query.all()
        
        faces = []
        labels = []
        
        for mahasiswa in mahasiswa_list:
            if mahasiswa.foto_wajah and os.path.exists(mahasiswa.foto_wajah):
                try:
                    # Load dan process wajah
                    image = cv2.imread(mahasiswa.foto_wajah)
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    face_locations = self.face_cascade.detectMultiScale(gray, 1.1, 4)
                    
                    if len(face_locations) > 0:
                        (x, y, w, h) = face_locations[0]
                        face_roi = gray[y:y+h, x:x+w]
                        face_roi = cv2.resize(face_roi, (100, 100))
                        
                        faces.append(face_roi)
                        labels.append(mahasiswa.id)
                        
                        self.known_face_names.append(mahasiswa.nama)
                        self.known_face_ids.append(mahasiswa.id)
                        print(f"Loaded face for: {mahasiswa.nama}")
                except Exception as e:
                    print(f"Error loading face for {mahasiswa.nama}: {e}")
        
        # Train the recognizer if we have faces
        if faces and labels:
            self.recognizer.train(faces, np.array(labels))
            self.save_model()
            self.model_loaded = True
    
    def save_model(self):
        """Save trained model"""
        try:
            self.recognizer.save(self.model_file)
            with open(self.labels_file, 'wb') as f:
                pickle.dump({
                    'names': self.known_face_names,
                    'ids': self.known_face_ids
                }, f)
        except Exception as e:
            print(f"Error saving model: {e}")
    
    def load_model(self):
        """Load trained model"""
        try:
            if os.path.exists(self.model_file):
                self.recognizer.read(self.model_file)
                with open(self.labels_file, 'rb') as f:
                    data = pickle.load(f)
                    self.known_face_names = data['names']
                    self.known_face_ids = data['ids']
                return True
        except Exception as e:
            print(f"Error loading model: {e}")
        return False
    
    def add_face(self, image_path, mahasiswa_id, nama):
        """Tambah wajah baru ke database"""
        try:
            # Load dan process wajah baru
            image = cv2.imread(image_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            face_locations = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            
            if len(face_locations) > 0:
                (x, y, w, h) = face_locations[0]
                face_roi = gray[y:y+h, x:x+w]
                face_roi = cv2.resize(face_roi, (100, 100))
                
                # Retrain the model with new face
                self.recognizer.train([face_roi], np.array([mahasiswa_id]))
                
                self.known_face_names.append(nama)
                self.known_face_ids.append(mahasiswa_id)
                
                self.save_model()
                print(f"Added new face for: {nama}")
                return True
            else:
                print("No face detected in the image")
                return False
        except Exception as e:
            print(f"Error adding face: {e}")
            return False
    
    def recognize_face(self, image_data):
        """Recognize wajah dari image data (base64 atau file path)"""
        # Load faces if not loaded yet
        if not self.model_loaded:
            self.load_known_faces()
            
        try:
            # Handle base64 image data
            if isinstance(image_data, str) and image_data.startswith('data:image'):
                # Decode base64 image
                image_data = image_data.split(',')[1]
                image_bytes = base64.b64decode(image_data)
                nparr = np.frombuffer(image_bytes, np.uint8)
                image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            else:
                # Handle file path
                image = cv2.imread(image_data)
            
            if image is None:
                return None, "Invalid image data"
            
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            face_locations = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            
            if len(face_locations) == 0:
                return None, "No face detected in the image"
            
            # Process each detected face
            for (x, y, w, h) in face_locations:
                face_roi = gray[y:y+h, x:x+w]
                face_roi = cv2.resize(face_roi, (100, 100))
                
                # Predict the face
                label, confidence = self.recognizer.predict(face_roi)
                
                # Lower confidence means better match (LBPH returns distance)
                if confidence < 100:  # Threshold for recognition
                    # Find the corresponding name
                    if label in self.known_face_ids:
                        idx = self.known_face_ids.index(label)
                        nama = self.known_face_names[idx]
                        
                        # Convert confidence to percentage (0-100)
                        confidence_percent = max(0, 100 - confidence)
                        
                        return {
                            'mahasiswa_id': int(label),
                            'nama': nama,
                            'confidence': float(confidence_percent),
                            'face_found': True
                        }, None
            
            return None, "Face not recognized"
            
        except Exception as e:
            return None, f"Error in face recognition: {str(e)}"
    
    def detect_face(self, image_data):
        """Detect apakah ada wajah dalam gambar"""
        try:
            # Handle base64 image data
            if isinstance(image_data, str) and image_data.startswith('data:image'):
                image_data = image_data.split(',')[1]
                image_bytes = base64.b64decode(image_data)
                nparr = np.frombuffer(image_bytes, np.uint8)
                image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            else:
                image = cv2.imread(image_data)
            
            if image is None:
                return False
            
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            face_locations = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            return len(face_locations) > 0
            
        except Exception as e:
            print(f"Error detecting face: {e}")
            return False
    
    def get_face_count(self, image_data):
        """Hitung jumlah wajah dalam gambar"""
        try:
            if isinstance(image_data, str) and image_data.startswith('data:image'):
                image_data = image_data.split(',')[1]
                image_bytes = base64.b64decode(image_data)
                nparr = np.frombuffer(image_bytes, np.uint8)
                image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            else:
                image = cv2.imread(image_data)
            
            if image is None:
                return 0
            
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            face_locations = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            return len(face_locations)
            
        except Exception as e:
            print(f"Error counting faces: {e}")
            return 0

# Global instance
face_model = FaceRecognitionModel()
