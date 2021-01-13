import random

from django.http.response import JsonResponse
# from rest_framework.parsers import JSONParser
from rest_framework import status

from .models import Ticket, Call, Secret, Result
from .serializers import TicketSerializer, CallSerializer, SecretSerializer, ResultSerializer
from rest_framework.decorators import api_view


@api_view(['DELETE'])
def deleteAll(request, game_id=1):
    Ticket.objects.all().delete()
    Call.objects.all().delete()
    Secret.objects.all().delete()
    Result.objects.get(game_id=game_id).delete()
    return JsonResponse({'message': 'wiped'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def initialise_game(request, game_id=1):
    tickets = Ticket.objects.all()
    ticket_amt = len(tickets)
    call_made = len(Call.objects.all()) != 0
    try:
        Result.objects.get(game_id=game_id)
    except:
        result_data = {
            'game_id': game_id,
            'winners': [['first 5', 'NONE'],
                        ['row 1', 'NONE'],
                        ['row 2', 'NONE'],
                        ['row 3', 'NONE'],
                        ['house 1', 'NONE'],
                        ['house 2', 'NONE'],
                        ['house 3', 'NONE'],
                        ['full house', 'NONE']]
        }
        result_serializer = ResultSerializer(data=result_data)
        if result_serializer.is_valid():
            result_serializer.save()
        else:
            return JsonResponse(result_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({"Registered": ticket_amt, "Started": call_made}, status=status.HTTP_200_OK)


@api_view(['PUT'])
def processClaim(request, ticket_state, key, game_id=1):
    # ticket_state is a binary string
    #   representing if a number is crossed out or not
    result = Result.objects.get(game_id=game_id)
    result_serializer = ResultSerializer(result)
    verdicts = result_serializer.data['winners']
    converter = {verdict[0]: index for index, verdict in enumerate(verdicts)}

    secret = Secret.objects.get(key=key)
    secret_serializer = SecretSerializer(secret)
    auth_id = secret_serializer.data['discord_id']

    ticket_obj = Ticket.objects.get(key=key)
    ticket_serializer = TicketSerializer(ticket_obj)
    ticket = ticket_serializer.data["grid"]

    calls_obj = Call.objects.all()
    calls_serializer = CallSerializer(calls_obj, many=True)
    calls = [call['value'] for call in calls_serializer.data]

    # first 5 check
    if verdicts[converter['first 5']][1] == 'NONE':
        nums = []
        for x in range(9):
            for y in range(3):
                if ticket[x][y] != 'X' and ticket_state[x + y * 9] == '1' and calls.count(int(ticket[x][y])) == 1:
                    nums.append(int(ticket[x][y]))
        if len(nums) >= 5:
            verdicts[converter['first 5']][1] = auth_id
            print(f'{auth_id} wins first five')
    # row checks
    for i in range(3):
        if verdicts[converter[f'row {i + 1}']][1] == 'NONE':
            win = True
            row_nums = []
            for x in range(9):
                if ticket[x][i] != 'X':
                    row_nums.append(int(ticket[x][i]))
                if ticket[x][i] != 'X' and ticket_state[x + i * 9] != '1':
                    win = False
                    break
            if win:
                if set(row_nums).issubset(set(calls)):
                    verdicts[converter[f'row {i + 1}']][1] = auth_id
                    print(f'{auth_id} wins row {i + 1}')
                    # win confirmed
    # house or 3x3 checks
    for i in range(3):
        if verdicts[converter[f'house {i+1}']][1] == 'NONE':
            win = True
            house_nums = []
            for x in range(3):
                for y in range(3):
                    if ticket[x + i * 3][y] != 'X':
                        house_nums.append(int(ticket[x + i * 3][y]))
                    if ticket[x + i * 3][y] != 'X' and ticket_state[x + i * 3 + y * 9] != '1':
                        win = False
                        break
            if win:
                if set(house_nums).issubset(set(calls)):
                    verdicts[converter[f'house {i+1}']][1] = auth_id
                    print(f'{auth_id} wins house {i + 1}')
                    # win confirmed
    # full house check
    if verdicts[converter['full house']][1] == 'NONE':
        nums = []
        win = True
        for x in range(9):
            for y in range(3):
                if ticket[x][y] != 'X':
                    nums.append(int(ticket[x][y]))
                if ticket[x][y] != 'X' and ticket_state[x + y * 9] != '1':
                    win = False
                    break
        if win:
            if set(nums).issubset(set(calls)):
                verdicts[converter['full house']][1] = auth_id
                print(f'{auth_id} wins full house')
                # win confirmed
    result_serializer = ResultSerializer(
        result, data={
            'game_id': result_serializer.data['game_id'],
            'winners': verdicts})
    if result_serializer.is_valid():
        result_serializer.save()
        return JsonResponse(verdicts, safe=False, status=status.HTTP_200_OK)
    return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)


@ api_view(['GET'])
def result_report(request, game_id=1):
    result = Result.objects.get(game_id=game_id)
    result_serializer = ResultSerializer(result)
    return JsonResponse(result_serializer.data, status=status.HTTP_200_OK)


@ api_view(['GET', 'POST'])
def ticket_list(request, key, discord=0):
    if request.method == 'POST':
        if discord == 0:
            return JsonResponse({'message': 'discord id incorrect'}, status=status.HTTP_400_BAD_REQUEST)
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

        ticket_data = {'key': key, 'grid':  grid}
        ticket_serializer = TicketSerializer(data=ticket_data)
        secret_data = {'key': key, 'discord_id': discord}
        secret_serializer = SecretSerializer(data=secret_data)
        if secret_serializer.is_valid():
            secret_serializer.save()
        else:
            return JsonResponse(secret_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if ticket_serializer.is_valid():
            ticket_serializer.save()
            return JsonResponse(ticket_serializer.data, status=status.HTTP_201_CREATED)
        secret = Secret.objects.get(key=key)
        secret.delete()
        return JsonResponse(ticket_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        ticket = Ticket.objects.get(key=key)
        ticket_serializer = TicketSerializer(ticket)
        return JsonResponse(ticket_serializer.data, status=status.HTTP_200_OK)


@ api_view(['GET', 'POST'])
def calls_list(request, num=-1):
    if request.method == 'GET':
        calls = Call.objects.all()
        if(calls == None):
            return JsonResponse([], safe=False)
        calls_serializer = CallSerializer(calls, many=True)
        return JsonResponse([call['value'] for call in calls_serializer.data], safe=False, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        if num == -1:
            return JsonResponse({'message': 'invalid call'}, status=status.HTTP_400_BAD_REQUEST)
        call_data = {'value': num}
        call_serializer = CallSerializer(data=call_data)
        if call_serializer.is_valid():
            call_serializer.save()
            return JsonResponse(call_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(call_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
