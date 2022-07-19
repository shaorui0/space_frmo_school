from mysql_connector import MYSQL


def main():
    # ip: 222.28.46.144
    # port: 3306
    # user: root
    # passwd: 123456
    # database: space
    msql = MYSQL("222.28.46.144",  "root", "123456", "space")
    res = msql.queryData("select * from combat_resource")

    msql = MYSQL("222.28.46.144", "root", "123456", "space")

    res = msql.queryData("select * from combat_resource limit 10")
    print(res)

main()