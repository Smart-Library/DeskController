import time
from desk import DeskObserver
import desk_sensor_table
from services.api_service import ApiService


class Obs(DeskObserver):
    def __init__(self):
        return

    def desk_occupied_updated(self, sender, new_val):
        print("[Event Received]: Desk", sender.name, " Occupied:", new_val)
        ApiService.update_desk_occupied_status(sender.desk_id, new_val)


if __name__ == "__main__":

    # Load the Desk-Pin table
    desk_map = desk_sensor_table.DeskSensorTable()

    # Add observer to desk events (as a test)
    (pin, d) = desk_map.get_mapping_from_desk_id(1)
    d.add_observer(Obs())

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
