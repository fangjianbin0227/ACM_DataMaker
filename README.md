# ACM_DataMaker

本工具主要用来快速生成各种排列，树，图等数据，gen.py为生成数据的核心库
生成数据的用法请参照data_sample.py，模仿写好data.py
然后用命令python3 data.py > data.in即可生成数据文件data.in
再使用自己的STD来跑出data.out，即为一对数据文件

另外bat.py可以用来快速对拍，如果使用小数据对拍，(减小cpp的全局变量内存)或者(增加生成数据的数据组数)可以显著减少对拍时间。
bat.py --file1 你的cpp位置 --file2 STD的位置 --out1 你cpp的输出位置 --out2 STD的输出位置 --dataout 数据的输出位置 --repeat 重复多少次 --bigdata 是否数据过大
默认参数为 bat.py --file1 bat/tmp1.cpp --file2 bat/tmp2.cpp --out1 bat/tmp1.out --out2 bat/tmp2.out --dataout bat/data.out --repeat 1 --bigdata false
