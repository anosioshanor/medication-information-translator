import json
import requests
from typing import Dict, Any, Optional

from utils import validate_medication_name, format_drug_info


class FDAClient:
    """
    Client for interacting with the openFDA Drug Label API.

    Responsibilities:
    - Validate medication names.
    - Retrieve medication information.
    - Format API responses.
    """

    BASE_URL = "https://api.fda.gov/drug/label.json"

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": "MedicationInformationTranslator/1.0"
        })

    def fetch_drug_info(self, drug_name: str) -> Dict[str, Any]:
        """
        Fetch medication information from the openFDA API.

        Args:
            drug_name (str): Name of the medication.

        Returns:
            dict:
                {
                    "drug_name": str,
                    "raw": dict,
                    "extracted": dict
                }

        Raises:
            ValueError
            ConnectionError
            LookupError
            Exception
        """

        if not validate_medication_name(drug_name):
            raise ValueError(
                f"Invalid medication name: '{drug_name}'."
            )

        query = (
            f'openfda.brand_name:"{drug_name}" '
            f'OR openfda.generic_name:"{drug_name}"'
        )

        params = {
            "search": query,
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

        except requests.exceptions.Timeout:
            raise ConnectionError(
                "Request timed out."
            )

        except requests.exceptions.ConnectionError:
            raise ConnectionError(
                "Could not connect to the openFDA API."
            )

        except requests.exceptions.HTTPError as e:
            raise Exception(
                f"HTTP Error: {e}"
            )

        except json.JSONDecodeError:
            raise Exception(
                "Invalid JSON received from the API."
            )

        if not data.get("results"):
            raise LookupError(
                f"No information found for '{drug_name}'."
            )

        extracted_info = format_drug_info(data)

        return {
            "drug_name": drug_name,
            "raw": data,
            "extracted": extracted_info
        }

    def fetch_warnings_only(
        self,
        drug_name: str
    ) -> Optional[str]:
        """
        Return only the warnings section
        for a medication.
        """

        try:
            result = self.fetch_drug_info(drug_name)
            return result["extracted"].get("warnings", "")

        except Exception:
            return None


# ----------------------------------------------------
# Test this module independently
# ----------------------------------------------------

if __name__ == "__main__":

    client = FDAClient()

    drug = input("Enter medication name: ")

    try:

        result = client.fetch_drug_info(drug)

        print("\nMedication Information\n")

        print(f"Drug: {result['drug_name']}")
        print("-" * 50)

        print("\nUsage:\n")
        print(result["extracted"]["usage"])

        print("\nWarnings:\n")
        print(result["extracted"]["warnings"])

        print("\nSide Effects:\n")
        print(result["extracted"]["side_effects"])

        print("\nInstructions:\n")
        print(result["extracted"]["instructions"])

    except Exception as e:
        print("\nError:", e)