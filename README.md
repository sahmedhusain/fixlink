<p align="center">
  <img src="static/css/logo.png" alt="FixLink Logo" width="140" />
</p>

# 🔧 FixLink

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-3.2+-092E20?style=flat&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.x-7952B3?style=flat&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE.md)

**FixLink** is a full-stack home services marketplace web platform engineered with Python, Django, and Bootstrap. FixLink connects residential and commercial property owners with verified trade service companies (electricians, plumbers, HVAC technicians, general contractors), enabling service catalog management, quote requests, appointment scheduling, and order tracking.

---

## ⚡ Key Highlights

- **Dual Persona Workflows**: Distinct user experiences tailored for **Customer Accounts** (browse services, request quotes, track active orders) and **Service Provider Companies** (manage listings, view job requests, update fulfillment status).
- **Service Catalog Management**: Service providers can post, edit, and categorize home service offerings with pricing metrics and descriptions.
- **Job Request Engine**: Customers can select service providers, submit detailed job specifications, and track order lifecycles (Pending -> Accepted -> In Progress -> Completed).
- **Company Profiles**: Service provider landing pages displaying company contact info, available service categories, ratings, and customer reviews.
- **Relational Data Persistence**: SQLite database schema with ORM relationships binding Customers, Companies, Services, and RequestedService records.

---

## 📋 Table of Contents

- [Key Highlights](#-key-highlights)
- [System Architecture](#-system-architecture)
- [Service Request Sequence Flow](#-service-request-sequence-flow)
- [Setup & Execution](#-setup--execution)
- [Project Directory Structure](#-project-directory-structure)
- [License](#-license)

---

## 🖼️ Application Dashboards

| Customer Workspace | Service Provider Dashboard |
| :---: | :---: |
| ![Customer Workspace](static/css/customer.png) | ![Company Workspace](static/css/company.png) |

---

## 🏗️ System Architecture

```mermaid
graph TD
    A[Web Browser / Client] --> B[Django URL Router & Middleware]
    B --> C{User Persona Type?}
    
    C -- Customer User --> D1[Customer Workspace: Profile & Requests]
    C -- Service Provider --> D2[Company Workspace: Catalog & Job Management]
    
    D1 --> E1[Browse Services / Submit Service Request]
    D2 --> E2[Manage Service Listings / Fulfill Orders]
    
    E1 --> F[Django Views & Forms Processing Layer]
    E2 --> F
    F --> G[Django ORM Data Models]
    
    G --> H1[User & Customer Profiles]
    G --> H2[Company Profiles]
    G --> H3[Service Offerings]
    G --> H4[RequestedService Orders]
    
    H1 --> I[(SQLite Database)]
    H2 --> I
    H3 --> I
    H4 --> I
```

---

## 📐 Service Request Sequence Flow

```mermaid
sequenceDiagram
    participant Customer as Customer User
    participant View as Django View / Bootstrap UI
    participant Service as Service Catalog Model
    participant Order as RequestedService Model
    participant Company as Service Provider

    Customer->>View: Browse Marketplace & Select Service
    View-->>Customer: Display Service Detail & Request Form
    Customer->>View: Submit Job Details & Preferred Date
    View->>Order: Create RequestedService (Status = Pending)
    Order-->>Company: Notify Company Dashboard
    
    Company->>View: Review Job & Accept Order
    View->>Order: Update Status -> Accepted / In Progress
    Company->>View: Mark Job Completed
    View->>Order: Update Status -> Completed
    View-->>Customer: Order Completed Summary & Invoice Record
```

---

## 🚀 Setup & Execution

### Prerequisites

- **Python**: 3.9 or newer installed.
- **pip**: Package installer.

---

### Setup & Run

1. **Clone Repository**:
   ```bash
   git clone https://github.com/sahmedhusain/fixlink.git
   cd fixlink
   ```

2. **Setup Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install django
   ```

4. **Execute Migrations & Seed Sample Data**:
   ```bash
   python3 manage.py migrate
   python3 seed_data.py
   ```

5. **Start Django Development Server**:
   ```bash
   python3 manage.py runserver
   ```
   *FixLink will run locally at `http://127.0.0.1:8000`.*

---

## 📂 Project Directory Structure

```
fixlink/
├── manage.py              # Django CLI utility
├── seed_data.py           # Database seeding script
├── fixlink/               # Core project configuration
│   ├── settings.py        # Django settings configuration
│   ├── urls.py            # Global URL routing
│   └── wsgi.py            # WSGI application entrypoint
├── main/                  # Core app (authentication & home views)
│   ├── models.py          # User profile models
│   ├── views/             # Authentication & landing page handlers
│   └── templates/         # Base layout templates
├── services/              # Marketplace app (catalog & order fulfillment)
│   ├── models.py          # Service, Company, and RequestedService models
│   ├── views.py           # Service CRUD & order lifecycle handlers
│   └── templates/         # Marketplace & service request templates
└── static/                # Static assets (CSS, JS, images)
```

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE.md) for details.
