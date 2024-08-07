from django.shortcuts import render
import joblib

def home(request):
    return render(request, 'home.html')

def result(request):
    def get_number(x):
        if x == '1':
            return 1
        else:
            return 0

    model = joblib.load('AdaBoosting.joblib')
    scaler = joblib.load('scaler.save')
    data = [0] * 33
    gender = request.GET['Гендер человека']
    data[3] = get_number(gender)

    senior = request.GET['Пенсионер']
    data[4] = get_number(senior)

    married = request.GET['Женат/замужем']
    data[5] = get_number(married)

    children = request.GET['Есть дети']
    data[6] = get_number(children)

    tenure = int(request.GET['Длительность контракта (месяцы)'])

    dom_phone = request.GET['Подписка на домашний телефон компании']
    data[7] = get_number(dom_phone)

    couple_lines = request.GET['Подписка на несколько телефонных линий компании']
    if couple_lines == '1':
        data[9] = 1
    elif couple_lines == '2':
        data[8] = 1

    service = request.GET['Интернет услуга компании']
    if service == '1':
        data[11] = 1
    elif service == '3':
        data[10] = 1

    security = request.GET['Подписка на онлайн безопасность']
    if security == '1':
        data[13] = 1
    elif security == '2':
        data[12] = 1

    copy = request.GET['Подписка на резервное копирование']
    if copy == '1':
        data[15] = 1
    elif copy == '2':
        data[14] = 1

    ad_security = request.GET['Подписка на дополнительную онлайн безопасность']
    if ad_security == '1':
        data[17] = 1
    elif ad_security == '2':
        data[16] = 1

    tech_security = request.GET['Подписка на техническую поддержку']
    if tech_security == '1':
        data[19] = 1
    elif tech_security == '2':
        data[18] = 1

    flaw = request.GET['Подписка на потоковую передачу телевезионных программ']
    if flaw == '1':
        data[21] = 1
    elif flaw == '2':
        data[20] = 1

    translation = request.GET['Подписка на трансляцию фильмов']
    if translation == '1':
        data[23] = 1
    elif translation == '2':
        data[22] = 1

    contract = request.GET['Тип контракта']
    if contract == '2':
        data[24] = 1
    elif contract == '3':
        data[25] = 1

    paperless = request.GET['Подписка на онлайн оплату']
    data[26] = get_number(paperless)

    buy_type = request.GET['Способ оплаты интернета']
    if buy_type == '1':
        data[28] = 1
    elif buy_type == '2':
        data[29] = 1
    elif buy_type == '4':
        data[27] = 1

    buy_month = request.GET['Ежемесячные траты на пользование интернетом']
    if ',' in buy_month:
        buy_month = float(buy_month.replace(',', '.'))
    buy_total = request.GET['Общие траты за весь период пользования интернетом']
    if ',' in buy_total:
        buy_total = float(buy_total.replace(',', '.'))

    transform_data = scaler.transform([[tenure, buy_month, buy_total]])
    data[0] = transform_data[0][0]
    data[1] = transform_data[0][1]
    data[2] = transform_data[0][2]

    if 12 < tenure <= 24:
        data[30] = 1
    elif 24 < tenure <= 48:
        data[31] = 1
    elif tenure > 48:
        data[32] = 1

    ans = model.predict([data])


    return render(request, 'result.html', {'ans': ans[0]})