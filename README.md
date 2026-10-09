# CargoTrack

**A cargo and package management system for importing businesses, built with Python and Flask.**

CargoTrack helps a business manage cargo movements, the people who handle deliveries, payment records, and accountability between importers, motorists, and receivers. It is used by real people in a real business.

---

## About Me

I'm **Menur Yimgeta**, a fourth-year Computer Engineering student at Addis Ababa University, Ethiopia. I'm a Python developer who works with Django and Flask, and I like building software that solves real problems. CargoTrack is one of two commercial applications I have built. The other is [Merkato](https://github.com/YOUR_USERNAME/merkato), an inventory and sales management system.

---

## The Purpose of CargoTrack

An importing business has to keep track of many things at once: which cargo is where, who is carrying it, how much was supposed to be paid, how much was actually paid, and what happened when a package goes missing. Without a system, this information ends up in paper records and scattered spreadsheets, and it is hard to find out who is responsible when something goes wrong.

CargoTrack puts these operations in one place. It records what happened to each cargo, who handled it, and what was paid, so the business can follow the process from one stage to the next and investigate problems with real records.

CargoTrack is a cargo operations and record-tracking system. It does not provide live GPS tracking of vehicles.

---

## Features

### Cargo and package records
- Record cargo-related posts and package information
- Follow the records connected to each cargo movement

### Importer management
- Keep importer details such as names and phone numbers
- Flag importers who have caused problems and record the reasons
- Flagged importers are shown with a **red flag** so staff can see the problem straight away
- If someone tries to give a new package to a flagged importer, **the system rejects it**, so the same problem is not repeated

### Motorist and cargo handling
- Support workflows for the motorists who transport or handle cargo
- Keep records of the cargo each motorist is responsible for

### Wage and payment tracking
- Record the original wage and the actual amount paid to the receiver
- Compare the expected amount with the amount actually paid

### Final-post management and history
- Manage final-post records using package codes
- Keep post-history records
- Generate a final-post report
- Reset workflow that treats reset final posts as lost, helping the business investigate missing packages

### Access control and accountability
- Login protection for the whole system
- Role-based restrictions on sensitive actions, for example motorist-only actions and administrator-only final-post details

---

## Built With

| Part | Technology |
|---|---|
| Language | Python |
| Backend | Flask |
| Database | [PostgreSQL / SQLite / MySQL: write the one you use] |
| Frontend | [HTML, CSS, Bootstrap, JavaScript: keep what you use] |
| Server | [Linux, Gunicorn: keep what you use] |
| Hosting | [DigitalOcean or other: write where it runs] |

---

## What I Learned

- Building a complete Flask application used in a real business
- Designing relational databases for connected records such as importers, motorists, cargo, and payments
- Login, permissions, and role-based access control
- Turning real business problems, like missing packages, payment differences, and unreliable importers, into working features such as the red-flag and rejection system
- Deploying and maintaining an application for real users
- Fixing problems reported by the people who use the system

---

## Run It Locally

```bash
# 1. Clone the project
git clone https://github.com/MENA8729/kedir_2.git
cd cargotrack

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# 3. Install the requirements
pip install -r requirements.txt

# 4. Set your environment variables (secret key, database URL)

# 5. Start the app
flask run
```

---

## Contact

**Menur Yimgeta**
menayimge87@gmail.com
Computer Engineering Student, Addis Ababa University
Addis Ababa, Ethiopia

Feedback and suggestions are welcome.
