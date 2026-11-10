import unittest
from aviation.engine import FlightCrewRosteringEngine, CrewMember, FlightSector


class TestFlightCrewRostering(unittest.TestCase):
    def setUp(self):
        self.engine = FlightCrewRosteringEngine()

    def test_compliant_assignment(self):
        crew = CrewMember(
            crew_id="CREW-007",
            full_name="Capt. Rajesh Malhotra",
            role="CAPTAIN",
            aircraft_type_rating="A320",
            total_flying_hours_this_month=65.0,
            last_duty_end_hour=14.0  # Ended at 14:00 yesterday
        )
        # Next flight 06:30 morning next day -> 16.5 hours rest
        sector = FlightSector(
            flight_number="6E-204",
            origin="DEL",
            destination="BLR",
            scheduled_departure_hour=6.5,
            block_hours=2.75,
            aircraft_type="A320"
        )
        audit = self.engine.audit_sector_assignment(crew, sector)
        self.assertTrue(audit.is_compliant)
        self.assertEqual(len(audit.violations), 0)
        self.assertEqual(audit.remaining_legal_flying_hours, 32.2)

    def test_rest_and_type_rating_violations(self):
        crew = CrewMember(
            crew_id="CREW-008",
            full_name="FO Ananya Sen",
            role="FIRST_OFFICER",
            aircraft_type_rating="B737",
            total_flying_hours_this_month=98.0,
            last_duty_end_hour=23.0  # Ended at 23:00
        )
        # Sector departs at 05:00 (only 6 hours rest) on A320
        sector = FlightSector(
            flight_number="AI-101",
            origin="BOM",
            destination="HYD",
            scheduled_departure_hour=5.0,
            block_hours=3.0,
            aircraft_type="A320"
        )
        audit = self.engine.audit_sector_assignment(crew, sector)
        self.assertFalse(audit.is_compliant)
        self.assertGreaterEqual(len(audit.violations), 2)  # Rating mismatch & Insufficient rest


if __name__ == "__main__":
    unittest.main()
