import collections
import enum
import json
import os
import unittest
from contextlib import contextmanager
from functools import reduce, wraps

"""
学习《Python进阶》一书
来源：https://py.eastlakeside.cn/
"""


# 工具
class Tool(unittest.TestCase):

    # dir
    # 展示所有属性和方法
    def test_dir(self):
        my_list = [1, 2, 3]
        print(dir(my_list))

    # type返回对象类型
    # id返回对象id
    def test_type_id(self):
        my_str = "123"
        print(type(my_str))
        print(id(str))


# 语法

# 异常
class MyException(unittest.TestCase):
    def test_e(self):
        try:
            # raise "123"
            print('I am sure no exception is going to occur!')
        except Exception:
            print('exception')
        else:
            # 这里的代码只会在try语句里没有触发异常时运行,
            # 但是这里的异常将 *不会* 被捕获
            print('This would only run if no exception occurs. And an error here '
                  'would NOT be caught.')
        finally:
            print('This would be printed in every case.')


# for-Else
# else会在for循环没有被打断并且执行完毕的情况下执行
class MyForElse(unittest.TestCase):
    def test_for_else(self):
        for n in range(2, 10):
            for x in range(2, n):
                if n % x == 0:
                    print(n, 'equals', x, '*', n / x)
                    break
            else:
                # loop fell through without finding a factor
                print(n, 'is a prime number')


# **kwargs 不定长度的键值对
# *args 非键值对的可变数量的参数列表
# greet_me(name="lyx")
def greet_me(**kwargs):
    for key, value in kwargs.items():
        print("{0} == {1}".format(key, value))


# 上下文管理器
# 1.基于类的实现：定义 __enter__ 和 __exit__ 方法
"""
定义：
class File(object):
    def __init__(self, file_name, method):
        self.file_obj = open(file_name, method)
    def __enter__(self):
        return self.file_obj
    def __exit__(self, type, value, traceback):
        # 在这处理异常（type，value，traceback）
        self.file_obj.close()
        return True
        
用法：
with File('demo.txt', 'w') as opened_file:
    opened_file.write('Hola!')
"""


# 2.基于生成器的实现
def my_context():
    @contextmanager
    def open_file(name):
        f = None
        try:
            f = open(name, 'w')
            yield f
        except IOError:
            print("exception")
        finally:
            if f:
                f.close()


# 函数式编程
# 枚举
class MyEnum(unittest.TestCase):
    def test_enum(self):
        my_list = ['apple', 'banana', 'grapes', 'pear']
        for c, value in enumerate(my_list, 100):
            print(c, value)


# lambda
class MyLambda(unittest.TestCase):
    def test_lambda_sort(self):
        a = [(1, 2), (4, 1), (9, 10), (13, -3)]
        a.sort(key=lambda x: x[1])
        print(a)

    def test_lambda_sort2(self):
        list1 = [1, 2, 3, 6, 9]
        list2 = [2, 5, 6, 7]
        data = zip(list1, list2)
        data = sorted(data)  # 此处已经完成了列表并行排序
        print(*data)
        # 下面展示了反向zip, 即还原出被zip的2个list
        list1, list2 = map(lambda s: list(s), zip(*data))
        print(list1, list2)


# map/filter/reduce
class MyMapFilterReduce(unittest.TestCase):
    # map
    def test_map(self):
        def multiply(x):
            return x * x

        def add(x):
            return x + x

        funcs = [multiply, add]
        for i in range(5):
            value = map(lambda x: x(i), funcs)
            print(list(value))

    # filter
    def test_filter(self):
        number_list = range(-5, 5)
        less_than_zero = filter(lambda x: x < 0, number_list)
        print(list(less_than_zero))

    # reduce
    def test_reduce(self):
        res = reduce(lambda x, y: x + y, (1, 2, 3, 4))
        print(res)


# 推导式（解析式）
class MyComprehensions(unittest.TestCase):
    def test_for_list(self):
        multi = list(x for x in range(0, 100) if x % 2 == 0)
        print(multi)

    def test_for_dict(self):
        a_dict = {'a': 10, 'b': 34, 'A': 7, 'Z': 3}

        a_dict_frequency = {
            k.lower(): a_dict.get(k.lower(), 0) + a_dict.get(k.upper(), 0)
            for k in a_dict.keys()
        }
        print(a_dict_frequency)

        print({v: k for k, v in a_dict.items()})


# 数据结构

# 生成器
# generator version
class MyGen(unittest.TestCase):
    def test_generator(self):
        def fibon(n):
            a = b = 1
            for i in range(n):
                yield b
                a, b = b, a + b

        for i in fibon(10):
            print(i)


