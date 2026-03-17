from dataclasses import dataclass, field
from enum import IntEnum
import numpy as np


class EscalationLevel(IntEnum):
    STABLE = 0
    POLITICAL_TENSION = 1
    DIPLOMATIC_CONFLICT = 2
    MILITARY_POSTURING = 3
    LIMITED_CONFLICT = 4
    FULL_ESCALATION = 5


STATE_NAMES = {
    EscalationLevel.STABLE: "Stable",
    EscalationLevel.POLITICAL_TENSION: "Political Tension",
    EscalationLevel.DIPLOMATIC_CONFLICT: "Diplomatic Conflict",
    EscalationLevel.MILITARY_POSTURING: "Military Posturing",
    EscalationLevel.LIMITED_CONFLICT: "Limited Conflict",
    EscalationLevel.FULL_ESCALATION: "Full Escalation",
}


BASE_TRANSITION_MATRIX = {
    EscalationLevel.STABLE: {
        EscalationLevel.STABLE: 0.70,
        EscalationLevel.POLITICAL_TENSION: 0.25,
        EscalationLevel.DIPLOMATIC_CONFLICT: 0.05,
    },
    EscalationLevel.POLITICAL_TENSION: {
        EscalationLevel.STABLE: 0.20,
        EscalationLevel.POLITICAL_TENSION: 0.50,
        EscalationLevel.DIPLOMATIC_CONFLICT: 0.30,
    },
    EscalationLevel.DIPLOMATIC_CONFLICT: {
        EscalationLevel.POLITICAL_TENSION: 0.30,
        EscalationLevel.DIPLOMATIC_CONFLICT: 0.30,
        EscalationLevel.MILITARY_POSTURING: 0.40,
    },
    EscalationLevel.MILITARY_POSTURING: {
        EscalationLevel.DIPLOMATIC_CONFLICT: 0.25,
        EscalationLevel.MILITARY_POSTURING: 0.35,
        EscalationLevel.LIMITED_CONFLICT: 0.40,
    },
    EscalationLevel.LIMITED_CONFLICT: {
        EscalationLevel.MILITARY_POSTURING: 0.20,
        EscalationLevel.LIMITED_CONFLICT: 0.45,
        EscalationLevel.FULL_ESCALATION: 0.35,
    },
    EscalationLevel.FULL_ESCALATION: {
        EscalationLevel.FULL_ESCALATION: 0.60,
        EscalationLevel.LIMITED_CONFLICT: 0.40,
    },
}


@dataclass
class CrisisState:
    current_level: EscalationLevel
    turn: int = 0
    history: list = field(default_factory=list)

    def record(self):
        self.history.append(self.current_level)