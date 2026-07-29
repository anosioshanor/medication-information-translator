import json
import requests
from typing import Dict, Any, Optional

from services.utils import validate_medication_name


class RecallChecker:
    """
    Client for interacting with the openFDA Drug Enforcement API.

    Responsibilities:
    - Validate medication names.
    - Check whether a medication has been recalled.
    - Return recall details.
    """

    BASE_URL = "https://api.fda.gov/drug/enforcement.json"

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": "MedicationInformationTranslator/1.0"
        })

    def check_recall(self, medication_name: str) -> Dict[str, Any]:
        """
        Checks if a medication has any recall records.

        Args:
            medication_name (str): Name of the medication to check.

        Returns:
            Dict[str, Any]: Recall information.
        """

        if not validate_medication_name(medication_name):
            raise ValueError(
                f"Invalid medication name: '{medication_name}'."
            )

        params = {
            "search": f'openfda.brand_name:"{medication_name}"',
            "limit": 1
        }

        try:
            response = self.session.get(
                self.BASE_URL,
                params=params,
                timeout=self.timeout
            )

            response.raise_for_status()

            data = response.json()

            if "results" not in data:
                return {
                    "recalled": False,
                    "message": "No recall found for this medication."
                }

            recall = data["results"][0]

            return {
                "recalled": True,
                "reason": recall.get("reason_for_recall", "No reason provided"),
                "company": recall.get("recalling_firm", "Unknown company"),
                "date": recall.get("report_date", "Unknown date"),
                "product": recall.get(
                    "product_description",
                    "No product description available"
                )
            }

        except requests.exceptions.Timeout:
            return {
                "recalled": False,
                "message": "The request timed out. Please try again."
            }

        except requests.exceptions.RequestException as e:
            return {
                "recalled": False,
                "message": f"An API error occurred: {str(e)}"
            }

        except Exception as e:
            return {
                "recalled": False,
                "message": f"An unexpected error occurred: {str(e)}"
            }


if __name__ == "__main__":
    print("✅ Program started!")

    checker = RecallChecker()

    print("✅ RecallChecker object created!")

    drug = input("Enter medication name: ")

    try:
        result = checker.check_recall(drug)

        print("\nRecall Check Result\n")
        print("-" * 50)

        if result["recalled"]:
            print("⚠️ Recall Found!")
            print(f"Reason: {result['reason']}")
            print(f"Company: {result['company']}")
            print(f"Date: {result['date']}")
            print(f"Product: {result['product']}")
        else:
            print(result["message"])

    except Exception as e:
        print("\nError:", e)