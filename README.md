# 🎓 StudentZone

**Nationwide Student Network for Dutch Higher Education**

StudentZone is a collaborative, cross-university platform designed to unite students in the Netherlands by field of study—starting with AI and expanding outward. It empowers students to connect beyond campus borders, share knowledge, and elevate learning together.

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-5.2.4-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Development-orange.svg)](https://github.com/Appie0904/studentzone)

## 🔑 Core Purpose

- **Connect**: Facilitate communication among Dutch students studying the same discipline at different universities
- **Collaborate**: Enable group study, project formation, resource-sharing, and peer-to-peer mentoring
- **Grow**: Foster a robust academic community that accelerates learning, innovation, and professional development

## 🎯 Key Features

### 1. Field-Based Communities
- Students join groups based on their discipline (e.g., "Artificial Intelligence", "Data Science") and study level
- Automatically connects peers from TU Delft, UvA, UU, and more

### 2. Peer Q&A & Discussion Channels
- Students can post questions, share notes, discuss lecture topics, or troubleshoot code
- Community voting helps surface best answers and contributors

### 3. Project & Event Collaboration
- Browse or create cross-institution projects
- Share events: hackathons, guest lectures, workshops, internships—open to all NL students

### 4. Resource Library
- Open sharing of lecture slides, code samples, book summaries, and study guides (students own their uploads)

### 5. Smart Matching & Partner Finder
- Find study partners by topic, university, or interest area
- Optional mentorship pairing—e.g., senior AI students mentoring juniors

### 6. Reputation & Recognition
- Upvote helpful contributions, earn badges (e.g., "Top Helper"), and build a respected profile

### 7. Multilingual Interface
- Support for NL and English usage, accommodating varying language preferences

## 🚀 Quick Start

### Prerequisites

- Python 3.12 or higher
- pip (Python package installer)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Appie0904/studentzone.git
   cd studentzone
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Visit the application**
   - Open your browser and go to `http://127.0.0.1:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

## 📁 Project Structure

```
studentzone/
├── core/                    # User profiles, universities, study fields
│   ├── models.py           # Core models (UserProfile, University, StudyField, etc.)
│   ├── views.py            # Core views (home, profile, search, etc.)
│   ├── forms.py            # User profile forms
│   └── admin.py            # Admin interface configuration
├── communities/            # Field-based communities and events
│   ├── models.py           # Community models
│   ├── views.py            # Community management views
│   ├── forms.py            # Community forms
│   └── admin.py            # Community admin
├── discussions/            # Q&A and discussion system
│   ├── models.py           # Discussion and comment models
│   ├── views.py            # Discussion views
│   ├── forms.py            # Discussion forms
│   └── admin.py            # Discussion admin
├── projects/               # Project collaboration and study partners
│   ├── models.py           # Project and study partner models
│   ├── views.py            # Project views
│   ├── forms.py            # Project forms
│   └── admin.py            # Project admin
├── resources/              # Educational resource library
│   ├── models.py           # Resource models
│   ├── views.py            # Resource views
│   ├── forms.py            # Resource forms
│   └── admin.py            # Resource admin
├── templates/              # HTML templates
│   ├── base.html           # Base template
│   ├── core/               # Core app templates
│   ├── communities/        # Community templates
│   ├── discussions/        # Discussion templates
│   ├── projects/           # Project templates
│   └── resources/          # Resource templates
├── static/                 # Static files (CSS, JS, images)
│   ├── css/                # Stylesheets
│   ├── js/                 # JavaScript files
│   └── images/             # Images and media
├── studentzone/            # Main project settings
│   ├── settings.py         # Django settings
│   ├── urls.py             # Main URL configuration
│   └── wsgi.py             # WSGI configuration
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## 🛠️ Technology Stack

- **Backend**: Django 5.2.4
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Frontend**: Bootstrap 5, Font Awesome, Vanilla JavaScript
- **Authentication**: Django's built-in user system
- **File Uploads**: Django's FileField with Pillow for image processing
- **Deployment**: WSGI compatible (Gunicorn, uWSGI)

## 📊 Database Models

### Core Models
- `University` - Dutch universities
- `StudyField` - Academic disciplines
- `UserProfile` - Extended user profiles
- `Badge` & `UserBadge` - Achievement system

### Community Models
- `Community` - Field-based communities
- `CommunityMembership` - User memberships
- `CommunityEvent` - Community events
- `CommunityInvitation` - Invitation system

### Discussion Models
- `Discussion` - Discussion threads
- `Comment` - Discussion comments
- `Vote` - Voting system (generic)
- `DiscussionBookmark` - User bookmarks

### Project Models
- `Project` - Collaborative projects
- `ProjectMembership` - Team memberships
- `ProjectApplication` - Project applications
- `StudyPartner` - Study partner profiles

### Resource Models
- `Resource` - Educational resources
- `ResourceCategory` - Resource categories
- `ResourceVote` - Resource voting
- `ResourceCollection` - User collections

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Settings

Key settings in `studentzone/settings.py`:

- `TIME_ZONE = 'Europe/Amsterdam'`
- `LANGUAGE_CODE = 'en-us'`
- Static and media file configurations
- Database settings
- Installed apps configuration

## 🧪 Testing

Run the test suite:

```bash
python manage.py test
```

## 📝 API Documentation

The platform provides RESTful endpoints for:

- User authentication and profiles
- Community management
- Discussion and Q&A
- Project collaboration
- Resource sharing
- Study partner matching

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests: `python manage.py test`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

## 📄 License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

**Key Points:**
- ✅ **Free to use, modify, and distribute**
- ✅ **Must share source code** when distributing modified versions
- ✅ **Cannot be made proprietary** - derivatives must also be open source
- ❌ **Cannot be sold commercially** without sharing the source code
- ❌ **Cannot be integrated into closed-source software**

## 🙏 Acknowledgments

- Django community for the excellent framework
- Bootstrap team for the responsive UI components
- Font Awesome for the beautiful icons
- All contributors and supporters of the StudentZone project

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Appie0904/studentzone/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Appie0904/studentzone/discussions)
- **Email**: [Contact us](mailto:support@studentzone.nl)

## 🗺️ Roadmap

- [ ] User registration and authentication
- [ ] Community creation and management
- [ ] Discussion and Q&A system
- [ ] Resource upload and sharing
- [ ] Project collaboration tools
- [ ] Study partner matching
- [ ] Mobile app development
- [ ] Advanced search and filtering
- [ ] Real-time notifications
- [ ] API for third-party integrations

---

**Made with ❤️ for Dutch students by Dutch students** 