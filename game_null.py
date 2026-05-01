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


def transponir(matrix):
	t_m = []
	for i in range(len(matrix[0])):
		tmp = []
		for j in range(len(matrix)):
			tmp.append(matrix[j][i])
		t_m.append(tmp)

	return t_m

def shuffle_strategy(strategy_s):
	bs_prob, rs_prob = strategy_s
	# Если случайное число (от 0 до 1) меньше вероятности bs, выбираем 0, иначе 1
	bs_c = 0 if random.random() < bs_prob else 1
	rs_c = 0 if random.random() < rs_prob else 1
	return bs_c, rs_c

def gen_strategy_list(freq_list):
	s = 0
	strategy_list = []
	for freq in freq_list:
		strategy_list += [s] * (freq * 100)
		s+=1
	return strategy_list


def shuffle_strategy_dev(freq_list):
	bs_freq, rs_freq = freq_list

	# choices возвращает список, поэтому берем [0] элемент
	bs_c = random.choices(range(len(bs_freq)), weights=bs_freq, k=1)[0]
	rs_c = random.choices(range(len(rs_freq)), weights=rs_freq, k=1)[0]

	return bs_c, rs_c



def theory_game(table, strategy):
	bs, rs = strategy
	rc1 = (table[0][0] * (rs*100) + table[0][1] *((1-rs)*100))/100
	rc2 =  (table[1][0] * (rs*100) + table[1][1] *((1-rs)*100))/100
	blue_count = ((bs*100)*rc1 + ((1-bs)*100) * rc2)/100
	return round(blue_count, 2)



def theory_blue_win(table, freq_list):
	bf_list, rf_list = freq_list
	red_count_list = []
	for strategy in table:
		rc = [i[0] for i in strategy]

		result_red = sum(
		map(
		lambda x: x[0]*x[1],
		zip(rf_list,rc)))/sum(rf_list)


		red_count_list.append(round(result_red, 2))

	bc = sum(map(
	lambda x: x[0]*x[1],
	zip(bf_list, red_count_list)))/sum(bf_list)

	return round(bc, 2)


def theory_red_win(table, freq_list):
	bf_list, rf_list = freq_list
	blue_count_list = []
	for strategy in transponir(table):
		b = [i[-1] for i in strategy]

		result_blue = sum(
		map(
		lambda x: x[0]*x[1],
		zip(bf_list,b)))/sum(bf_list)


		blue_count_list.append(round(result_blue, 2))

	rc = sum(map(
	lambda x: x[0]*x[1],
	zip(rf_list, blue_count_list)))/sum(rf_list)

	return round(rc, 2)


def theory_game_dev(table, freq_list):
	if type(table[0][0]) is not list:
		bf_list, rf_list = freq_list
		red_count_list = []
		for strategy in table:
			result_red = sum(
			map(
			lambda x: x[0]*x[1],
			zip(rf_list,strategy)))/sum(rf_list)

			red_count_list.append(round(result_red, 2))

		bc = sum(map(
		lambda x: x[0]*x[1],
		zip(bf_list, red_count_list)))/sum(bf_list)

		return round(bc, 2), round(-bc, 2)

	else:
		bc = theory_blue_win(table, freq_list)
		rc = theory_red_win(table, freq_list)
		return bc, rc



def game(table, strategy, count_games=1000):
	blue_count = 0
	red_count = 0
	if type(strategy[0]) is list:
		shuffle = shuffle_strategy_dev
	else:
		shuffle = shuffle_strategy
	for i in range(count_games):
		bs, rs = shuffle(strategy)
		blue_count += table[bs][rs]
		red_count -= table[bs][rs]
	return round(blue_count/count_games, 2)


def print_table(table):
	print("|"*20)
	print(*table, sep="\n", end="\n")
	print()


def input_strategy(bs=0.0, rs=0.0, auto=False):
	if auto:
		return bs, rs
	else:
		bs = float(input("blue = "))
		rs = float(input("red = "))
	return bs, rs

def get_count_strategy(win_table):
	count_red_strategy = len(win_table)
	count_blue_strategy = len(win_table[0])
	return count_blue_strategy, count_red_strategy

def input_strategy_dev(count_strategy, auto=False):
	bs_c, rs_c = count_strategy
	bs = []
	rs = []
	print("input blue strategy")
	for i in range(bs_c):
		bs.append(int(input(f"strategy # {i+1} >>> ")))
	print("input red strategy")
	for i in range(rs_c):
		rs.append(int(input(f"strategy # {i+1} >>> ")))
	print("/"*20)
	return bs, rs



def max_win(matrix):
	blue_win = [i[0] for i in matrix]
	return max(blue_win), min(blue_win)


def get_win_data(data, objective_list):
	#(4.6, (0.0, 0.6)) - пример элемента в data
	min_win = min(data)
	objective_list.append(min_win)

def sim_practice():
	stop = "n"
	objective_data_pract = []

	while stop != "y":
		print_table(table_win)
		count_games = int(input("input count games\n"))
		c = 0
		for b in range(101):
			c+=1
			print(c)
			data_theory = []
			data_pract = []
			for r in range(101):
				strategy = input_strategy(bs=(b/100), rs=(r/100), auto=True)

				pract_blue_count = game(table_win, strategy, count_games)

				data_pract.append(
				(pract_blue_count, strategy)
				)
				#(4.6, (0.0, 0.6)) - пример элемента в data

			get_win_data(data_pract, objective_data_pract)
		for i in objective_data_pract:
			print(i)
		stop = input("stop?\ny/n ")

