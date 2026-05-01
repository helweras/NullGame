import random
import sys

table_win = [
[3, 6],
[5, 4]
]
table_win_br = [
[[3, -3], [6, -6]],
[[5, -5], [4, -4]]
]

import random


def transponir(matrix):
	"""
    Выполняет транспонирование матрицы.

    Меняет строки и столбцы местами. Использует zip для эффективной распаковки.

    Args:
        matrix (list of list): Исходная матрица (список списков).

    Returns:
        list of list: Новая транспонированная матрица.
    """
	return [list(row) for row in zip(*matrix)]


def shuffle_strategy(strategy_s):
	"""
    Моделирует случайный выбор хода для игры 2x2.

    Используется для бинарных стратегий, где передаются вероятности выбора
    первого варианта для каждого игрока.

    Args:
        strategy_s (tuple): Пара вероятностей (prob_blue, prob_red) от 0 до 1.

    Returns:
        tuple: (bs_c, rs_c) - индексы выбранных стратегий (0 или 1).
    """
	bs_prob, rs_prob = strategy_s
	# Сравниваем случайное число с порогом вероятности
	bs_c = 0 if random.random() < bs_prob else 1
	rs_c = 0 if random.random() < rs_prob else 1
	return bs_c, rs_c


def gen_strategy_list(freq_list):
	"""
    Генерирует расширенный список индексов стратегий на основе их частот.

    Умножает частоту на 100 для создания пропорционального набора данных.
    Удобно для последующего использования с random.choice().

    Args:
        freq_list (list): Список частот/весов стратегий.

    Returns:
        list: Список индексов [0, 0...1, 1...], где количество повторов
              зависит от веса в freq_list.
    """
	s = 0
	strategy_list = []
	for freq in freq_list:
		# Добавляем индекс 's' в список freq * 100 раз
		strategy_list += [s] * (freq * 100)
		s += 1
	return strategy_list


def shuffle_strategy_dev(freq_list):
	"""
    Выбирает случайную стратегию для любого количества вариантов.

    В отличие от shuffle_strategy, работает с произвольным числом стратегий,
    используя взвешенный выбор random.choices.

    Args:
        freq_list (tuple): Кортеж из двух списков частот (bs_freq, rs_freq).

    Returns:
        tuple: (bs_c, rs_c) - выбранные индексы стратегий для обоих игроков.
    """
	bs_freq, rs_freq = freq_list

	# weights позволяет задать вероятность выбора каждого элемента из диапазона
	bs_c = random.choices(range(len(bs_freq)), weights=bs_freq, k=1)[0]
	rs_c = random.choices(range(len(rs_freq)), weights=rs_freq, k=1)[0]

	return bs_c, rs_c


def theory_game(table, strategy):
	"""
    Вычисляет теоретическое математическое ожидание выигрыша в игре 2x2.

    Рассчитывает ожидаемый результат для "синего" игрока на основе
    матрицы платежей и заданных смешанных стратегий.

    Args:
        table (list of list): Матрица платежей 2x2.
        strategy (tuple): Вероятности (bs, rs) выбора первых стратегий.

    Returns:
        float: Ожидаемый выигрыш, округленный до 2 знаков после запятой.
    """
	bs, rs = strategy

	# rc1 и rc2 - мат. ожидание выигрыша при выборе синим игроком 1-й или 2-й строки
	# Умножение на 100 используется для перевода вероятности в "веса",
	# хотя математически это эквивалентно (val * rs + val * (1-rs))
	rc1 = (table[0][0] * (rs * 100) + table[0][1] * ((1 - rs) * 100)) / 100
	rc2 = (table[1][0] * (rs * 100) + table[1][1] * ((1 - rs) * 100)) / 100

	# Итоговое мат. ожидание с учетом вероятности выбора строк синим игроком
	blue_count = ((bs * 100) * rc1 + ((1 - bs) * 100) * rc2) / 100
	return round(blue_count, 2)


def theory_blue_win(table, freq_list):
	"""
    Рассчитывает теоретическое мат. ожидание выигрыша Синего игрока.

    Применяется для биматричных игр, где в каждой ячейке хранится список [win_blue, win_red].

    Args:
        table (list): Матрица, где каждый элемент — список или кортеж (выигрыш_Б, выигрыш_К).
        freq_list (tuple): Веса стратегий игроков (bf_list, rf_list).

    Returns:
        float: Средний ожидаемый выигрыш Синего игрока.
    """
	bf_list, rf_list = freq_list
	red_count_list = []

	for strategy in table:
		# Извлекаем только выигрыши Синего игрока (первый элемент в паре)
		rc = [i[0] for i in strategy]

		# Взвешенное среднее выигрышей Синего против всех стратегий Красного
		result_red = sum(
			map(lambda x: x[0] * x[1], zip(rf_list, rc))
		) / sum(rf_list)

		red_count_list.append(round(result_red, 2))

	# Финальное взвешенное среднее с учетом частот стратегий Синего
	bc = sum(map(
		lambda x: x[0] * x[1], zip(bf_list, red_count_list)
	)) / sum(bf_list)

	return round(bc, 2)


