import os

from api import PetFriends
from settings import valid_email, valid_password
from settings import invalid_email, invalid_password

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Вася', animal_type='Кот',
                                     age='2'):
    """Проверяем что можно добавить питомца с корректными данными"""
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_api_Add_photo_of_pet(pet_photo="images/cat1.jpg"):
    """Проверяем возможность добавления фото питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)
        assert status == 200
        assert result['pet_photo'] == pet_photo



def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Барон", "Собака", "2", "images/dog.JPG")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Борька', animal_type='Кот', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_get_api_key_with_invalid_mail(email=invalid_email, password=valid_password):
    # Проверяем получение API c невалидной почтой
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    assert status == 403 #Ожидаем ошибку 403

def test_get_api_key_with_invalid_password(email=valid_email, password=invalid_password):
    # Проверяем получение API c невалидным паролем
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    assert status == 403 #Ожидаем ошибку 403

def test_add_pet_without_name(animal_type='Собака', age='2'):
    # Не указываем имя питомца
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name=None, animal_type=animal_type, age=age)
    assert status == 400
    assert 'name' in result
    # Имеется баг питомец добовляется без имени
def test_add_pet_name_symbols(name='%^$', animal_type='Собака', age='2'):
    # Указываем имя питомца символоми
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name=name, animal_type=animal_type, age=age)
    assert status == 400
    assert 'name' in result
    # Имеется баг питомец добовляется символоми  и это БАГ


def test_add_pet_age_str(name='Сеня', animal_type='Собака', age='два'):
    # указываем возраст строкой
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name=name, animal_type=animal_type, age=age)
    assert status == 400
    assert 'name' in result
    # Возраст принемается строкой  и это БАГ

def test_add_new_pet_with_negative_age(name='Барон', animal_type='Собака',
                                         age='-2'):
    """Проверяем что нельзя добавить питомца с отрицательным возрастом"""
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

     # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    assert result['name'] == name
    # Имеется баг
def test_get_api_key_for_valid_user_none_index(email=valid_email, password=valid_password):
    # код получения API ключа
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    # Если есть список ключей, но мы обращаемся к несуществующему индексу
    key = result['keys'][3]  # Допустим, у нас нет элемента с индексом 3

    assert status == 403 # Ожидаемый статус
    assert 'name' in result

def test_add_new_pet_with_none_type_data(name='123', animal_type='Собака',
                                     age='2'):
    """Проверяем что можно добавить питомца с неправильнып типом данных"""
    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    assert result['name'] == name
    # Баг, выходит статус 200 а не 400
def test_api_Add_document_pet(pet_photo="images/my Pets.txt"):
    """Проверяем возможность добавления постороннего документа вместо фото питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)
        assert status == 500 # статус соответствует ожидаемому

def test_add_pet_without_name_animal_type_age(name=' ',animal_type=' ', age=' '):
    # Не указываем имя питомца
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name=None, animal_type=None, age=None)
    assert status == 400
    assert 'name' in result
    # Имеется баг питомец добовляется c пустыми значениями и это БАГ
