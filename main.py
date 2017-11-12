# Potential future CLI args for this script can be:
# start-service (starts service to communicate with cloud, watch pin status for sensors)
# register-device (registers a device with the cloud, store device info and pin into persistent storage)
# unregister-device (unregister a table)
# print-table (pretty print the table mapping sensor/desk info to pin number)

import desk
import desk_pin_table
import config_loader
import time


class Obs(desk.DeskObserver):
    def __init__(self):
        return

    def desk_occupied_changed(self, sender, new_val):
        print("[Event Received]: Desk", sender.get_name(), " Occupied:", new_val)


if __name__ == "__main__":
    # Load the program configuration
    print("Current Config:", config_loader.get_global_config().get_properties())

    # Add observer to desk events (as a test)
    d_m = desk_pin_table.DeskPinTable()
    d = d_m.get_desk_from_id(1)
    d.register_occupied_change_event(Obs())

    # Run Infinite loop so that we can receive events for pin changes
    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt as k:
            print("Exit")
            desk_pin_table.GPIO.cleanup()
            exit(0)



