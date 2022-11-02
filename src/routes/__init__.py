from .user import signup, login, logout, user_suspended, get_all_users, create_new_user, get_user_by_id, delete_user_by_id
from .planet import get_planets, get_planet_by_id, create_new_planet, delete_planet_by_id, delete_favorite_planet_by_id, put_planet_by_id, search_planet
from .vehicle import get_vehicles, get_vehicle_by_id, create_new_vehicle, delete_vehicle_by_id, delete_favorite_vehicle_by_id, put_vehicle_by_id, search_vehicle
from .person import get_people, get_people_by_id, create_new_person, delete_character_by_id, delete_favorite_character_by_id, put_people_by_id, search_people