def theory_red_win(table, freq_list):
	"""
    Рассчитывает теоретическое мат. ожидание выигрыша Красного игрока.

    Логика аналогична Синему, но матрица транспонируется для удобства
    обхода стратегий Красного как строк.

    Args:
        table (list): Матрица выигрышей.
        freq_list (tuple): Веса стратегий.
    """
	bf_list, rf_list = freq_list
	blue_count_list = []

	# Транспонируем, чтобы смотреть на игру с позиции столбцов (Красного)
	for strategy in transponir(table):
		# Извлекаем последний элемент (выигрыш Красного)
		b = [i[-1] for i in strategy]

		# Ожидаемый результат Красного против всех стратегий Синего
		result_blue = sum(
			map(lambda x: x[0] * x[1], zip(bf_list, b))
		) / sum(bf_list)

		blue_count_list.append(round(result_blue, 2))

	# Усредняем результат по частотам стратегий Красного
	rc = sum(map(
		lambda x: x[0] * x[1], zip(rf_list, blue_count_list)
	)) / sum(rf_list)

	return round(rc, 2)


def theory_game_dev(table, freq_list):
	"""
    Универсальный расчет мат. ожидания для двух типов игр.

    1. Игры с нулевой суммой (в ячейке только число): выигрыш Красного = -выигрыш Синего.
    2. Биматричные игры (в ячейке список): выигрыши считаются независимо.

    Args:
        table: Матрица (числа или списки).
        freq_list: Частоты стратегий.

    Returns:
        tuple: (ожидание_Синего, ожидание_Красного).
    """
	# Проверка: если в ячейке просто число (игра с нулевой суммой)
	if type(table[0][0]) is not list:
		bf_list, rf_list = freq_list
		red_count_list = []
		for strategy in table:
			result_red = sum(
				map(lambda x: x[0] * x[1], zip(rf_list, strategy))
			) / sum(rf_list)
			red_count_list.append(round(result_red, 2))

		bc = sum(map(
			lambda x: x[0] * x[1], zip(bf_list, red_count_list)
		)) / sum(bf_list)

		return round(bc, 2), round(-bc, 2)

	# Если в ячейке список [выигрыш1, выигрыш2]
	else:
		bc = theory_blue_win(table, freq_list)
		rc = theory_red_win(table, freq_list)
		return bc, rc


def game(table, strategy, count_games=1000):
	"""
    Проводит серию случайных игр (метод Монте-Карло) для оценки реальности стратегий.

    Args:
        table (list): Матрица выигрышей (только для игр с нулевой суммой).
        strategy (tuple): Вероятности или частотные списки.
        count_games (int): Количество итераций симуляции.

    Returns:
        float: Средний фактический выигрыш Синего за все игры.
    """
	blue_count = 0
	red_count = 0

	# Определяем, какую функцию выбора использовать (простую или расширенную)
	if type(strategy[0]) is list:
		shuffle = shuffle_strategy_dev
	else:
		shuffle = shuffle_strategy

	for i in range(count_games):
		# Генерируем случайный выбор хода на основе вероятностей
		bs, rs = shuffle(strategy)

		# Начисляем очки (предполагается игра с нулевой суммой)
		blue_count += table[bs][rs]
		red_count -= table[bs][rs]

	# Возвращаем среднее значение выигрыша на одну игру
	return round(blue_count / count_games, 2)


def print_table(table):
	"""
    Выводит матрицу выигрышей в консоль в читаемом виде.
    """
	print("|" * 20)
	# Распаковывает строки матрицы и выводит каждую с новой строки
	print(*table, sep="\n", end="\n")
	print()


def input_strategy(bs=0.0, rs=0.0, auto=False):
	"""
    Получает вероятности стратегий для игры 2x2.

    Args:
        bs, rs: Дефолтные вероятности для Синего и Красного.
        auto: Если True, использует переданные значения без запроса ввода.
    """
	if auto:
		return bs, rs
	else:
		# Ручной ввод вероятностей от пользователя
		bs = float(input("blue = "))
		rs = float(input("red = "))
	return bs, rs


def get_count_strategy(win_table):
	"""
    Определяет размерность игровой матрицы.

    Returns:
        tuple: (количество_стратегий_синего, количество_стратегий_красного).
    """
	count_red_strategy = len(win_table)
	count_blue_strategy = len(win_table[0])
	return count_blue_strategy, count_red_strategy


