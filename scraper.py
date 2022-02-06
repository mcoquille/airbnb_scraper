from lib import scraping, airbnb
import pickle

# Initiate driver
driver = scraping.get_driver()

# Get the list of room IDs we want to scrape
with open('room_ids.pickle', 'rb') as handle:
    room_ids = pickle.load(handle)

# Initiate the list of room IDs we won't be able to scrape
failed_room_ids = []

for room_id in room_ids:
    room = airbnb.scrape_room(driver, room_id)
    if room:
        # Add data in db
        pass
    else:
        failed_room_ids.append(room_id)

driver.quit()

print(f"We couldn't scrape rooms {failed_room_ids}")
