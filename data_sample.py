import gen

'''
所有gen库中的类均为生成器
所有生成器在一个batch里只会拥有一个值
'''

def get_data():

    batch = gen.batch()
    # 这里一定要用生成器而不能使用[gint(1,10)] * 2
    n, (m, k) = 5, [gen.randint(1,10) for _ in range(2)]
    permutation = gen.shuffle_int(1,n)
    tree1 = gen.tree(1,n,"fa")
    tree2 = gen.tree(1,n,"eage",w=(1,k))

    # 如果sp选择了simple简单图，一定要附加上此图示"sparse"稀疏图还是"dense"稠密图
    graph1 = gen.graph(1,n,m,w=(1,9),sp=["undirected","simple", "sparse"])
    graph2 = gen.graph(1,n,m,sp=["directed","simple", "dense"])
    graph3 = gen.graph(1,n,m,sp=["undirected","multi","noselfloop"])
    graph4 = gen.graph(1,n,m,sp=["directed","multi","selfloop"])

    graph5 = gen.graph_DAG(1,n,m)
    graph6 = gen.graph_DAG(1,n,m,sp="multi")

    batch.addline([n,m,k])
    batch.addline(permutation)
    batch.addline(tree1)

    batch.addline("")
    batch.addline(n)
    batch.addline(tree2)

    # batch.addline("")
    # batch.addline([n,m])
    # batch.addline(graph1)
    # batch.addline(graph2)
    # batch.addline(graph3)
    # batch.addline(graph4)
    # batch.addline(graph5)
    # batch.addline(graph6)
    
    data1 = gen.gen(batch)
    data2 = gen.gen(batch,10)

    return data1

if __name__ == "__main__":
    print(get_data())