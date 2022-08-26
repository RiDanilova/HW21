from abc import ABC, abstractmethod


class Storage(ABC):
	@abstractmethod
	def add(self, name, count):
		pass

	@abstractmethod
	def remove(self, name, count):
		pass

	@abstractmethod
	def _get_free_space(self):
		pass

	@abstractmethod
	def _get_items(self):
		pass

	@abstractmethod
	def get_unique_items_count(self):
		pass


class Store(Storage):

	def __init__(self, items: dict, capacity=100):
		self.__items = items
		self.__capacity = capacity

	@property
	def items(self):
		return self.__items

	@items.setter
	def items(self, item: dict):
		self.__items = item

	def add(self, name, count):
		if name in self.__items.keys():
			if self._get_free_space() >= count:
				self.__items[name] += count
				print("Товар успешно добавлен!")
				return True
			else:
				if isinstance(self, Shop):
					print("Недостаточно места в магазине!")
				else:
					print("Недостаточно места на складе!")
				return False
		else:
			if self._get_free_space() >= count:
				self.__items[name] = count
				print("Товар успешно добавлен!")
				return True
			else:
				if isinstance(self, Shop):
					print("Недостаточно места в магазине!")
				else:
					print("Недостаточно места на складе!")
				return False

	def remove(self, name, count):
		if self.__items[name] >= count:
			self.__items[name] -= count
			print("Необходимое количество товара имеется на складе!")
			return True
		else:
			print("Недостаточно товара на складе!")
			return False

	def _get_free_space(self):
		current_space = 0
		for value in self.__items.values():
			current_space += value
		return self.__capacity - current_space

	def _get_items(self):
		return self.__items

	def get_unique_items_count(self):
		return len(self.__items.keys())

	def __str__(self):
		format_list = ""
		for key, value in self.__items.items():
			format_list += f"{key}: {value}\n"
		return format_list


class Shop(Store):
	def __init__(self, items: dict, capacity=20):
		super().__init__(items, capacity)

	def add(self, name, count):
		if self.get_unique_items_count() >= 5:
			print("Уже есть 5 уникальных товаров!")
			return False
		else:
			super().add(name, count)
			return False


class Request:

	def __init__(self, job_request: str):
		job_list = job_request.split()

		job_action = job_list[0]  # выполняемое действие

		self.__amount = int(job_list[1])  # количество товара
		self.__product = job_list[2]  # наименование товара

		if job_action == "Забрать":  # Из указанного места и никуда не отвозить...
			self.__from = job_list[4]  # Откуда забирать
			self.__to = None  # Куда доставить
		elif job_action == "Перевезти":  # Из одного указанного места в другое
			self.__from = job_list[4]  # Откуда забирать
			self.__to = job_list[6]  # Куда доставить
		elif job_action == "Привезти":  # В указанное место из ниоткуда...
			self.__to = job_list[4]
			self.__from = None

	def move(self):
		if self.__from and self.__to:
			if eval(self.__from).remove(self.__product, self.__amount):
				eval(self.__to).add(self.__product, self.__amount)
		elif self.__to:
			eval(self.__to).add(self.__product, self.__amount)
		elif self.__from:
			eval(self.__from).remove(self.__product, self.__amount)


# Данные по складу 'store_1' и магазину 'shop_1'
store_1 = Store(items={"Кружка": 30, "Фонарик": 15, "Отвертка": 10})
shop_1 = Shop(items={"Кружка": 5, "Фонарик": 3, "Удлинитель": 3})
