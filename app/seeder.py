import random
from datetime import datetime, timedelta
from database import supabase

def generate_random_song():
    title = f"Random Song {random.randint(1, 1000)}"  
    length = random.randint(120, 300)
    date_released = datetime.now() - timedelta(days=random.randint(0, 365 * 5))
    price = round(random.uniform(0.99, 9.99), 2)

    return {
        "title": title,
        "length": length,
        "date_released": date_released.isoformat(),
        "price": price
    }

def seed_songs(num_songs=10):
    try:
        for _ in range(num_songs):
            song = generate_random_song()
            print(f"Attempting to insert: {song}") 
            response = supabase.table("song").insert(song).execute()
            if not response.data[0]:
                print(f"Error inserting {song['title']}")
            else:
                print(f"Inserted: {response.data[0]['title']}")
    except Exception as e:
        print(f"An error occurred while inserting {song['title']}: {str(e)}")


if __name__ == "__main__":
    seed_songs()
