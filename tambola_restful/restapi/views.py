from datetime import time
import random

from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse
from rest_framework import status

from .models import GameTickets, GameCalls, GameSecrets, Result
from .serializers import GameTicketsSerializer, GameCallsSerializer, GameSecretsSerializer, ResultSerializer
from rest_framework.decorators import api_view


@api_view(['DELETE'])
def delete(request, game_id):
    try:
        Result.objects.get(game_id=game_id).delete()
        GameTickets.objects.get(game_id=game_id).delete()
        GameSecrets.objects.get(game_id=game_id).delete()
        GameCalls.objects.get(game_id=game_id).delete()
    except:
        return JsonResponse({'message': 'incomplete wipe'}, status=status.HTTP_404_NOT_FOUND)
    return JsonResponse({'message': 'wiped'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def initialise_game(request, game_id):
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
    try:
        g_tickets = GameTickets.objects.get(game_id=game_id)
        g_tickets_serializer = GameTicketsSerializer(g_tickets)
        ticket_amt = len(g_tickets_serializer.data['tickets'])
    except:
        ticket_amt = 0
    try:
        GameCalls.objects.get(game_id=game_id)
        call_made = True
    except:
        call_made = False
    return JsonResponse({"Registered": ticket_amt, "Started": call_made}, status=status.HTTP_200_OK)


@api_view(['PUT'])
def processClaim(request, ticket_state, key, game_id):
    # ticket_state is a binary string
    #   representing if a number is crossed out or not
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
    result = Result.objects.get(game_id=game_id)
    result_serializer = ResultSerializer(result)
    verdicts = result_serializer.data['winners']
    converter = {verdict[0]: index for index, verdict in enumerate(verdicts)}

    g_secrets = GameSecrets.objects.get(game_id=game_id)
    g_secrets_serializer = GameSecretsSerializer(g_secrets)
    secrets = g_secrets_serializer.data['secrets']
    ticket_id = -1
    auth_id = -1
    for secret in secrets:
        if secret['key'] == key:
            auth_id = secret['discord_id']
            ticket_id = secret['ticket_id']
            break

    g_tickets = GameTickets.objects.get(game_id=game_id)
    g_tickets_serializer = GameTicketsSerializer(g_tickets)
    tickets = g_tickets_serializer.data['tickets']
    ticket = tickets[ticket_id]

    try:
        g_calls = GameCalls.objects.get(game_id=game_id)
        g_calls_serializer = GameCallsSerializer(g_calls)
        calls = g_calls_serializer.data['calls']
    except:
        calls = []

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
def result_report(request, game_id):
    try:
        result = Result.objects.get(game_id=game_id)
    except:
        return JsonResponse({'message': 'game_id not found'}, status=status.HTTP_404_NOT_FOUND)
    result_serializer = ResultSerializer(result)
    return JsonResponse(result_serializer.data, status=status.HTTP_200_OK)


@ api_view(['GET', 'POST'])
def ticket_list(request, game_id, key, discord=0):
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

        try:
            g_tickets = GameTickets.objects.get(game_id=game_id)
            g_tickets_serializer = GameTicketsSerializer(g_tickets)
            new_tickets = g_tickets_serializer.data['tickets']
            new_tickets.append(grid)
            g_tickets_serializer = GameTicketsSerializer(
                g_tickets, data={'game_id': game_id, 'tickets': new_tickets})
        except ObjectDoesNotExist:
            g_tickets_serializer = GameTicketsSerializer(
                data={'game_id': game_id, 'tickets': [grid]})
        if g_tickets_serializer.is_valid():
            g_tickets_serializer.save()
        else:
            return JsonResponse(g_tickets_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        secret = {'key': key, 'discord_id': discord, 'ticket_id': len(
            g_tickets_serializer.data['tickets']) - 1}
        try:
            g_secrets = GameSecrets.objects.get(game_id=game_id)
            g_secrets_serializer = GameSecretsSerializer(g_secrets)
            new_secrets = g_secrets_serializer.data['secrets']
            new_secrets.append(secret)
            g_secrets_serializer = GameSecretsSerializer(
                g_secrets, data={'game_id': game_id, 'secrets': new_secrets})
        except ObjectDoesNotExist:
            g_secrets_serializer = GameSecretsSerializer(
                data={'game_id': game_id, 'secrets': [secret]})
        if g_secrets_serializer.is_valid():
            g_secrets_serializer.save()
        else:
            return JsonResponse(g_secrets_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(secret, safe=False, status=status.HTTP_201_CREATED)
    elif request.method == 'GET':
        g_secrets = GameSecrets.objects.get(game_id=game_id)
        g_secrets_serializer = GameSecretsSerializer(g_secrets)
        secrets = g_secrets_serializer.data['secrets']
        ticket_id = -1
        for secret in secrets:
            if secret['key'] == key:
                ticket_id = secret['ticket_id']
                break
        if ticket_id == -1:
            return JsonResponse({'message': 'ticket not found'}, status=status.HTTP_404_NOT_FOUND)

        g_tickets = GameTickets.objects.get(game_id=game_id)
        g_tickets_serializer = GameTicketsSerializer(g_tickets)
        tickets = g_tickets_serializer.data['tickets']
        return JsonResponse({'grid': tickets[ticket_id]}, status=status.HTTP_200_OK)


@ api_view(['GET', 'POST'])
def calls_list(request, game_id, num=-1):
    if request.method == 'GET':
        try:
            g_calls = GameCalls.objects.get(game_id=game_id)
        except:
            return JsonResponse([], safe=False, status=status.HTTP_200_OK)
        g_calls_serializer = GameCallsSerializer(g_calls)
        calls = g_calls_serializer.data['calls']
        return JsonResponse(calls, safe=False, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        if num == -1:
            return JsonResponse({'message': 'invalid call'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            g_calls = GameCalls.objects.get(game_id=game_id)
            g_calls_serializer = GameCallsSerializer(g_calls)
            new_calls = g_calls_serializer.data['calls']
            new_calls.append(num)
            g_calls_serializer = GameCallsSerializer(
                g_calls, data={'game_id': game_id, 'calls': new_calls})
        except ObjectDoesNotExist:
            g_calls_serializer = GameCallsSerializer(
                data={'game_id': game_id, 'calls': [num]})
        if g_calls_serializer.is_valid():
            g_calls_serializer.save()
            return JsonResponse(g_calls_serializer.data['calls'], safe=False, status=status.HTTP_201_CREATED)
        return JsonResponse(g_calls_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