def input_strategy_dev(count_strategy, auto=False):
	"""
    Запрашивает веса (частоты) для каждой стратегии игрока.

    Args:
        count_strategy: Кортеж с количеством стратегий (bs_c, rs_c).
    """
	bs_c, rs_c = count_strategy
	bs, rs = [], []
	print("input blue strategy")
	for i in range(bs_c):
		bs.append(int(input(f"strategy # {i + 1} >>> ")))
	print("input red strategy")
	for i in range(rs_c):
		rs.append(int(input(f"strategy # {i + 1} >>> ")))
	print("/" * 20)
	return bs, rs


def max_win(matrix):
	"""
    Находит максимальный и минимальный выигрыш Синего игрока в матрице.
    """
	blue_win = [i[0] for i in matrix]
	return max(blue_win), min(blue_win)


def get_win_data(data, objective_list):
	"""
    Извлекает минимальный выигрыш из набора данных и сохраняет его.

    Используется для реализации принципа минимакса (поиск гарантированного результата).
    """
	min_win = min(data)
	objective_list.append(min_win)


def sim_practice():
	"""
    Запускает практическую симуляцию (метод Монте-Карло).

    Перебирает все комбинации вероятностей от 0.0 до 1.0 с шагом 0.01
    и сохраняет результаты практических игр.
    """
	stop = "n"
	objective_data_pract = []

	while stop != "y":
		print_table(table_win)
		count_games = int(input("input count games\n"))
		for b in range(101):
			data_pract = []
			for r in range(101):
				strategy = input_strategy(bs=(b / 100), rs=(r / 100), auto=True)
				# Проведение реальной серии игр
				pract_blue_count = game(table_win, strategy, count_games)
				data_pract.append((pract_blue_count, strategy))

			# Поиск худшего сценария для каждой стратегии синего (принцип min-max)
			get_win_data(data_pract, objective_data_pract)

		for i in objective_data_pract:
			print(i)
		stop = input("stop?\ny/n ")


def sim_theory():
	"""
    Проводит теоретический расчет всех возможных исходов игры.

    Сравнивает гарантированный результат Синего (минимум из максимумов)
    с аналогичным показателем Красного.
    """
	stop = "n"
	objective_data_theory = []

	while stop != "y":
		print_table(table_win)
		for b in range(101):
			data_theory = []
			for r in range(101):
				strategy = input_strategy(bs=(b / 100), rs=(r / 100), auto=True)
				theory_blue_count = theory_game(table_win, strategy)
				data_theory.append((theory_blue_count, strategy[0]))

			get_win_data(data_theory, objective_data_theory)

		# Получаем данные для красного игрока
		odr = sim_theory_red()
		for i in range(len(objective_data_theory)):
			print(f"{objective_data_theory[i]} |  {odr[i]}")
		stop = input("stop?\ny/n ")


def sim_theory_red():
	"""
    Вспомогательная функция для симуляции действий Красного игрока.
    Ищет его минимальные потери (максимизирует выигрыш -theory_blue_count).
    """
	objective_data_theory = []
	for r in range(101):
		data_theory = []
		for b in range(101):
			strategy = input_strategy(bs=(b / 100), rs=(r / 100), auto=True)
			theory_blue_count = theory_game(table_win, strategy)
			# Для красного выигрыш — это инвертированный результат синего
			data_theory.append((-theory_blue_count, strategy[-1]))
		get_win_data(data_theory, objective_data_theory)
	return objective_data_theory


def sim_all():
	"""
    Комплексная симуляция: рассчитывает теорию и практику одновременно.
    Позволяет наглядно увидеть отклонение случайных игр от мат. ожидания.
    """
	stop = "n"
	objective_data_theory = []
	objective_data_pract = []

	while stop != "y":
		print_table(table_win)
		count_games = int(input("input count games\n"))
		for b in range(101):
			data_theory, data_pract = [], []
			for r in range(101):
				strategy = input_strategy(bs=(b / 100), rs=(r / 100), auto=True)
				pract_blue_count = game(table_win, strategy, count_games)
				theory_blue_count = theory_game(table_win, strategy)

				data_theory.append((theory_blue_count, strategy))
				data_pract.append((pract_blue_count, strategy))

			get_win_data(data_theory, objective_data_theory)
			get_win_data(data_pract, objective_data_pract)

		print("T" + "	" * 5 + "P")
		for i in range(len(objective_data_pract)):
			print(f"{objective_data_theory[i]} | {objective_data_pract[i]} ")
		stop = input("stop?\ny/n ")