def sim_theory():
	stop = "n"
	objective_data_theory = []

	while stop != "y":
		print_table(table_win)
		c = 0
		for b in range(101):
			c+=1
			print(c)
			data_theory = []
			for r in range(101):
				strategy = input_strategy(bs=(b/100), rs=(r/100), auto=True)

				theory_blue_count = theory_game(table_win, strategy)

				data_theory.append(
				(theory_blue_count, strategy[0])
				)



				#(4.6, (0.0, 0.6)) - пример элемента в data
			get_win_data(data_theory, objective_data_theory)
		odr = sim_theory_red()
		for i in range(len(objective_data_theory)):
			print(f"{objective_data_theory[i]} |  {odr[i]}")
		stop = input("stop?\ny/n ")

def sim_theory_red():
	objective_data_theory = []

	c = 0
	for r in range(101):
		c+=1
		print(c)
		data_theory = []
		for b in range(101):
			strategy = input_strategy(bs=(b/100), rs=(r/100), auto=True)

			theory_blue_count = theory_game(table_win, strategy)

			data_theory.append(
			(-theory_blue_count, strategy[-1])
			)



				#(4.6, (0.0, 0.6)) - пример элемента в data
		get_win_data(data_theory, objective_data_theory)
	return objective_data_theory



def sim_all():
	stop = "n"
	objective_data_theory = []
	objective_data_pract = []

	while stop != "y":
		print_table(table_win)
		count_games = int(input("input count games\n"))
		c = 0
		for b in range(101):
			c+=1
			print(c)
			data_theory = []
			data_pract = []
			for r in range(101):
				strategy = input_strategy(bs=(b/100), rs=(r/100), auto=True)

				pract_blue_count = game(table_win, strategy, count_games)
				theory_blue_count = theory_game(table_win, strategy)

				data_theory.append(
				(theory_blue_count, strategy)
				)

				data_pract.append(
				(pract_blue_count, strategy)
				)
				#(4.6, (0.0, 0.6)) - пример элемента в data
			get_win_data(data_theory, objective_data_theory)
			get_win_data(data_pract, objective_data_pract)
		print("T"+"	"*5 +"P")
		for i in range(len(objective_data_pract)):
			print(f"{objective_data_theory[i]} | {objective_data_pract[i]} ")
		stop = input("stop?\ny/n ")

def sim_game():
		conf = int(input("all >>> 0 / theory >>> 1 / practice >>> 2, exit >>> 3\n"))
		while conf != 3:
			if conf == 0:
				sim_all()
			elif conf == 1:
				sim_theory()
			else:
				sim_practice()
			conf = int(input("all >>> 0 / theory >>> 1 / practice >>> 2, exit >>> 3\n"))



def sum_win(win_data):
		s = 0
		for i in win_data:
			s += i[0]
		return round(s/len(win_data), 2)


def check_strategy():
	check_side = int(input("blue >>> 0  red >>> 1\n"))
	if check_side == 0:
		data_t, data, = check_strategy_blue()
	else:
		data_t, data = check_strategy_red()
	print("T"+"	"*3+"P")
	for i in range(len(data)):
		print(f"{data_t[i]} | {data[i]}")
	print(sum_win(data))

def check_strategy_blue():
	bs = float(input("bs = "))
	data = []
	data_t = []
	c=0
	for r in range(101):
		c+=1
		print(c)
		strategy = input_strategy(bs=bs, rs=(r/100), auto=True)
		blue_count = game(table_win, strategy)
		blue_count_t = theory_game(table_win, strategy)
		data.append((blue_count, strategy[1]))
		data_t.append((blue_count_t, strategy[1]))
	print("-"*15)
	data = sorted(data)
	data_t = sorted(data_t)
	return data_t, data

def check_strategy_red():
	rs = float(input("rs = "))
	data = []
	data_t = []
	c=0
	for b in range(101):
		c+=1
		print(c)
		strategy = input_strategy(bs=(b/100), rs=rs, auto=True)
		blue_count = game(table_win, strategy)
		blue_count_t = theory_game(table_win, strategy)
		data.append((-blue_count, strategy[0]))
		data_t.append((-blue_count_t, strategy[0]))
	print("-"*15)
	data = sorted(data)
	data_t = sorted(data_t)
	return data_t, data



def hand_game(table):
	mode = "rp"
	while mode == "rp":
		win_matrix = []
		print_table(table)
		count_strategy = get_count_strategy(table)
		strategy = input_strategy_dev(count_strategy)
		win_tab = game(table_win, strategy)
		win_matrix.append(win_tab)
		theory = theory_game_dev(table, strategy)
		print(win_tab)
		print("theory=", theory)
		mode = input("repeat  >> rp return >> rt exit >> 0\n")
	return mode



def main():
	conf = input("auto >>> 1 / hand >>> 2 / check >>> 3 / exit >>> 0\n")
	while conf != "0":
		if conf == "1":
			sim_game()
		elif conf == "2":
			conf = hand_game(table_win)
		elif conf == "3":
			check_strategy()
		conf = input("auto >>> 1 / hand >>> 2 / check >>> 3 / exit >>> 0\n")
	print(3)
	sys.exit(True)

main()

