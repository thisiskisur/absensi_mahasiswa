# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- GitHub issue templates for bug reports and feature requests
- CONTRIBUTING.md with contribution guidelines
- MIT License
- Comprehensive .gitignore file

### Changed
- Updated README.md with comprehensive documentation
- Improved project structure and organization

## [1.0.0] - 2024-12-31

### Added
- Initial release of Sistem Absensi Mahasiswa
- Face recognition using OpenCV and LBPH Face Recognizer
- Admin dashboard for managing students and attendance
- Student attendance page with face capture
- JWT authentication system
- MySQL database integration
- React frontend with TailwindCSS
- Real-time camera integration
- Attendance history and statistics
- Responsive design for mobile and desktop
- Upload photo functionality for student registration
- Face verification before attendance submission
- Toast notifications for user feedback
- Protected routes based on user roles
- Search and filter functionality
- Automatic system startup script

### Features
- **Admin Features:**
  - Login with username/password
  - Dashboard with student and attendance statistics
  - Add new students with photo upload
  - View student list with search functionality
  - View attendance history
  - Delete students

- **Student Features:**
  - Login with NIM as username and password
  - Face capture for attendance
  - Real-time face verification
  - View attendance status for current day
  - Attendance history

- **Technical Features:**
  - Face detection and recognition
  - Secure password hashing
  - JWT token authentication
  - RESTful API endpoints
  - Cross-origin resource sharing (CORS)
  - Error handling and validation
  - Database backup and restore

### Security
- JWT token-based authentication
- Password hashing with Werkzeug
- Input validation and sanitization
- SQL injection protection
- CORS configuration for security

### Performance
- Lazy loading of face recognition models
- Optimized database queries
- Efficient image processing
- Responsive UI with smooth animations

---

## Version History

- **v1.0.0** - Initial release with core functionality
- **Unreleased** - Documentation and project structure improvements
