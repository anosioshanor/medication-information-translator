class Medication:
    def __init__(
        self,
        name,
        uses,
        warnings,
        side_effects,
        dosage,
        recall_status="Unknown",
        recall_reason=None
    ):
        self.name = name
        self.uses = uses
        self.warnings = warnings
        self.side_effects = side_effects
        self.dosage = dosage
        self.recall_status = recall_status
        self.recall_reason = recall_reason

    def get_medication_info(self):
        return {
            "name": self.name,
            "uses": self.uses,
            "warnings": self.warnings,
            "side_effects": self.side_effects,
            "dosage": self.dosage,
            "recall_status": self.recall_status,
            "recall_reason": self.recall_reason
        }

    def get_summary(self):
        return f"{self.name} is used for {self.uses}."

    def get_warnings(self):
        return self.warnings

    def get_side_effects(self):
        return self.side_effects

    def get_dosage(self):
        return self.dosage

    def get_recall_status(self):
        return self.recall_status

    def get_recall_reason(self):
        return self.recall_reason


# Test
if __name__ == "__main__":
    medication = Medication(
        "Paracetamol",
        "Relieves pain and reduces fever",
        "Do not exceed the recommended dosage",
        "Nausea and allergic reactions",
        "Follow the recommended dosage instructions",
        "Not Recalled",
        None
    )

    print(medication.get_medication_info())
    print(medication.get_recall_status())
