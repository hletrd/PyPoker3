from pypoker3 import poker
import time

p = poker.Poker()

print('Login result: ', end='')
print(p.login('(Your FB Email)', '(Your FB Password)'))

while True:
	pokes = p.get_poke_list()
	print('# of people to poke: ', end='')
	print(len(pokes))
	for i in pokes:
		p.poke_single(i)
		print('Poked ', end='')
		print(i['name'])
	time.sleep(2)