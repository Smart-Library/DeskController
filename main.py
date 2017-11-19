# Potential future CLI args for this script can be:
# start-service (starts service to communicate with cloud, watch pin status for sensors)
# register-device (registers a device with the cloud, store device info and pin into persistent storage)
# unregister-device (unregister a desk)
# print-table (pretty print the table mapping sensor/desk info to pin number)

import time
from desk import DeskObserver, Desk
import desk_pin_table


class Obs(DeskObserver):
    def __init__(self):
        return

    def desk_occupied_updated(self, sender, new_val):
        print("[Event Received]: Desk", sender.name, " Occupied:", new_val)


if __name__ == "__main__":

    # Load the Desk-Pin table
    desk_map = desk_pin_table.DeskPinTable()

    # Add observer to desk events (as a test)
    d: Desk = desk_map.get_mapping_from_desk_id(1)
    d.add_observer(Obs())

    # Run Infinite loop so that we can receive events for pin changes
    while True:
        try:
            # Basically keep the main thread asleep,
            # as everything is run on a separate thread due to pin event detection
            time.sleep(500)
        except KeyboardInterrupt as k:
            print("Keyboard Interrupt - Exiting")
            desk_pin_table.GPIO.cleanup()
            exit(0)
