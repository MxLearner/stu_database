import pymssql
from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
# 查询学生基本信息
def search_stu(cursor): # 查询学生
    put_markdown('## 查询学生基本信息')
    put_text('请填写以下信息：')
    name = input('姓名')
    # 将用户输入的数据插入到数据库中
    sql = "declare @stu_name nvarchar(50);\n" \
          "set @stu_name = '{}';\n" \
          "select * from stu_name\n" \
          "where name=@stu_name".format(name)

    cursor.execute(sql)
    # 查询数据库中的所有数据
    rows = cursor.fetchall()
    if (rows):
        # 显示数据库中的所有数据
        put_markdown('### 数据库中的查询结果如下：')
        put_table(rows, header=[(put_markdown('学号'), 'stu_id'), (put_markdown("姓名"), 'name'),
                                (put_markdown("年龄"), 'age'), (put_markdown("性别"), 'sex')])
    else:
        put_markdown('### 数据库中无查询结果')

def search_all(cursor): # 查询全部学生
    sql = "select stu_cour.stu_id,stu_name.name as stu_name,stu_cour.course_id,course_name.name as cour_name,score from stu_cour " \
          "inner join stu_name on stu_cour.stu_id=stu_name.stu_id  " \
          "inner join course_name on course_name.course_id=stu_cour.course_id"
    # cursor 返回的字典key是表中列名，用as 重命名可防止重名导致数据覆盖！！！
    cursor.execute(sql)
    # 查询数据库中的所有数据
    rows = cursor.fetchall()
    if (rows):
        # 显示数据库中的所有数据
        put_markdown('### 数据库中的查询结果如下：')
        put_table(rows, header=[(put_markdown('学号'), 'stu_id'), (put_markdown("姓名"), 'stu_name'),
                                (put_markdown("课程编号"), 'course_id'), (put_markdown("课程名称"), 'cour_name'),
                                (put_markdown("得分"),'score')])
        put_text('PS:None代表老师尚未打分')
    else:
        put_markdown('### 数据库中无查询结果')

def search_course(cursor): # 查询课程
    #全新写法 QAQ
    sql = '''
    SELECT
    course_name.course_id,
    course_name.name,
    course_name.val_max,
    COUNT(stu_cour.course_id) AS student_count,
	MAX(score)AS maxx,
	AVG(score) AS avgg
    FROM
        course_name
    INNER JOIN
        stu_cour ON stu_cour.course_id = course_name.course_id
    GROUP BY
        course_name.course_id, course_name.name, course_name.val_max;
    '''

    cursor.execute(sql)
    # 查询数据库中的所有数据
    rows = cursor.fetchall()
    if (rows):
        # 显示数据库中的所有数据
        put_markdown('### 数据库中的查询结果如下：')
        put_table(rows, header=[(put_markdown('课程编号'), 'course_id'), (put_markdown("课程名称"), 'name'),
                                (put_markdown("最大容量"), 'val_max'), (put_markdown("当前已选人数"), 'student_count'),
                                (put_markdown('最高分'),'maxx'),(put_markdown('平均分'),'avgg')])
        put_text('PS:None代表老师尚未打分')
    else:
        put_markdown('### 数据库中无查询结果')

