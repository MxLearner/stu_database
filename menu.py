import pymssql
from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from function import *

conn = pymssql.connect(server='MX\TEMP', user='111',
                       password='111',database='stu_m', charset='utf8')

cursor = conn.cursor(as_dict=True)  # as_dict=True  transform tuples to dict
if cursor:
    print("successfully connect!")
conn.autocommit(True)
def main():
    # 创建一个注册表单
    while True:
        choice =radio('请选择操作',['查询','选课','退课','修改成绩','结束'])
        if choice =='查询':
            choice = radio('请选择操作', ['查询所有学生选课情况', '查询学生基本信息','查询所有课程情况'])
            if choice=='查询所有学生选课情况':
                search_all(cursor)
            elif choice=='查询学生基本信息':
                search_stu(cursor)
            elif choice=='查询所有课程情况':
                search_course(cursor)
        elif choice=='选课':
            select_course(cursor)
        elif choice == '退课':
            delete_course(cursor)
        elif choice=='修改成绩':
            alter_score(cursor)
        elif choice=='结束':
            put_text("已退出")
            break
        choice = radio('请选择操作', ['回到选择界面', '结束'])
        if choice =='回到选择界面' :
            clear()
            continue
        else:
            put_text("已退出")
            break

# 启动一个Web服务器
if __name__ == '__main__':
    start_server(main, port=8080)

cursor.close()
conn.close()








