import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import unquote
import threading

class Poker:
	def __init__(self):
		self.sess = requests.Session()

	def logout(self):
		resp = self.sess.get('https://www.facebook.com/logout.php')
		return True

	def login(self, email, password):
		resp = self.sess.get('https://www.facebook.com')
		soup = BeautifulSoup(resp.text, 'html.parser')
		form = soup.find('form')
		inputs = form.find_all('input')
		inputs = map(lambda x: [x['name'], x['value'] if x.has_attr('value') else None] if x.has_attr('name') else None, inputs)
		inputs = dict(filter(lambda x: x, inputs))
		inputs['email'] = email
		inputs['pass'] = password
		resp = self.sess.post(form['action'], inputs)
		soup = BeautifulSoup(resp.text, 'html.parser')
		result = True
		for i in soup.find_all('input'):
			if i.has_attr('name') and i['name'] == 'email':
				result = False
		return result

	def get_poke_list(self):
		resp = self.sess.get('https://www.facebook.com/pokes')
		soup = BeautifulSoup(resp.text, 'html.parser')
		pokes = soup.find_all('a')
		pokes = filter(lambda x: x.has_attr('ajaxify') and re.search(r'^/pokes', x['ajaxify']), pokes)
		pokes = filter(lambda x: not 'is_hide=1' in x['ajaxify'] and not x.has_attr('data-gt'), pokes)
		pokes = map(lambda x: unquote(x['ajaxify']), pokes)
		pokes = list(pokes)

		names = soup.find_all('a')
		names = list(names)
		names = filter(lambda x: x.has_attr('data-hovercard') and 'user.php' in x['data-hovercard'], names)
		names = map(lambda x: [['name', x.get_text()], ['uid', re.search(r'id=(.*)', x['data-hovercard']).group(0)]], names)
		names = list(names)[0:len(pokes)]
		names = map(lambda x: dict(x[1]+[['poke', pokes[x[0]]]]), enumerate(names))
		return list(names)

	def poke_all(self):
		resp = self.sess.get('https://www.facebook.com/pokes')
		soup = BeautifulSoup(resp.text, 'html.parser')
		pokes = soup.find_all('a')
		pokes = filter(lambda x: x.has_attr('ajaxify') and re.search(r'^/pokes', x['ajaxify']), pokes)
		pokes = filter(lambda x: not 'is_hide=1' in x['ajaxify'] and not x.has_attr('data-gt'), pokes)
		pokes = map(lambda x: unquote(x['ajaxify']), pokes)
		pokes = list(pokes)

		names = soup.find_all('a')
		names = list(names)
		names = filter(lambda x: x.has_attr('data-hovercard') and 'user.php' in x['data-hovercard'], names)
		names = map(lambda x: [['name', x.get_text()], ['uid', re.search(r'id=(.*)', x['data-hovercard']).group(0)]], names)
		names = list(names)[0:len(pokes)]
		names = map(lambda x: dict(x[1]+[['poke', pokes[x[0]]]]), enumerate(names))
		for i in names:
			self.poke_single(i)
		return list(names)

	def poke_single(self, person):
		self.poke_single_async(person)

	def poke_single_async(self, person):
		url = 'https://www.facebook.com/' + person['poke']
		ar = AsyncRequest(self.sess, url)
		ar.start()
		return True

	def poke_single_sync(self, person):
		url = 'https://www.facebook.com/' + person['poke']
		resp = self.sess.get(url)
		return True

class AsyncRequest(threading.Thread):
	def __init__(self, sess, url):
		threading.Thread.__init__(self)
		self.sess = sess
		self.url = url
	
	def run(self):
		resp = self.sess.get(self.url)