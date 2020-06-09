import socketserver
import socket


class Node:
    def __init__(self, initdata):
        self.data = initdata
        self.next = None
        self.prev = None        # викор. тільки в двозвязному списку

    def getData(self):
        return self.data

    def getNext(self):
        return self.next

    def getPrev(self):          # викор. тільки в двозвязному списку
        return self.prev        # викор. тільки в двозвязному списку

    def setPrev(self, newprev):  # викор. тільки в двозвязному списку
        self.prev = newprev     # викор. тільки в двозвязному списку

    def setData(self, newdata):
        self.data = newdata

    def setNext(self, newnext):
        self.next = newnext


class LoopList:
    def __init__(self):
        self._curr = None
        self._prev = None

    def gotonext(self):
        if self._curr is not None:
            self._prev = self._curr
            self._curr = self._curr.next
        else:
            return None

    def getCurrent(self):
        if self._curr is not None:
            return self._curr.getData()
        else:
            return None

    def insert(self, data):
        elem = Node(data)
        if self._curr is None:
            self._curr = elem
            self._curr.next = self._curr
            self._prev = None
        else:
            if self._prev is None:
                elem.setNext(self._curr.getNext())
                self._curr.setNext(elem)
                self._prev = elem
            else:
                elem.setNext(self._curr.getNext())
                self._curr.setNext(elem)

    def remove_current(self):
        if self._prev is not None:
            self._prev.setNext = self._curr.getNext
            self._curr = self._prev.getNext()
        else:
            self._curr = None

    def size(self):
        current = self._curr
        if current is not None:
            count = 1
            while current != self._prev:
                count += 1
                current = current.getNext()
        else:
            count = 0
        return count

    def search(self, data):
        found = False
        current = self._curr
        if self._prev.getData() != data:
            while current != self._prev and not found:
                if current.getData == data:
                    found = True
                else:
                    current = current.getNext()
        else:
            found = True
        return found


class ClientError(Exception):
    "Виключення у разі отримання неправильних даних від клієнта."
    pass


class NetPlayer():
    """Гравець у мережі """

    def __init__(self, name, wfile):
        # Player.__init__(self, name)
        self._name = name
        self.wfile = wfile
        # файлоподібний об'єкт для передачі даних у мережі
        # self.field = []

    def __str__(self):
        return '{} {}'.format(self._name, self._points)

    def getname(self):
        return '{}'.format(self._name)


class BattleServer(socketserver.ThreadingTCPServer):
    "Клас багатопоточного TCP-сервера."

    def __init__(self, server_address, RequestHandlerClass):
        socketserver.ThreadingTCPServer.__init__(self, server_address, RequestHandlerClass)
        # кільцевий список гравців)
        # типу NetGuesser
        self.plist = LoopList()
        # поточна кількість гравців
        self.num_players = 0
        self.num_placed_ships = 0
        self.num_to_start = 2  # кількість гравців для початку гри
        self.game_on = False        # чи йде гра


