import pyrebase
import random
from django.http.response import JsonResponse

config = {
    "apiKey": "AIzaSyDHL7uPqv0P0Y_WVxcID7_FJhx6c-IO0y4",
    "authDomain": "tambola-3402f.firebaseapp.com",
    "databaseURL": "https://tambola-3402f-default-rtdb.firebaseio.com",
    "storageBucket": "tambola-3402f.appspot.com",
    "serviceAccount": "ServiceAccountKey.json"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()


def start(request):
    tickets = db.child('test').child("tickets").get().val()
    if not tickets:
        ticket_amt = 0
    else:
        ticket_amt = len(tickets)
    call_made = True if (db.child('test').child(
        'calls').shallow().get().val()) else False
    if db.child("test").child("win-cons").get().each() == None:
        db.child("test").child("win-cons").set({
            'first 5': False,
            'row 1': False,
            'row 2': False,
            'row 3': False,
            'house 1': False,
            'house 2': False,
            'house 3': False,
            'full house': False
        })
    return JsonResponse({"Registered": ticket_amt, "Started": call_made})


def processClaim(request, ticket_state, key):
    # ticket_state is a binary string
    #   representing if a number is crossed out or not
    verdicts = {win_con.key(): win_con.val()
                for win_con in db.child("test").child("win-cons").get().each()}
    auth_id = db.child("test").child("secrets").child(key).get().val()
    ticket = [column.val() for column in db.child(
        "test").child("tickets").child(key).get().each()]
    calls = [int(call.val()) for call in db.child(
        'test').child('calls').get().each()]
    # first 5 check
    if not verdicts['first 5']:
        nums = []
        for x in range(9):
            for y in range(3):
                if ticket[x][y] != 'X' and ticket_state[x + y * 9] == '1' and calls.count(ticket[x][y]) == 1:
                    nums.append(ticket[x][y])
        if len(nums) >= 5:
            verdicts['first 5'] = auth_id
            print(f'{auth_id} wins first five')
    # row checks
    for i in range(3):
        if not verdicts[f'row {i + 1}']:
            win = True
            row_nums = []
            for x in range(9):
                if ticket[x][i] != 'X':
                    row_nums.append(ticket[x][i])
                if ticket[x][i] != 'X' and ticket_state[x + i * 9] != '1':
                    win = False
                    break
            if win:
                if set(row_nums).issubset(set(calls)):
                    verdicts[f'row {i + 1}'] = auth_id
                    print(f'{auth_id} wins row {i + 1}')
                    # win confirmed
    # house or 3x3 checks
    for i in range(3):
        if not verdicts[f'house {i+1}']:
            win = True
            house_nums = []
            for x in range(3):
                for y in range(3):
                    if ticket[x + i * 3][y] != 'X':
                        house_nums.append(ticket[x + i * 3][y])
                    if ticket[x + i * 3][y] != 'X' and ticket_state[x + i * 3 + y * 9] != '1':
                        win = False
                        break
            if win:
                if set(house_nums).issubset(set(calls)):
                    verdicts[f'house {i+1}'] = auth_id
                    print(f'{auth_id} wins house {i + 1}')
                    # win confirmed
    # full house check
    if not verdicts['full house']:
        nums = []
        win = True
        for x in range(9):
            for y in range(3):
                if ticket[x][y] != 'X':
                    nums.append(ticket[x][y])
                if ticket[x][y] != 'X' and ticket_state[x + y * 9] != '1':
                    win = False
                    break
        if win:
            if set(nums).issubset(set(calls)):
                verdicts['full house'] = auth_id
                print(f'{auth_id} wins full house')
                # win confirmed
    db.child("test").child("win-cons").set(verdicts)
    return JsonResponse(verdicts)


def finish(request):
    result = {win_con.key(): win_con.val()
              for win_con in db.child("test").child("win-cons").get().each()}

    # db.remove()
    return JsonResponse(result)


def generateTicket(request, key, discord):
    grid = []
    for i in range(9):
        column = []
        for j in range(3):
            rnd_num = random.randint(1, 9 + (i == 8)) + 10 * i
            while(column.count(rnd_num) > 0):
                rnd_num = random.randint(1, 9 + (i == 8)) + 10 * i
            column.append(rnd_num)
        column.sort()
        grid.append(column)

    for i in range(12):
        rnd_a = random.randint(0, 8)
        while(grid[rnd_a].count('X') == 2):
            rnd_a = random.randint(0, 8)
        rnd_y = random.randint(0, 2)
        while(grid[rnd_a][rnd_y] == 'X'):
            rnd_y = random.randint(0, 2)
        grid[rnd_a][rnd_y] = 'X'

    ticket = {'grid':  grid}
    db.child("test").child("tickets").child(key).set(grid)
    db.child("test").child("secrets").child(key).set(discord)
    return JsonResponse(ticket)


def getTicket(request, key):
    return JsonResponse({'grid': db.child("test").child("tickets").child(key).get().val()})


def listCalls(request):
    calls_temp = db.child("test").child("calls").get()
    if(calls_temp.each() == None):
        return JsonResponse([], safe=False)
    calls = [call.val() for call in calls_temp.each()]
    return JsonResponse(calls, safe=False)


def processNumCall(request, num):
    db.child("test").child("calls").push(num)
    return JsonResponse({"stuff": 20})
