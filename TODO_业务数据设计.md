# 业务数据设计

最终是什么样子？


输入，分解

现在是导弹车。。。

反正有个东西能够看看就很好了，日志都打印出来


1. 业务输入数据思考
   1. 现在得把整个一条链路的数据设计好了
      1. 第七旅一营二营 进攻 749高地
      2. a_7_1 a_7_2 hit c_1 c_2
      3. a_7_1_1 a_7_1_2 a_7_1_3 a_7_2_1 a_7_2_2 hit c_1 c_2
      4. 
      5. 1营、2营攻打1号敌人、二号敌人
2. fitness 结合到 cso
3. 张立波的画图代码结合到现有框架
4. 数据库的连接要弄好 + docker

car a_7_1_1 
    type 1
    cordinate 5_5
    hit 0.5
    value 0.9
car a_7_1_2
    type 2
    cordinate 5_5
    hit 0.5
    value 0.9
car a_7_1_3
    type 3
    cordinate 5_5
    hit 0.5
    value 0.9
car a_7_2_1
    type 4
    cordinate 5_5
    hit 0.5
    value 0.9
car a_7_2_2
    type 5
    cordinate 5_5
    hit 0.5
    value 0.9

限制：
第 1 类导弹总共有 x 个
第 2 类导弹总共有 y 个
第 3 类导弹总共有 z 个

n[i][j]
第 i 类导弹，分配给 j 号敌人，多少枚？
这个是通过 fitness 进行一个获取的
我把其他的参数准备好就行了

公开的 fitness 是2维数组的，这里我要搞成多维的，指定n就好了
bound 是上下界


mainView 加进去，没有mainWindow

现在大概能显示出来了，然后管理一下
最后一条链路可以出来了