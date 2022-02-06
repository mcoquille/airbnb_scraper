from lib import scraping, airbnb

# Initiate driver
driver = scraping.get_driver()

# Get the list of room IDs we want to scrape
with open('room_ids.txt', 'r') as f:
    room_ids = [line.strip() for line in f]

# Initiate the list of room IDs we won't be able to scrape
failed_room_ids = []

for room_id in room_ids:
    room = airbnb.scrape_room(driver, room_id)
    if room:
        # Add data in db
        print(f"Successfully processed {room_id}")
        pass
    else:
        failed_room_ids.append(room_id)

driver.quit()

print(f"We couldn't scrape rooms {failed_room_ids}")
