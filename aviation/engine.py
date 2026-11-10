"""Aviation Pilot & Cabin Crew Duty Rostering, DGCA FDTL Rest Period Compliance Engine."""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class CrewMember(BaseModel):
    crew_id: str
    full_name: str
    role: str  # CAPTAIN, FIRST_OFFICER, CABIN_LEAD, FLIGHT_ATTENDANT
    aircraft_type_rating: str  # A320, B737, B787
    total_flying_hours_this_month: float = 0.0
    last_duty_end_hour: Optional[float] = None  # in 24-hr scale for rest compliance


class FlightSector(BaseModel):
    flight_number: str  # e.g., "AI-805"
    origin: str         # "DEL"
    destination: str    # "BOM"
    scheduled_departure_hour: float  # e.g., 06.5 (06:30 AM)
    block_hours: float               # e.g., 2.25 hours flight time
    aircraft_type: str               # "A320"


class RosteringAuditResult(BaseModel):
    crew_id: str
    flight_number: str
    is_compliant: bool
    violations: List[str]
    remaining_legal_flying_hours: float


class FlightCrewRosteringEngine:
    """Audits pilot and cabin crew schedules against DGCA India FDTL limits."""

    # DGCA FDTL Limits:
    # Max monthly flying limit: 100 block hours per 28-day window
    # Mandatory minimum rest period before next flight duty: 12 consecutive hours
    MAX_MONTHLY_HOURS = 100.0
    MIN_REST_HOURS = 12.0

    def audit_sector_assignment(self, crew: CrewMember, sector: FlightSector) -> RosteringAuditResult:
        violations: List[str] = []

        # 1. Type Rating validation
        if crew.aircraft_type_rating != sector.aircraft_type:
            violations.append(
                f"Type rating mismatch: Crew is rated for {crew.aircraft_type_rating}, but flight requires {sector.aircraft_type}."
            )

        # 2. Monthly flight hours limit
        projected_monthly = crew.total_flying_hours_this_month + sector.block_hours
        if projected_monthly > self.MAX_MONTHLY_HOURS:
            exceeded = projected_monthly - self.MAX_MONTHLY_HOURS
            violations.append(
                f"DGCA FDTL Monthly limit breached: {projected_monthly:.1f} hrs exceeds 100-hr cap by {exceeded:.1f} hrs."
            )

        # 3. Mandatory Rest Period validation
        if crew.last_duty_end_hour is not None:
            rest_given = sector.scheduled_departure_hour - crew.last_duty_end_hour
            if rest_given < 0:
                rest_given += 24.0  # overnight rest rollover
            if rest_given < self.MIN_REST_HOURS:
                violations.append(
                    f"Insufficient rest: Only {rest_given:.1f} hours provided between duties (DGCA minimum: 12.0 hours)."
                )

        remaining_hours = max(0.0, self.MAX_MONTHLY_HOURS - projected_monthly)

        return RosteringAuditResult(
            crew_id=crew.crew_id,
            flight_number=sector.flight_number,
            is_compliant=len(violations) == 0,
            violations=violations,
            remaining_legal_flying_hours=round(remaining_hours, 1)
        )