def sim_game():
	"""
    Меню управления автоматическими симуляциями.

    Позволяет пользователю выбрать между полным анализом, только теорией
    или только практикой. Работает циклично до выбора команды выхода.
    """
	conf = int(input("all >>> 0 / theory >>> 1 / practice >>> 2, exit >>> 3\n"))
	while conf != 3:
		if conf == 0:
			sim_all()
		elif conf == 1:
			sim_theory()
		elif conf == 2:
			sim_practice()
		conf = int(input("all >>> 0 / theory >>> 1 / practice >>> 2, exit >>> 3\n"))


def sum_win(win_data):
	"""
    Рассчитывает средний выигрыш на основе накопленных данных.

    Args:
        win_data (list): Список кортежей, где первый элемент — значение выигрыша.

    Returns:
        float: Среднее арифметическое выигрышей.
    """
	s = 0
	for i in win_data:
		s += i[0]
	return round(s / len(win_data), 2)


def check_strategy():
	"""
    Интерфейс для детальной проверки одной конкретной стратегии.

    Позволяет выбрать игрока (Синий или Красный) и посмотреть,
    как его фиксированная стратегия ведет себя против всех возможных
    ответов оппонента.
    """
	check_side = int(input("blue >>> 0  red >>> 1\n"))
	if check_side == 0:
		data_t, data = check_strategy_blue()
	else:
		data_t, data = check_strategy_red()

	print("T" + "	" * 3 + "P")
	for i in range(len(data)):
		# Вывод сравнения: Теория | Практика
		print(f"{data_t[i]} | {data[i]}")
	# Вывод среднего значения выигрыша при данной стратегии
	print(f"Average win: {sum_win(data)}")


def check_strategy_blue():
	"""
    Анализирует фиксированную стратегию Синего против диапазона ответов Красного.

    Returns:
        tuple: (отсортированные_теоретические_данные, отсортированные_практические_данные).
    """
	bs = float(input("bs = "))
	data, data_t = [], []
	for r in range(101):
		strategy = input_strategy(bs=bs, rs=(r / 100), auto=True)
		# Симуляция игры (метод Монте-Карло)
		blue_count = game(table_win, strategy)
		# Теоретический расчет
		blue_count_t = theory_game(table_win, strategy)

		data.append((blue_count, strategy[1]))
		data_t.append((blue_count_t, strategy[1]))

	print("-" * 15)
	# Сортировка для удобства анализа (от худшего исхода к лучшему)
	return sorted(data_t), sorted(data)


def check_strategy_red():
	"""
    Анализирует фиксированную стратегию Красного против диапазона ответов Синего.

    Для красного выигрыш инвертируется (-blue_count), так как игра
    предполагается с нулевой суммой.
    """
	rs = float(input("rs = "))
	data, data_t = [], []
	for b in range(101):
		strategy = input_strategy(bs=(b / 100), rs=rs, auto=True)
		blue_count = game(table_win, strategy)
		blue_count_t = theory_game(table_win, strategy)

		# Инвертируем результат синего, чтобы получить профит красного
		data.append((-blue_count, strategy[0]))
		data_t.append((-blue_count_t, strategy[0]))

	print("-" * 15)
	return sorted(data_t), sorted(data)


def hand_game(table):
	"""
    Режим "ручного" тестирования конкретных весов стратегий.

    Поддерживает ввод произвольных частот и выводит сравнение
    практического результата симуляции с теоретическим ожиданием.
    """
	mode = "rp"
	while mode == "rp":
		print_table(table)
		count_strategy = get_count_strategy(table)
		# Запрос весов/частот для каждой стратегии
		strategy = input_strategy_dev(count_strategy)

		win_tab = game(table_win, strategy)
		theory = theory_game_dev(table, strategy)

		print(f"Practical result: {win_tab}")
		print(f"Theory result: {theory}")

		mode = input("repeat >> rp, return >> rt, exit >> 0\n")
	return mode


def main():
	"""
    Главная точка входа в программу.

    Распределяет потоки работы:
    1. Автоматический перебор (MinMax)
    2. Ручной ввод стратегий
    3. Детальная проверка одной ветки
    """
	conf = input("auto >>> 1 / hand >>> 2 / check >>> 3 / exit >>> 0\n")
	while conf != "0":
		if conf == "1":
			sim_game()
		elif conf == "2":
			# Возвращает режим (rt/0), чтобы управлять вложенным циклом
			conf = hand_game(table_win)
		elif conf == "3":
			check_strategy()

		if conf == "0": break
		conf = input("auto >>> 1 / hand >>> 2 / check >>> 3 / exit >>> 0\n")

	print(3)
	sys.exit(True)

main()