# 协程
class MyCoroutine(unittest.TestCase):
    def test_Coroutine(self):
        def grep(pattern):
            print("Searching for", pattern)
            while True:
                line = (yield)
                if pattern in line:
                    print(line)

        search = grep('coroutine')
        next(search)
        search.send("I love you")
        search.send("Don't you love me?")
        search.send("I love coroutine instead!")
        search.close()
        search.send("I love coroutine instead!")


# 数据类型
# collections
class MyCollections(unittest.TestCase):
    colours = (
        ('Yasoob', 'Yellow'),
        ('Ali', 'Blue'),
        ('Arham', 'Green'),
        ('Ali', 'Black'),
        ('Yasoob', 'Red'),
        ('Ahmed', 'Silver'),
    )

    def test_defaultdict(self):
        fav_colors = collections.defaultdict(list)
        for k, v, in self.colours:
            fav_colors[k].append(v)
        print(fav_colors)
        print(dict(fav_colors))

        # 无限嵌套字典
        def tree():
            return collections.defaultdict(tree)

        # tree = lambda: collections.defaultdict(tree)
        some_dict = tree()
        some_dict['colours']['favourite']["hhh"] = "yellow"
        print(json.dumps(some_dict))

    def test_counter(self):
        count = collections.Counter(name for name, color in self.colours)
        print(count)

    def test_deque(self):
        d = collections.deque(i for i in range(1, 4))
        print(d)
        print(d.popleft())
        print(d[0])
        print(d[-1])
        d.extend([4])
        print(d)

    _Animal = None
    _cat = None

    def test_namedtuple(self):
        _Animal = collections.namedtuple('Animal', 'name age type')
        _cat = _Animal(name="miaomiao", age=2, type="cat")
        print(_cat)
        try:
            _cat.age = 3
        except Exception as e:
            print(e)
        print(_cat._asdict())

    def test_enum(self):
        class Species(enum.Enum):
            cat = 1
            dog = 2

        print(Species.cat)
        print(Species(1))


# slot
class MySlot(unittest.TestCase):
    def test_slot(self):
        # 不使用slot
        # 用一个字典来保存一个对象的实例属性
        class Aclass(object):
            def __init__(self, name, age):
                self.name = name
                self.age = age

        # 使用slot
        # 使用 __slots__ 来告诉 Python 不要使用字典，而且只给一个固定集合的属性分配空间
        class Bclass(object):
            __slots__ = ['name', 'age']

            def __init__(self, name, age):
                self.name = name
                self.age = age

# 装饰器
class MyDecorator(unittest.TestCase):

    # 装饰器 decorator
    def test_decorator(self):
        def a_decorator(func):
            @wraps(func)
            def wrapper(*args):
                print("before..........")
                print("函数入参是:{}".format(args))
                func(*args)
                print("after...........")

            return wrapper

        @a_decorator
        def say_hello(*args):
            print("hello world")

        say_hello(3, 4)
        print("原方法name是{}".format(say_hello.__name__))

    # 带参数的装饰器 decorator
    def test_decorator2(self):
        def log(logfile="app.log"):
            def a_decorator(func):
                @wraps(func)
                def wrapper():
                    func()
                    print("执行了" + func.__name__)
                    if not os.path.exists("./log"):
                        os.mkdir("./log")
                    with open(file="./log/{}".format(logfile), mode='a', encoding="utf-8") as open_file:
                        open_file.write("日志文件，方法是:{}\n".format(func.__name__))

                return wrapper

            return a_decorator

        @log(logfile="file0.log")
        def fun1():
            pass

        @log(logfile="file1.log")
        def fun2():
            pass

        fun1()
        fun2()

    # decorator 装饰器类
    def test_decorator3(self):
        class MyDecorator3(object):
            _logfile = 'out.log'

            def __init__(self, func):
                self.func = func

            def __call__(self, *args):
                print(self.func.__name__ + " was called")
                if not os.path.exists("./log"):
                    os.mkdir("./log")
                with open(file="./log/{}".format(self._logfile), mode='a', encoding="utf-8") as open_file:
                    open_file.write("日志文件，方法是:{}\n".format(self.func.__name__))
                self.do_job()
                return self.func(*args)

            @staticmethod
            def do_job():
                print("do job")

        MyDecorator3._logfile = "file3.log"

        @MyDecorator3
        def fun3(args):
            print(args)

        fun3(888)

        class MyDecorator3Email(MyDecorator3):
            _email = "123@qq.com"

            def __init__(self, func):
                super(MyDecorator3Email, self).__init__(func)

            def do_job(self):
                print("sending mail to: {}".format(self._email))

        @MyDecorator3Email
        def fun4(args):
            print(args)

        fun4(999)


if __name__ == '__main__':
    unittest.main()
