import re
import json
import datetime
import pandas as pd
import os

# Load the data contract from JSON file
CONTRACT_PATH = os.path.join(os.path.dirname(__file__), "data_contract.json")
with open(CONTRACT_PATH, "r") as validation_contract:
    DATA_CONTRACT = json.load(validation_contract)

# Helper to map string type names from JSON to Python types
TYPE_MAP = {
    "string": str,
    "integer": int,
    "number": float
}

def dict_validation(dict_record, filename=None, line_number=None):
    valid = True
    failed_tests = []
    time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


    for key, rules in DATA_CONTRACT.items():
        value = dict_record.get(key)
        expected_type = TYPE_MAP.get(rules.get("type"))

        # Check for missing keys is a dict_record
        if key not in dict_record:
            error_msg = f"Missing key in record: {key}"
            failed_tests.append({"line_number": line_number, "time": time_stamp, "key": key, "error": error_msg, "dict": dict_record, "filename": filename})
            valid = False

        # Values that can not be None/empty checks
        mandatory_key_values = ["policy_id", "customer_id", "event_timestamp", "event_type", "policy_type"]

        if key in mandatory_key_values and value is None:
            error_msg = f"Mandatory field: Missing or empty value for {key}"
            failed_tests.append({"line_number": line_number, "time": time_stamp, "key": key, "error": error_msg, "dict": dict_record, "filename": filename})
            valid = False
            continue

        # Values that can be None/empty checks
        mandatory_events = ["purchase", "renewal"]
        non_mandatory_key_values = ["premium_amount", "coverage_amount", "region", "age_of_insured"]

        if key in non_mandatory_key_values and dict_record["event_type"] in mandatory_events:
            if value is None:
                error_msg = f"Purchase or Renewal Events: Missing or empty value for {key}"
                failed_tests.append({"line_number": line_number, "time": time_stamp, "key": key, "error": error_msg, "dict": dict_record, "filename": filename})
                valid = False
                continue

        # Type check (try casting if not correct type)
        if value is not None and type(value) != expected_type and key in mandatory_events:
            try:
                if expected_type == float:
                    value = float(value)
                elif expected_type == int:
                    value = int(value)
                else:
                    error_msg = f"Type mismatch for '{key}': expected {expected_type}, got {type(value)}"
                    failed_tests.append({"line_number": line_number, "time": time_stamp, "key": key, "error": error_msg, "dict": dict_record, "filename": filename})
                    valid = False
                    continue
            except Exception:
                error_msg = f"Type mismatch for '{key}': expected {expected_type}, got {type(value)}"
                failed_tests.append({"line_number": line_number, "time": time_stamp, "key": key, "error": error_msg, "dict": dict_record, "filename": filename})
                valid = False
                continue

        # Pattern check
        column_patterns = ["policy_id", "customer_id","region", "event_type", "event_timestamp"]
        if key in column_patterns:
            if not re.fullmatch(rules["pattern"], str(value)):
                error_msg = f"Value for '{key}' does not match pattern: {value}"
                failed_tests.append({"line_number": line_number, "time": time_stamp, "key": key, "error": error_msg, "dict": dict_record, "filename": filename})
                valid = False
                continue

        # JSON structure check for fields like policy_type
        if key == "policy_type" and dict_record["event_type"] == "purchase" and mandatory_key_values:

            try:
                val = json.loads(value.replace("'", '"'))

                for req in rules["required_keys"]:
                    required_key = req
                    required_value = val.get(required_key)

                    # Check if the required key exists
                    if required_key not in val:
                        error_msg = f"policy_type missing required key: {required_key}"
                        failed_tests.append({"line_number": line_number,"time": time_stamp,"key": key,"error": error_msg,"dict": dict_record,"filename": filename})
                        valid = False
                        continue

                    # Check if the required value is valid
                    if required_value is None:
                        error_msg = f"Mising or empty value within the policy_type for {required_key}"
                        failed_tests.append({"line_number": line_number,"time": time_stamp,"key": key,"error": error_msg,"dict": dict_record,"filename": filename})
                        valid = False
                        continue

                    # Only accept valid strings (not None, not empty, and type is str)
                    if required_value is not None:
                        if type(required_value) != str:
                            error_msg = f"Type mismatch for '{required_key}': expected string, got {type(required_value)}"
                            failed_tests.append({"line_number": line_number, "time": time_stamp, "key": key, "error": error_msg, "dict": dict_record, "filename": filename})
                            valid = False

                # Check if unexpected key in the json object
                for k in val.keys():
                        if k not in rules["required_keys"]:
                            error_msg = f"Unexpected key found in policy_type: {k}"
                            failed_tests.append({"line_number": line_number, "time": time_stamp, "key": key, "error": error_msg, "dict": dict_record, "filename": filename})
                            valid = False
                            continue

            except Exception:
                error_msg = f"policy_type is not valid JSON"
                failed_tests.append({"line_number": line_number, "time": time_stamp, "key": key, "error": error_msg, "dict": dict_record, "filename": filename})
                valid = False
                continue

            # check that premium_amount and coverage_amount are not < 0. Valid values

    # Check for unexpected keys
    for key in dict_record.keys():
        if key not in DATA_CONTRACT:
            error_msg = f"Unexpected key found: {key}"
            failed_tests.append({"line_number": line_number, "time": time_stamp, "key": key, "error": error_msg, "dict": dict_record, "filename": filename})
            valid = False

    return valid, failed_tests

