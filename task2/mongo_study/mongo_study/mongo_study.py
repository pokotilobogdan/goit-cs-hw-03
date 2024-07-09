from pymongo import MongoClient
from pymongo.server_api import ServerApi
from colorama import Fore, Back


def fill_collection(collection):                    # Функція буде створювати колекцію з фіксованими даними
    delete(collection)
    
    collection.insert_many(
        [
            {
                "name": "barsik",
                "age": 3,
                "features": ["ходить в капці", "дає себе гладити", "рудий"],
            },
            {
                "name": "Lama",
                "age": 2,
                "features": ["ходить в лоток", "не дає себе гладити", "сірий"],
            },
            {
                "name": "Liza",
                "age": 4,
                "features": ["ходить в лоток", "дає себе гладити", "білий"],
            },
            {
                "name": "Boris",
                "age": 12,
                "features": ["ходить в лоток", "не дає себе гладити", "сірий"],
            },
            {
                "name": "Murzik",
                "age": 1,
                "features": ["ходить в лоток", "дає себе гладити", "чорний"],
            },
            {
                "name": "Dariy",
                "age": 3,
                "features": ["ходить в лоток", "не дає себе гладити", "сірий"],
            },
            {
                "name": "Tom",
                "features": ["ходить в лоток", "не дає себе гладити", "сірий"],
            },
        ]
        )


def show(collection, name: str=None):
    '''
    Функція показує інформацію по одному коту, якщо name не None
    Інакше - виводиться інформація про всіх котів у базі
    '''
    if name != None:
        cat = collection.find_one({'name': name}, {'_id': 0})
        if cat is None:
            print("В базі даних немає кота з таким іменем")
        else:
            pretty_print(cat)
    else:
        cats = collection.find({}, {'_id': 0})
        for cat in cats:
            pretty_print(cat)
    print()


def pretty_print(document: dict, tab_count=0):
    tab = '\t'
    for key, value in document.items():
        print(tab*tab_count + Fore.GREEN + str(key) + ':' + Fore.RESET)
        if isinstance(value, dict):
            pretty_print(value, tab_count+1)
        elif isinstance(value, list) or isinstance(value, tuple):
            for elem in value:
                print(tab*(tab_count+1) + str(elem))
        else:
            print(tab*(tab_count+1) + str(value))
    print(Fore.RED + '-'*30 + Fore.RESET)


def update_name(collection, old_name: str, new_name: str):
    cat = collection.find_one({'name': old_name})
    if cat is None:
        print("В базі даних немає кота з таким іменем")
    else:
        collection.update_one({"name": old_name}, {"$set": {"name": new_name}})


def add_feature(collection, name: str, *features):
    cat = collection.find_one({'name': name})
    if cat is None:
        print("В базі даних немає кота з таким іменем")
    else:
        collection.update_one({'name': name}, {'$addToSet': {'features': {'$each': features}}})


def delete(collection, name: str=None):
    '''
    Функція видаляє інформацію по одному коту, якщо name не None
    Інакше - видаляється інформація про всіх котів у базі
    '''
    if name != None:
        cat = collection.delete_one({'name': name})
        if cat is None:
            print("В базі даних немає кота з таким іменем")
        else:
            collection.delete_one({'name': name})
    else:
        cats = collection.find({})
        for cat in cats:
            delete(collection, cat['name'])


if __name__ == "__main__":

    client = MongoClient(
        "mongodb+srv://bohdanino:some-password12321@cluster0.oqbkibo.mongodb.net/test?retryWrites=true&w=majority&appName=Cluster0",
        server_api=ServerApi('1')
    )

    collection = client.test.cats
    
    # Refill the collection with the same data:
    fill_collection(collection)

    print(Fore.CYAN + "Виводимо інформацію про всіх котів у базі:\n" + Fore.RESET)
    show(collection)

    input(Back.BLUE + "Щоб піти далі - натисніть що завгодно." + Back.RESET + "\n")

    print(Fore.CYAN + "Шукаємо кота по імені" + Fore.YELLOW + " Liza" + Fore.CYAN + ":\n" + Fore.RESET)
    show(collection, 'Liza')
    
    input(Back.BLUE + "Щоб піти далі - натисніть що завгодно." + Back.RESET + "\n")

    print(Fore.CYAN + "Шукаємо кота по імені" + Fore.YELLOW + " Vladon" + Fore.CYAN + ":\n" + Fore.RESET)
    show(collection, "Vladon")
    
    input(Back.BLUE + "Щоб піти далі - натисніть що завгодно." + Back.RESET + "\n")
    
    print(Fore.CYAN + "Змінюємо ім'я кота" + Fore.YELLOW + " Lama" + Fore.CYAN + " на" + Fore.YELLOW + " Vladon" + Fore.CYAN + ". Перевіряємо:\n" + Fore.RESET)
    update_name(collection, 'Lama', 'Vladon')
    show(collection)
    
    input(Back.BLUE + "Щоб піти далі - натисніть що завгодно." + Back.RESET + "\n")
    
    print(Fore.CYAN + "Додаємо пару особливостей коту під іменем" + Fore.YELLOW + " Vladon" + Fore.CYAN + ":\n" + Fore.RESET)
    add_feature(collection, 'Vladon', 'солоденький', 'вусатий')
    show(collection, 'Vladon')
    
    input(Back.BLUE + "Щоб піти далі - натисніть що завгодно." + Back.RESET + "\n")
    
    print(Fore.CYAN + "Видалимо запис з котом по імені" + Fore.YELLOW + " Borys" + Fore.CYAN + ":\n" + Fore.RESET)
    delete(collection, 'Boris')
    show(collection)

    input(Back.BLUE + "Щоб піти далі - натисніть що завгодно." + Back.RESET + "\n")
    
    print(Fore.CYAN + "І тепер видалимо всі записи.\n" + Fore.RESET)
    delete(collection)
    print("База даних порожня.")
    show(collection)
    print()
    