def delete_course(cursor): # 退课
    put_text('请填写以下信息：')
    name = input('姓名')

    sql = '''
    declare @stu_name nvarchar(50);
	set @stu_name = '{}';
	select stu_name.stu_id,stu_name.name as stu_name,stu_cour.course_id ,course_name.name as cour_name from stu_cour
	inner join stu_name on stu_cour.stu_id=stu_name.stu_id 
	inner join course_name on course_name.course_id=stu_cour.course_id
	where stu_name.name=@stu_name
    '''.format(name)

    cursor.execute(sql)
    # 查询数据库中的所有数据
    rows = cursor.fetchall()
    if (rows):
        # 显示数据库中的所有数据
        put_markdown('### 数据库中的查询结果如下：')
        put_table(rows, header=[(put_markdown('学号'), 'stu_id'), (put_markdown("姓名"), 'stu_name'),
                                (put_markdown('课程编号'), 'course_id'), (put_markdown("课程名称"), 'cour_name')])
    else:
        put_markdown('### 数据库中无查询结果')
        return
    data = input_group("", [
        input('学号', name='stu_id'),
        input('课程编号', name='cour_id')
    ])
    stu_id = data['stu_id']
    cour_id=data['cour_id']

    sql='''
    declare @stu_id int;
    declare @course_id int;
    set @stu_id={};
    set @course_id={};
    delete from stu_cour
    where stu_id=@stu_id and course_id=@course_id;
    '''.format(stu_id,cour_id)

    cursor.execute(sql)
    if(cursor.rowcount !=0):
        put_markdown('### 退课成功')
    else:
        put_markdown('### 退课失败，请检查学号，课程号')

def select_course(cursor): # 选课
    put_text('请填写以下信息：')
    name = input('姓名')

    sql = '''
        declare @stu_name nvarchar(50);
    	set @stu_name = '{}';
    	select stu_name.stu_id,stu_name.name as stu_name,stu_cour.course_id ,course_name.name as cour_name from stu_cour
    	inner join stu_name on stu_cour.stu_id=stu_name.stu_id 
    	inner join course_name on course_name.course_id=stu_cour.course_id
    	where stu_name.name=@stu_name
        '''.format(name)

    cursor.execute(sql)
    # 查询数据库中的所有数据
    rows = cursor.fetchall()
    if (rows):
        # 显示数据库中的所有数据
        put_markdown('### 数据库中的查询结果如下：')
        put_table(rows, header=[(put_markdown('学号'), 'stu_id'), (put_markdown("姓名"), 'stu_name'),
                                (put_markdown('课程编号'), 'course_id'), (put_markdown("课程名称"), 'cour_name')])
    else:
        put_markdown('### 数据库中无查询结果')
        return
    data = input_group("", [
        input('学号', name='stu_id'),
        input('课程编号', name='cour_id')
    ])
    stu_id = data['stu_id']
    cour_id = data['cour_id']
    sql='''
    declare @stu_id int;
    declare @course_id int;
    set @stu_id={};
    set @course_id={};
    declare @course_num int;
    declare @course_max int;
    declare @count int;
    select @count=count(*) from stu_cour
    where stu_id=@stu_id and course_id=@course_id;
    select  @course_num=count(course_id)  from stu_cour where course_id=@course_id;
    select  @course_max=val_max  from course_name where course_id=@course_id;
    if(@course_num<@course_max and @count=0 )  -- 判断是否超过课程最大容量
	    begin
            insert into stu_cour(stu_id,course_id)
            values(@stu_id,@course_id);
        end;
    '''.format(stu_id,cour_id)

    cursor.execute(sql)
    if (cursor.rowcount != 0):
        put_markdown('### 选课成功')
    else:
        put_markdown('### 选课失败，请检查学号，课程号')

def alter_score(cursor):
    def check_(key):
        if(key!='111111'):
            return "密码错误"

    key=input("请输入管理员密码",validate=check_)
    data = input_group("", [
        input('学号', name='stu_id'),
        input('课程编号', name='cour_id'),
        input('得分',name='score')
    ])
    stu_id = data['stu_id']
    cour_id = data['cour_id']
    score=data['score']
    sql = '''
    declare @stu_id int;
    declare @course_id int;
    set @stu_id={};
    set @course_id={};
    declare @score int;
    set @score={};
    update stu_cour
    set score=@score
    where stu_id=@stu_id and course_id=@course_id;
    '''.format(stu_id,cour_id,score)

    cursor.execute(sql)
    if (cursor.rowcount != 0):
        put_markdown('### 修改成功')
    else:
        put_markdown('### 修改失败，请检查学号，课程号')

