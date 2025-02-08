import json
import os
import traceback
from selenium.webdriver.common.by import By

from selenium.common.exceptions import NoSuchElementException
from config.selectors import KiwiSelectors






import json
import os
import traceback

def save_flight_data(flight_data, output_file="json_data/flight_results.json"):
    """
    Saves structured flight data into a JSON file immediately after extraction.
    Ensures that all flights are appended to the existing JSON file in real-time.
    """
    try:
        # ✅ Ensure the directory exists before writing the file
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        # ✅ Validate flight_data before saving
        if not flight_data or not isinstance(flight_data, dict) or "flights" not in flight_data:
            print("[ERROR] Invalid flight data format. Not saving empty or incorrect data.")
            return

        # ✅ Check if the JSON file exists and has valid data
        if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
            try:
                with open(output_file, "r", encoding="utf-8") as file:
                    existing_data = json.load(file)
            except json.JSONDecodeError:
                print("[WARNING] Corrupted JSON file. Resetting data.")
                existing_data = {"flights": []}
        else:
            existing_data = {"flights": []}

        # ✅ Append new flight data immediately after extraction
        existing_data["flights"].append(flight_data)

        # ✅ Save JSON data **IMMEDIATELY AFTER EACH SCRAPE**
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(existing_data, file, indent=4)

        print(f"[SUCCESS] Flight data saved to {output_file}")

    except Exception as e:
        print(f"[ERROR] Failed to save flight data: {traceback.format_exc()}")



from selenium.common.exceptions import NoSuchElementException
from config.selectors import KiwiSelectors

from selenium.common.exceptions import NoSuchElementException
from config.selectors import KiwiSelectors
from selenium.webdriver.common.by import By
import json

def structure_flight_data(parents):
    """
    Organizes extracted flight data into a structured JSON format,
    ensuring stops are correctly assigned to departure and return flights.
    If a flight has only one box, it is marked as a direct flight (stops = 0)
    and retains all extracted flight details.
    """
    flight_data = {
        "flight_type": "round trip" if len(parents) > 1 else "one way",
        "flights": []
    }

    for parent_idx, parent in enumerate(parents[:2], start=1):  # Process only departure & return
        try:
            flight_label = "departure" if parent_idx == 1 else "return"

            departure_root = parent.find_element(By.XPATH, KiwiSelectors.DEPARTURE_ROOT).text.strip()
            arrival_root = parent.find_element(By.XPATH, KiwiSelectors.ARRIVAL_ROOT).text.strip()

            try:
                total_duration = parent.find_element(By.XPATH, KiwiSelectors.TOTAL_DURATION).text.strip()
            except NoSuchElementException:
                total_duration = "Not Available"

            # ✅ Fetch stops within this specific flight (departure or return)
            info_boxes = parent.find_elements(By.XPATH, ".//div[@class='pt-300' and @role='button' and @tabindex='0']")
            num_stops = len(info_boxes)

            # ✅ If only one info_box, it's a direct flight (stops = 0)
            if num_stops == 1:
                direct_flight_details = {
                    "flight_label": flight_label,
                    "departure_root": departure_root,
                    "arrival_root": arrival_root,
                    "total_duration": total_duration,
                    "stops": [],  # No stops
                    "num_stops": 0,
                    "is_direct": True,
                    "flight_details": {
                        "seating_info": {}
                    }
                }

                # ✅ Extract Flight-Specific Details (Airline, Flight Number, Seating, etc.)
                for key, xpath in KiwiSelectors.FLIGHT_INFO_TEMPLATE.items():
                    try:
                        extracted_value = info_boxes[0].find_element(By.XPATH, xpath).get_attribute("innerText").strip()
                        if key in ["Seat Pitch", "Seat Width", "Seat Recline", "Audio & Video on Demand",
                                   "In-Seat Power", "Wi-Fi on Board"]:
                            direct_flight_details["flight_details"]["seating_info"][key.lower().replace(" ", "_")] = extracted_value if extracted_value else "N/A"
                        else:
                            direct_flight_details["flight_details"][key.lower().replace(" ", "_")] = extracted_value if extracted_value else "N/A"
                    except NoSuchElementException:
                        direct_flight_details["flight_details"][key.lower().replace(" ", "_")] = "N/A"

                # ✅ Extract Departure & Arrival Times
                for key, xpath in KiwiSelectors.TIME_SELECTORS.items():
                    try:
                        extracted_value = info_boxes[0].find_element(By.XPATH, xpath).text.strip()
                        if "Departure Time" in key:
                            direct_flight_details["departure_time"] = extracted_value
                        elif "Arrival Time" in key:
                            direct_flight_details["arrival_time"] = extracted_value
                    except NoSuchElementException:
                        pass

                flight_data["flights"].append(direct_flight_details)

            else:
                # ✅ Process multi-stop flights
                stops = []
                for box_idx, box in enumerate(info_boxes, start=1):
                    stop_data = {
                        "stop_number": box_idx,
                        "departure": {},
                        "arrival": {},
                        "flight_details": {
                            "seating_info": {}
                        }
                    }

                    # ✅ Extract Flight-Specific Details
                    for key, xpath in KiwiSelectors.FLIGHT_INFO_TEMPLATE.items():
                        try:
                            extracted_value = box.find_element(By.XPATH, xpath).get_attribute("innerText").strip()
                            if key in ["Seat Pitch", "Seat Width", "Seat Recline", "Audio & Video on Demand",
                                       "In-Seat Power", "Wi-Fi on Board"]:
                                stop_data["flight_details"]["seating_info"][key.lower().replace(" ", "_")] = extracted_value if extracted_value else "N/A"
                            else:
                                stop_data["flight_details"][key.lower().replace(" ", "_")] = extracted_value if extracted_value else "N/A"
                        except NoSuchElementException:
                            stop_data["flight_details"][key.lower().replace(" ", "_")] = "N/A"

                    # ✅ Extract Departure & Arrival Times
                    for key, xpath in KiwiSelectors.TIME_SELECTORS.items():
                        try:
                            extracted_value = box.find_element(By.XPATH, xpath).text.strip()
                            if "Departure" in key:
                                stop_data["departure"][key.split(" ")[-1].lower()] = extracted_value
                            elif "Arrival" in key:
                                stop_data["arrival"][key.split(" ")[-1].lower()] = extracted_value
                        except NoSuchElementException:
                            stop_data["departure" if "Departure" in key else "arrival"][
                                key.split(" ")[-1].lower()] = "Not Available"

                    stops.append(stop_data)

                flight_data["flights"].append({
                    "flight_label": flight_label,
                    "departure_root": departure_root,
                    "arrival_root": arrival_root,
                    "total_duration": total_duration,
                    "stops": stops,
                    "num_stops": num_stops,
                    "is_direct": False
                })

        except Exception as e:
            print(f"[ERROR] Could not extract flight details for parent {parent_idx}: {e}")

    # ✅ Print structured flight data after extraction
    print(json.dumps(flight_data, indent=4))

    return flight_data
