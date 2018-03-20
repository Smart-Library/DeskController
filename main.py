import time
from desk import DeskObserver
import desk_sensor_table
from services.api_service import ApiService
import requests.exceptions


class APIObserver(DeskObserver):
    def __init__(self):
        return

    def desk_occupied_updated(self, sender, new_val):
        print("[Event Received]: Desk", sender.name, " Occupied:", new_val)
        try:
            ApiService.update_desk_occupied_status(sender.desk_id, new_val)
        except requests.exceptions.ConnectionError as cE:
            # TODO: Handle API connection failure case
            print(f"Failed to connect to API Service. {cE}")


if __name__ == "__main__":

    # Load the Desk-Pin table
    desk_map = desk_sensor_table.DeskSensorTable()

    # Create API observer to update API service desk events (as a test)
    obs = APIObserver()
    desk_map.add_observer_to_all_desks(obs)

    # Run Infinite loop so that we can receive events for pin changes
    while True:
        try:
            desk_map.poll_desk_occupancy()

            # Sleep between sensor polling
            time.sleep(0.1)
        except KeyboardInterrupt as k:
            print("Keyboard Interrupt - Exiting")
            desk_map.cleanup()
            exit(0)
