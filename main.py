import socket
import math
import matplotlib.pyplot as plt
import pandas as pd


R = 4  # радиус колеса
L = 15  # расстояние между колесами
alfa = math.pi / 2  # угол 90 град
conn = socket.socket()


def main():
    conn.connect(("127.0.0.1", 10007))
    distance = 15  # расстояние между траекториями при объезде
    position = [0, 0]  # координаты робота
    orientation = ''  # направление робота

    while "S0" in connection(0, 0, 0):

        for j in range(2):
            angle = move_forward(distance)
            for i in range(int(angle[0] // 10)):
                if "S0" in connection(0, 0, 0):
                    connection(100, 100, 0)
                    if j == 0:
                        position[1] += coordinates(10)
                    if j == 1:
                        position[1] -= coordinates(10)
                else:
                    if j == 0:
                        orientation = 'x0y'
                    if j == 1:
                        orientation = 'x0-y'
                    break

            if "S0" in connection(0, 0, 0):
                connection(int(angle[0] % 10 * 10), int(angle[1] % 10 * 10), 0)
                if j == 0:
                    position[1] += coordinates(int(angle[0] % 10))
                if j == 1:
                    position[1] -= coordinates(int(angle[0] % 10))
                for i1 in range(int(turn(alfa)[0] // 10)):
                    connection(100, -100, 0)
                connection(87, -87, 0)
            else:
                if j == 0:
                    orientation = 'x0y'
                if j == 1:
                    orientation = 'x0-y'

            for i in range(int(angle[0] // 10)):
                if "S0" in connection(0, 0, 0):
                    connection(100, 100, 0)
                    if j == 0:
                        position[0] += coordinates(10)
                    if j == 1:
                        position[0] -= coordinates(10)
                else:
                    if j == 0:
                        orientation = 'xy0'
                    if j == 1:
                        orientation = '-xy0'
                    break

            if "S0" in connection(0, 0, 0):
                connection(int(angle[0] % 10 * 10), int(angle[1] % 10 * 10), 0)
                if j == 0:
                    position[0] += coordinates(int(angle[0] % 10))
                if j == 1:
                    position[0] -= coordinates(int(angle[0] % 10))
                for i1 in range(int(turn(alfa)[0] // 10)):
                    connection(100, -100, 0)
                connection(87, -87, 0)
            else:
                if j == 0:
                    orientation = 'xy0'
                if j == 1:
                    orientation = '-xy0'

            distance += 16

    while "M10" in connection(0, 0, 0):
        connection(0, 0, 100)

    print(position)

    while "M20" in connection(0, 0, 0):
        length_back = math.sqrt(abs(position[0]) ** 2 + (abs(position[1])) ** 2)
        angle_back = math.atan(abs(position[1]) / abs(position[0]))

        if orientation == 'x0-y':
            for i in range(int(turn(alfa)[0]*2 // 10)):
                connection(100, -100, 0)
            connection(74, -74, 0)

        if orientation == 'xy0':
            for i in range(int(turn(alfa)[0] // 10)):
                connection(-100, 100, 0)
            connection(-87, 87, 0)

        if orientation == '-xy0':
            for i in range(int(turn(alfa)[0] // 10)):
                connection(100, -100, 0)
            connection(87, -87, 0)

        if position[0] > 0 and position[1] > 0:
            angle_back += math.pi / 2
            for i in range(int(turn(angle_back)[0] // 10)):
                connection(-100, 100, 0)
            connection(-int((turn(angle_back)[0] % 10) * 10), int((turn(angle_back)[0] % 10) * 10), 0)

        if position[0] < 0 < position[1]:
            angle_back += math.pi / 2
            for i in range(int(turn(angle_back)[0] // 10)):
                connection(100, -100, 0)
            connection(int((turn(angle_back)[0] % 10) * 10), -int((turn(angle_back)[0] % 10) * 10), 0)

        if position[0] < 0 and position[1] < 0:
            angle_back = math.pi / 2 - angle_back
            for i in range(int(turn(angle_back)[0] // 10)):
                connection(100, -100, 0)
            connection(int((turn(angle_back)[0] % 10) * 10), -int((turn(angle_back)[0] % 10) * 10), 0)

        if position[0] > 0 > position[1]:
            angle_back = math.pi / 2 - angle_back
            for i in range(int(turn(angle_back)[0] // 10)):
                connection(-100, 100, 0)
            connection(-int((turn(angle_back)[0] % 10) * 10), int((turn(angle_back)[0] % 10) * 10), 0)

        for i in range(int(move_forward(length_back)[0] // 10)):
            connection(100, 100, 0)
        connection(int(move_forward(length_back)[0] % 10 * 10), int(move_forward(length_back)[0] % 10 * 10), 0)

    data = pd.read_csv(r'C:\Users\mixa7\Desktop\Моб. роб\сервер\Log\data1.csv', sep=';', names=range(9))
    plt.plot(data[1], data[0])
    plt.show()


def connection(m1, m2, m3):
    data = f'0xFF 0xFF L{m1} R{m2} D{m3} 0xEE'
    data = str.encode(data)
    conn.send(data)
    data = conn.recv(1024)
    data = bytes.decode(data)
    print(data)
    return data


def move_forward(distance):
    left = distance * 360 / (math.pi * R * 2)
    right = distance * 360 / (math.pi * R * 2)
    return left, right


def turn(angle):
    distance = L * angle / 2
    left = distance * 360 / (math.pi * R * 2)
    right = -distance * 360 / (math.pi * R * 2)
    return left, right


def coordinates(angle):
    coord = angle * 2 * math.pi * R / 360
    return coord


if __name__ == "__main__":
    main()
