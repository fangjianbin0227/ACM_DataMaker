import random
import copy
import math

class element:
    def __init__(self):
        self.val = None

    def gen(self):
        if isinstance(self,element):
            return self.val if self.val else self.gen()
        else: return self

    def clear(self):
        if isinstance(self,element):
            self.val = None
            self.clear()
    
class randint(element):
    
    def __init__(self, a, b):
        '''
        返回产生一个[a,b]间随机数的生成器
        '''
        super().__init__()
        self.a, self.b = a, b
        
    def gen(self):
        if self.val: return self.val
        x = element.gen(self.a)
        y = element.gen(self.b)
        assert(type(x) == int and type(y) == int and x <= y)
        self.val = random.randint(x, y)
        return self.val

    def clear(self):
        self.val = None
        element.clear(self.a)
        element.clear(self.b)

class shuffle_int(element):
    def __init__(self, a, b):
        '''
        返回一个产生a到b的整数序列的随机排列的生成器
        '''
        super().__init__()
        self.a, self.b = a, b

    def gen(self):
        
        if self.val: return self.val
        x = element.gen(self.a)
        y = element.gen(self.b)
        assert(type(x) == int and type(y) == int and x <= y)
        self.val = [i for i in range(x,y+1)]
        random.shuffle(self.val)
        return " ".join(map(str, self.val))

    def clear(self):
        self.val = None
        element.clear(self.a)
        element.clear(self.b)

class tree(element):
    def __init__(self, a, b, tag,w=None):
        '''
        能返回编号为a到b的一棵树的生成器,
        若希望生成边权w则传入一个范围二元组，默认无边权,
        tag为"fa"则生成一行father,有边权额外生成一行w,
        tage为"eage则生成若干行a,b，有边权额外增加w。
        '''
        super().__init__()
        self.a, self.b, self.tag, self.w = a, b, tag, w

    def gen(self):
        
        if self.val: return self.val
        x = element.gen(self.a)
        y = element.gen(self.b)
        if self.w: w = tuple(map(element.gen, self.w))
        assert(type(x) == int and type(y) == int and x <= y)
        if self.w: assert(w[0] <= w[1])
        
        fa_list, w_list = [], []
        for i in range(x+1, y+1):
            fa_list.append(random.randint(self.a, i-1))
            if self.w: w_list.append(random.randint(w[0], w[1]))
        
        # import traceback
        # traceback.print_stack()
        # print("fa",fa)
        # print("w",w)
        
        if self.tag == "fa" :
            self.val = " ".join(map(str,fa_list)) + "\n"
            if self.w: self.val += " ".join(map(str,w_list)) + "\n"
        else:
            self.val = ""
            if self.w:
                for a,(b,c) in enumerate(zip(fa_list,w_list)):
                    self.val += " ".join(map(str,[a,b,c])) + "\n"
            else:
                for a,b in enumerate(fa_list):
                    self.val += " ".join(map(str,[a,b])) + "\n"

        return self.val[:-1]

    def clear(self):
        self.val = None
        element.clear(self.a)
        element.clear(self.b)