class RequestHandler(socketserver.StreamRequestHandler):
    """Клас обробляє запити одного клієнта"""

    def handle(self):
        """Обробляє з'єднання одного гравця та підтримує його участь у грі."""
        print('connected from', self.client_address)
        self.name = None    # ім'я гравця
        done = self.server.game_on  # done - чи завершено з'єднання
        if not done:
            name = self._readline()
            try:
                self.addPlayer(name)   # додати гравця
            except ClientError as error:
                print(error)
                self.privateMessage(error.args[0])
                done = True
            except socket.error as e:
                print(e)
                done = True

        # Вести гру
        while not done:
            try:
                done = self.processInput()  # обробити отримані дані
            except ClientError as error:
                self.privateMessage(str(error))
            except socket.error as e:
                done = True

    def startGame(self):
        """Починає гру."""
        self.server.game_on = True
        # повідомити про початок гри
        self.broadcast('The Battle is on!')
        # надати хід першому гравцю
        self.nextTurn()

    def nextTurn(self):
        """Надає гравцю хід."""
        player = self.server.plist.getCurrent()
        # повідомляє всіх про те, у кого хід
        self.broadcast('Хід {}'.format(player.getname()))
        # надсилає гравцю команду поточного ходу (TURN)
        player.wfile.write(bytes(self._ensureNewline(TURN), encoding='utf-8'))

    def addPlayer(self, name):
        """Додає нового гравця з ім'ям name."""
        self.name = name
        # вставити гравця у список
        self.server.plist.insert(NetPlayer(self.name, self.wfile))
        # повідомити про приєднання гравця
        self.broadcast('До гри прєднався(лась) {}'.format(self.name))

    def processInput(self):
        """Читає рядок тексту та обробляє отриману команду."""
        done = False
        line = self._readline()
        # отримати команду та аргументи
        command, arg = self._parseCommand(line)
        if command:
            # викликати метод для виконання команди
            done = command(arg)
        return done

    def privateMessage(self, message):
        """Надіслати повідомлення тільки поточному клієнту."""
        self.wfile.write(bytes(self._ensureNewline(message), encoding='utf-8'))

    def startCommand(self):
        '''Комманда /start'''
        self.num_placed_ships += 1
        if self.server.num_placed_ships == self.server.num_to_start:
            print('game started')
            self.startGame()

    def fireCommand(self, pos):
        '''Команда /fire'''
        # передаємо наступному гравцю інфу, куди в нього стріляли
        next_player = self.server.plist.gotonext()
        message = '/fire {}'.format(pos)
        next_player.wfile.write(bytes(self._ensureNewline(message), encoding='utf-8'))

    def hitCommand(self, arg):
        pos = arg[:2]
        arg = arg[2:]
        if arg == 'True':
            next_player = self.server.plist.gotonext()
            message = '/hit {}'.format(pos + arg)
            next_player.wfile.write(bytes(self._ensureNewline(message), encoding='utf-8'))
        else:
            message = '/turn'
            self.server.plist.getcurrent().wfile.write(bytes(self._ensureNewline(message), encoding='utf-8'))

    def _parseCommand(self, inp):
        """Намагається розібрати рядок як команду серверу.

           Якщо цю команду реалізовано, викликає відповідний метод.
        """
        commandMethod, arg = None, None
        # якщо рядок непорожній та починається з '/'
        if inp and inp[0] == '/':
            if len(inp) < 2:
                raise ClientError('Недопустима команда: "{}"'.format(inp))
            # список з 2 (або 1) значень: команда та її аргументи (якщо є)
            commandAndArg = inp[1:].split(' ', 1)
            if len(commandAndArg) == 2:  # є аргументи
                command, arg = commandAndArg
            else:
                command, = commandAndArg  # немає аргументів
            # Чи реалізовано у класі метод, який починається
            # ім'ям команди та завершується 'Command'
            commandMethod = getattr(self, command + 'Command', None)
            if not commandMethod:
                raise ClientError('Немає такої команди: "{}"'.format(command))
        return commandMethod, arg

    def _readline(self):
        """Читає з мережі рядок, видаляє пропуски з початку та кінця."""
        line = str(self.rfile.readline().strip(), encoding='utf-8')
#        print(line)
        return line

    def broadcast(self, message, includeThisUser=True):
        """Розіслати повідомлення message всім клієнтам.

           Повідомлення відпправляється всім приєднаним клієнтам,
           окрім, можливо, поточного, що встановлюється параметром
           includeThisUser."""
        message = bytes(self._ensureNewline(message), encoding='utf-8')
        for i in range(self.server.plist.size()):
            player = self.server.plist.getCurrent()
            self.server.plist.gotonext()
            if includeThisUser or player.getname() != self.name:
                player.wfile.write(message)

    def _ensureNewline(self, s):
        """Запевняє, що рядок завершується символом '\n'."""
        if s and s[-1] != '\n':
            s += '\n'
        return s


HOST = ''        # Комп'ютер для з'єднання
PORT = 30003            # Порт для з'єднання
TURN = '/turn'   # команда "зробити хід"
QUIT = '/quit'   # команда "завершити"

if __name__ == '__main__':
    print('=== Battleships server ===')
    # запустити сервер
    BattleServer((HOST, PORT), RequestHandler).serve_forever()
