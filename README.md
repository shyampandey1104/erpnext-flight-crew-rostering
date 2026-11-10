# ERPNext Flight Crew Rostering & DGCA FDTL Compliance ✈️👨‍✈️

![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![ERPNext](https://img.shields.io/badge/ERPNext-v14%20%7C%20v15-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Build](https://img.shields.io/badge/Build-Passing-brightgreen.svg)

An aviation crew pairing, pilot duty rostering, and civil aviation safety audit engine for **ERPNext HRMS & Airlines**. Enforces Directorate General of Civil Aviation (DGCA India) Flight Duty Time Limitations (FDTL) and mandatory fatigue rest windows.

---

## 🚀 Key Features

- **DGCA FDTL Rest Window Audit**: Enforces mandatory 12-hour continuous rest intervals between operational sectors.
- **Monthly Block Hour Capping**: Prevents pilots and cabin crew from exceeding the legal 100-hour monthly flying threshold.
- **Aircraft Fleet Rating Validation**: Validates pilot type rating certifications (Airbus A320, Boeing B737/B787) against aircraft equipment.
- **Fatigue & Alert Risk Mitigation**: Automates crew duty rescheduling to avoid safety compliance grounding notices.

---

## 📦 Installation & Setup

```bash
git clone https://github.com/shyampandey1104/erpnext-flight-crew-rostering.git
cd erpnext-flight-crew-rostering
pip install -r requirements.txt
```

---

## 🛠️ Usage Example

```python
from aviation.engine import FlightCrewRosteringEngine, CrewMember, FlightSector

engine = FlightCrewRosteringEngine()

pilot = CrewMember(
    crew_id="CPT-102",
    full_name="Capt. Sameer Rao",
    role="CAPTAIN",
    aircraft_type_rating="A320",
    total_flying_hours_this_month=72.0,
    last_duty_end_hour=16.0
)

sector = FlightSector(
    flight_number="IX-342",
    origin="BOM",
    destination="DXB",
    scheduled_departure_hour=8.0,
    block_hours=3.5,
    aircraft_type="A320"
)

audit = engine.audit_sector_assignment(pilot, sector)
print(f"Roster Compliant: {audit.is_compliant} | Remaining Legal Hours: {audit.remaining_legal_flying_hours}")
```

---

## 🧪 Testing

```bash
pytest tests/
```

---

## 📄 License
MIT License. Created with ❤️ by [Shyam Pandey](https://github.com/shyampandey1104).