class graph(element):
    def __init__(self, a, b, m, w=None, sp=[]):
        '''
        能返回编号为a到b并且含有m条边的图的生成器,
        若希望生成边权w则传入一个范围二元组，默认无边权,
        生成若干行a到b的边，有边权额外增加w。
        sp为参数列表:
        "undirected"/"directed","simple"/"multi",
        如果选择了simple grahp，则需要带上"sparse"/"dense",
        如果选择了multi grahp，则需要带上"noselfloop"/"selfloop"。
        '''
        super().__init__()
        self.a, self.b, self.m, self.w, self.sp = a, b, m, w, sp

        assert(("undirected" in sp) ^ ("directed" in sp))
        assert(("simple" in sp) ^ ("multi" in sp))
        assert("simple" not in sp or ("sparse" in sp) ^ ("dense" in sp))
        assert("multi" not in sp or ("noselfloop" in sp) ^ ("selfloop" in sp))

    def gen(self):
        
        if self.val: return self.val
        x = element.gen(self.a)
        y = element.gen(self.b)
        m = element.gen(self.m)
        n = y-x+1
        if self.w: w = tuple(map(element.gen, self.w))
        assert(type(x) == int and type(y) == int and x <= y)
        if self.w: assert(w[0] <= w[1])
        assert("undirected" not in self.sp or m <= n*(n-1)//2)
        maxm = n*(n-1)//2 if "directed" in self.sp else \
            (n*(n-1) if "noloop" in self.sp else n*n)
        assert(m <= maxm)
        
        # 分类生成简单/多重图
        e_list = None
        if "simple" in self.sp and "sparse" in self.sp:
            e_list = set()
            i = 0
            while i < m:
                e = (random.randint(x,y),random.randint(x,y))
                if "undirected" in self.sp:
                    if(e[0] > e[1]): e = (e[1], e[0])
                if e[0] == e[1] or e in e_list: continue
                e_list.add(e)
                i += 1

        elif "simple" in self.sp and "dense" in self.sp:
            e_list = list()
            for a in range(x,y+1):
                if "undirected" in self.sp:
                    for b in range(a+1,y+1):
                        e_list.append((a,b))
                else:
                    for b in range(x,y+1):
                        if a != b: e_list.append((a,b))
            e_list = random.sample(e_list,m)
                
        elif "multi" in self.sp:
            e_list = list()
            i = 0
            while i < m:
                e = (random.randint(x,y),random.randint(x,y))
                if "noselfloop" in self.sp and e[0] == e[1]: continue
                if "undirected" in self.sp:
                    if(e[0] > e[1]): e = (e[1], e[0])
                e_list.append(e)
                i += 1
            
        e_list = list(e_list)
        
        self.val = ""
        if self.w:
            w_list = [random.randint(w[0],w[1]) for i in range(m)]
            for (a,b),c in zip(e_list,w_list):
                self.val += " ".join(map(str,[a,b,c])) + "\n"
        else:
            for a,b in e_list:
                self.val += " ".join(map(str,[a,b])) + "\n"

        return self.val[:-1]

    def clear(self):
        self.val = None
        element.clear(self.a)
        element.clear(self.b)
        element.clear(self.m)

def graph_DAG(a,b,m,w=None,sp="simple"):
    '''
    能返回编号为a到b并且含有m条边的DAG的生成器,
    若希望生成边权w则传入一个范围二元组，默认无边权,
    生成若干行a到b的边，有边权额外增加w,
    sp可选"simple"或者"multi",默认"simple"。
    '''
    if sp=="simple": return graph(a,b,m,w,["directed","simple","sparse"])
    else: return graph(a,b,m,w,["directed","multi","noselfloop"])

class batch:
    def __init__(self):
        self.data = []
    
    def gen(self):
        ret = ""
        for i in self.data:
            tmp = ""
            if type(i) == list:
                for j in i:
                    element_of_list = element.gen(j)
                    assert(type(element_of_list) == int)
                    tmp += str(element_of_list) + " "
            else:
                tmp = str(element.gen(i))
            ret += tmp + "\n"
        return ret

    def clear(self):
        for i in self.data:
            if type(i) == list:
                for j in i:
                    element.clear(j)
            else: element.clear(i)

    def addline(self, data):
        '''
        可传入字符串，整数，element的子类，只包含字符串、整数和element子类的列表
        '''
        self.data.append(data)
        
def gen(b: batch, cnt = 0):
    '''
    cnt=0则不含组数t，直接返回batch数据，否则先生成组数t，返回t组batch数据
    '''
    assert(cnt>=0)
    if(cnt==0): return b.gen()
    else:
        ret = str(cnt) + "\n"
        for i in range(cnt):
            b.clear()
            ret += b.gen()
        return ret
