from random import randint
from time import sleep
import brain
import game

import socket
import logging
from enum import Enum

logging.basicConfig(level=logging.DEBUG)


class Keys(Enum):
    UP = "w"
    DOWN =  "s"
    LEFT = "a"
    RIGHT = "d"

class Container(object):

    def __init__(self,name="amtestam",host="our_box",port=2048):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host,port))
        self.name = name
        self.score = 0


    def send_move(self, key):
        self.sendall(key)

    def sendall(self, str):
        logging.info('sending: "{0}"'.format(str))
        self.socket.sendall(str+'\n')

    def recv(self, length):
        logging.info('waiting to recv....')
        res = self.socket.recv(length)
        logging.info('recvd: "{0}"'.format(res))
        return res

    def recv_until(self, expected, seconds=0):
        logging.info('waiting to recv expected....')
        buffer = ''
        while expected not in buffer:
            sleep(seconds)
            res = self.socket.recv(1024)
            buffer+=res
            logging.debug(buffer.replace(']',''))
        logging.info('got expected..."{0}"'.format(buffer))
        return buffer

    def send_name(self):
        self.sendall(self.name)
        buffer = self.recv_until("Welcome, >>{name}<<".format(name=self.name))

    def get_game_board(self, seconds=0):
        import re
        response = self.recv_until("wasd q:",seconds=seconds)
        '''+------+------+------+------+
        |  0   |  0   |  0   |  0   |
        +------+------+------+------+
        |  0   |  0   |  0   |  0   |
        +------+------+------+------+
        |  2   |  0   |  0   |  2   |
        +------+------+------+------+
        |  0   |  0   |  0   |  0   |
        +------+------+------+------+
        wasd q:'''
        clean_control = re.compile(r'\x1b[^m]*m')

        # get score
        clean_lines = []
        for line in response.split('\n'):
            clean_lines.append(clean_control.sub('', line))

        score_matches = []
        score_prog = re.compile('Current score:\s*(?P<score>\d+)')
        for line in clean_lines:
            match = score_prog.match(line)
            if match is not None:
                score_matches.append(match)
        if len(score_matches) > 0:
            self.score = int(score_matches[-1].groupdict()['score'])
            logging.info('My score is %d' % self.score)
        else:
            logging.debug('Could not find score')
         

        lines = response.split('\n')
        wasd_num = None
        for i, line in enumerate(lines):
            if 'wasd q:' in line:
                wasd_num = i
                
        if len(lines) < 10:
            raise Exception('board parsing problem')
        board_lines = lines[wasd_num-9:wasd_num]
        numbers = []
        for bl in board_lines:
            if '+' in bl:
                continue
            clean_control = re.compile(r'\x1b[^m]*m')
            clean_bl = clean_control.sub('', bl)

            prog = re.compile('\|\s*(?P<a>\d+)\s*\|\s*(?P<b>\d+)\s*\|\s*(?P<c>\d+)\s*\|\s*(?P<d>\d+)\s*\|')
            try:
                match = prog.match(clean_bl)
                d = match.groupdict()
            except Exception as e:
                print 'board lines:'
                print '\n'.join([ x.replace('[','') for x in board_lines ])
                print '-----------'
                raise e
            numbers.append(int(d['a']))
            numbers.append(int(d['b']))
            numbers.append(int(d['c']))
            numbers.append(int(d['d']))
        t_board = []
        for n in numbers:
            if n == 0:
                t_board.append(None)
            else:
                t_board.append(n)
        self.board = t_board
        return self.board 

def get_connected(box):

    container = Container(host=box)
    container.recv_until("Please enter your name: ")
    logging.info("got to the name prompt")
    container.send_name()
    logging.info("sent name")
    return container

    

def move_up():
    container.send_keys(Keys.UP)

def move_down():
    container.send_keys(Keys.DOWN)

def move_left():
    container.send_keys(Keys.LEFT)

def move_right():
    container.send_keys(Keys.RIGHT)

def zero_board():
    global board
    board = [[None, None, None, None],
             [None, None, None, None],
             [None, None, None, None],
             [None, None, None, None]]

def update_board():
    global board
    sleep(0.1)
    tiles = container.find_elements_by_class_name('tile')
    tiledata = list(map(lambda x: x.get_attribute('class').split(), tiles))
    zero_board()
    for tile in tiledata:
        value = tile[1].split('-')[1]
        pos = tile[2].split('-')[-2:]
        board[int(pos[1]) - 1][int(pos[0]) - 1] = int(value)


def pick_move():
    global board
    g = game.Game(board)
    predictions = brain.predict_next_board(g)
    scores = []
    for p in predictions[1:]:
        print(p, len(p))
        score = brain.weight_boards(predictions[0], p)
        scores.append(score)
    return brain.choose(scores)



'''
while not retry.is_displayed():
    update_board()
    pick_move()()
'''

'''

sleep(2)
update_board()
for b in board:
    print(b)
sleep(2)
print("Score: ", drv.find_element_by_class_name('score-container').text.splitlines()[0])
print("Game Over")
'''
