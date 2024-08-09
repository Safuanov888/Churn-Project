from django.shortcuts import render
import joblib
from django.templatetags.static import static


def check_perhap(data):
    if ',' in data:
        return float(data.replace(',', '.'))
    else:
        return float(data)


def create_answer(pred):
    if pred[0] == 1:
        return 'Модель предсказала, что клиент уйдёт в отток'
    else:
        return 'Модель предсказала, что клиент не уйдёт в отток'


def get_number(x):
    if x == '1':
        return 1
    else:
        return 0


def get_model(model_name):
    if model_name == 'Логистическая регрессия':
        return [joblib.load('LogisticRegression.joblib'), static('images/LogisticRegression_1.png'),
                static('images/LogisticRegression_2.png'), static('images/LogisticRegression_3.png')]
    elif model_name == 'Случайный лес':
        return [joblib.load('RandomForest.joblib'), static('images/RandomForest_1.png'),
                static('images/RandomForest_2.png'), static('images/RandomForest_3.png')]
    else:
        return [joblib.load('AdaBoosting.joblib'), static('images/AdaBoosting_1.png'),
                static('images/AdaBoosting_2.png'), static('images/AdaBoosting_3.png')]


def home(request):
    return render(request, 'home.html')


def info(request):
    return render(request, 'info.html')


def result(request):
    model_name = request.GET['Модель']
    model, image_1, image_2, image_3 = get_model(model_name)  # Загрузка модели и графиков обучения

    tenure = int(request.GET['Длительность контракта (месяцы)'])
    buy_month = check_perhap(request.GET['Ежемесячные траты на пользование интернетом'])
    buy_total = check_perhap(request.GET['Общие траты за весь период пользования интернетом'])
    scaler = joblib.load('scaler.save')
    transformed_data = scaler.transform(
        [[tenure, buy_month, buy_total]])  # Преобразование численных переменных с помощью scaler

    data = [0] * 33  # Количество признаков в массиве для предсказания
    data[0] = transformed_data[0][0]
    data[1] = transformed_data[0][1]
    data[2] = transformed_data[0][2]
    data[3] = get_number(request.GET['Гендер человека'])
    data[4] = get_number(request.GET['Пенсионер'])
    data[5] = get_number(request.GET['Женат/замужем'])
    data[6] = get_number(request.GET['Есть дети'])
    data[7] = get_number(request.GET['Подписка на домашний телефон компании'])
    data[8] = 1 if request.GET['Подписка на несколько телефонных линий компании'] == '2' else 0
    data[9] = 1 if request.GET['Подписка на несколько телефонных линий компании'] == '1' else 0
    data[10] = 1 if request.GET['Интернет услуга компании'] == '3' else 0
    data[11] = 1 if request.GET['Интернет услуга компании'] == '1' else 0
    data[12] = 1 if request.GET['Подписка на онлайн безопасность'] == '2' else 0
    data[13] = 1 if request.GET['Подписка на онлайн безопасность'] == '1' else 0
    data[14] = 1 if request.GET['Подписка на резервное копирование'] == '2' else 0
    data[15] = 1 if request.GET['Подписка на резервное копирование'] == '1' else 0
    data[16] = 1 if request.GET['Подписка на дополнительную онлайн безопасность'] == '2' else 0
    data[17] = 1 if request.GET['Подписка на дополнительную онлайн безопасность'] == '1' else 0
    data[18] = 1 if request.GET['Подписка на техническую поддержку'] == '2' else 0
    data[19] = 1 if request.GET['Подписка на техническую поддержку'] == '1' else 0
    data[20] = 1 if request.GET['Подписка на потоковую передачу телевезионных программ'] == '2' else 0
    data[21] = 1 if request.GET['Подписка на потоковую передачу телевезионных программ'] == '1' else 0
    data[22] = 1 if request.GET['Подписка на трансляцию фильмов'] == '2' else 0
    data[23] = 1 if request.GET['Подписка на трансляцию фильмов'] == '1' else 0
    data[24] = 1 if request.GET['Тип контракта'] == '2' else 0
    data[25] = 1 if request.GET['Тип контракта'] == '3' else 0
    data[26] = get_number(request.GET['Подписка на онлайн оплату'])
    data[27] = 1 if request.GET['Способ оплаты интернета'] == '4' else 0
    data[28] = 1 if request.GET['Способ оплаты интернета'] == '1' else 0
    data[29] = 1 if request.GET['Способ оплаты интернета'] == '2' else 0
    data[30] = 1 if 12 < tenure <= 24 else 0
    data[31] = 1 if 24 < tenure <= 48 else 0
    data[32] = 1 if tenure > 48 else 0

    ans = create_answer(model.predict([data]))

    return render(request, 'result.html',
                  {'ans': ans, 'model_name': model_name, 'image_1': image_1, 'image_2': image_2, 'image_3': image_3})
