# 🛍️ E-Commerce Platform with Dynamic Form Builder

A modern, full-stack e-commerce platform built with Next.js 14 and Django 5, featuring a powerful drag-and-drop form builder for admin users and a planned employee portal for product management.

## ✨ Features

### 🎨 Dynamic Form Builder
- **11 Field Types**: Text, Email, Number, Textarea, Select, Radio, Checkbox, Date, Time, File Upload, URL
- **Drag & Drop Interface**: Intuitive field reordering using @dnd-kit library
- **Real-Time Preview**: Instant form visualization with live updates
- **Windows-Style Compact UI**: Efficient space utilization for power users
- **Field Customization**: Label, placeholder, validation rules, required status
- **Unlimited Options**: Dynamic options editor for select/radio fields
- **JSON Schema Storage**: Flexible form structure with UUID-based keys

### 🔐 Authentication & Authorization
- **JWT Token Authentication**: Secure admin login with session management
- **Role-Based Access Control**: Admin and employee permission levels
- **OAuth Integration Ready**: Extensible authentication system

### 🎯 Planned Features
- **Employee Portal**: Product management dashboard for staff
- **Product CRUD**: Complete inventory management system
- **Order Management**: Track and process customer orders
- **Real-Time Chat**: Django Channels integration for customer support
- **Sales Analytics**: Dashboard with insights and reporting
- **PostgreSQL Migration**: Production-ready database deployment

## 🏗️ Architecture

### Frontend (Next.js 14 + TypeScript)
```
frontend/
├── app/
│   ├── admin/           # Admin dashboard and form builder
│   ├── auth/            # OAuth callback handlers
│   └── (customer)/      # Customer-facing pages
├── components/
│   ├── form-builder/    # Modular form builder components
│   └── [shared]/        # Reusable UI components
├── lib/                 # Type definitions and utilities
└── hooks/               # Custom React hooks
```

### Backend (Django 5 + DRF)
```
backend/
├── authentication/      # User management and JWT auth
├── form_builder/        # Form templates and submissions
├── ecommerce_backend/   # Core settings and configuration
└── [products]/          # Planned: Product management app
```

## 🚀 Getting Started

### Prerequisites
- **Node.js** 18+ and npm
- **Python** 3.10+
- **Git**

### Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/MilanChaulagain/ecommerce-start.git
cd ecommerce-start
```

#### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows PowerShell:
venv\Scripts\Activate.ps1
# Windows CMD:
venv\Scripts\activate.bat
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
# Copy .env.example to .env and configure:
# - SECRET_KEY
# - JWT_SECRET_KEY
# - DB_ENGINE (default: sqlite3)
# - OAUTH credentials (optional)

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

#### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Create .env.local file
# NEXT_PUBLIC_API_URL=http://localhost:8000

# Start development server
npm run dev
```

#### 4. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Admin Login**: http://localhost:3000/admin/login
- **Form Builder**: http://localhost:3000/admin/form-builder

## 📦 Tech Stack

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS 4
- **Drag & Drop**: @dnd-kit (core, sortable, utilities)
- **Icons**: Lucide React
- **State Management**: React Hooks + Custom Hooks

### Backend
- **Framework**: Django 5.0.1
- **API**: Django REST Framework 3.14
- **Authentication**: JWT (PyJWT 2.8.0)
- **Database**: SQLite (dev) / PostgreSQL (production)
- **CORS**: django-cors-headers 4.3.1
- **Configuration**: python-decouple 3.8

## 🎨 Form Builder Components

The form builder follows a modular architecture with focused, maintainable components:

| Component | Purpose | Size |
|-----------|---------|------|
| `FieldPalette.tsx` | Field type selector sidebar | 35 lines |
| `FormCanvas.tsx` | Drag-drop form preview canvas | 115 lines |
| `FieldSettingsPanel.tsx` | Field property editor | Varies |
| `TextFieldSettings.tsx` | Text-specific settings | Compact |
| `NumberFieldSettings.tsx` | Number-specific settings | Compact |
| `OptionsFieldSettings.tsx` | Dynamic options editor | Feature-rich |
| `CheckboxFieldSettings.tsx` | Checkbox settings | Minimal |
| `FormPreviewModal.tsx` | Full-screen form preview | 170 lines |
| `useFormBuilder.ts` | State management hook | 180 lines |

## 🔑 Key Design Decisions

### Modular Component Architecture
Refactored from a monolithic 850-line file into 8 focused components for improved maintainability, testability, and code reusability.

### Windows-Style Compact UI
- **Font Sizes**: `text-xs`, `text-[10px]`
- **Padding**: `py-1`, `py-1.5`, `px-2`
- **Sidebar Widths**: `w-52` (palette), `w-64` (settings)
- **Goal**: Maximize screen real estate for professional power users

### Type-Safe Development
Central type definitions in `lib/form-builder-types.ts` ensure consistency across all components with TypeScript interfaces for `FormField`, `FieldType`, `FormTemplate`, and `FormBuilderState`.

### JSON Schema Storage
Forms stored as flexible JSON schemas in PostgreSQL/SQLite JSONB fields, enabling dynamic field types without schema migrations.

## 📚 Documentation

- **[Quick Start Guide](QUICK_START.md)**: Get up and running in 5 minutes
- **[Admin System Guide](ADMIN_SYSTEM_GUIDE.md)**: Complete admin features walkthrough
- **[OAuth Setup Guide](Notes/OAUTH_SETUP_GUIDE.md)**: Configure social authentication
- **[Theme Guide](Notes/THEME_GUIDE.md)**: Customize UI appearance
- **[Form Builder Refactoring](Notes/FORM_BUILDER_REFACTORING.md)**: Architecture decisions
- **[Implementation Status](Notes/IMPLEMENTATION_STATUS.md)**: Current progress

## 🗺️ Roadmap

### Phase 1: Foundation ✅
- [x] Django backend with REST API
- [x] Next.js frontend with TypeScript
- [x] JWT authentication system
- [x] Basic admin dashboard

### Phase 2: Form Builder ✅
- [x] 11 field types implementation
- [x] Drag-and-drop field reordering
- [x] Real-time form preview
- [x] Modular component architecture
- [x] Windows-style compact design

### Phase 3: Employee Portal 🚧
- [ ] Product management CRUD
- [ ] Category and inventory system
- [ ] Order processing workflow
- [ ] Role-based access control
- [ ] Compact dashboard UI

### Phase 4: Production Ready 📋
- [ ] PostgreSQL migration
- [ ] Django Channels (WebSocket support)
- [ ] Real-time chat system
- [ ] Sales analytics dashboard
- [ ] Performance optimization
- [ ] Comprehensive testing suite

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Milan Chaulagain**
- GitHub: [@MilanChaulagain](https://github.com/MilanChaulagain)

## 🙏 Acknowledgments

- [Next.js](https://nextjs.org/) - React framework
- [Django](https://www.djangoproject.com/) - Python web framework
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS framework
- [@dnd-kit](https://dndkit.com/) - Drag and drop toolkit
- [Lucide](https://lucide.dev/) - Beautiful icon set

## 📞 Support

For support, email your-email@example.com or open an issue in the GitHub repository.

---

**Built with ❤️ using Next.js, Django, and TypeScript**
