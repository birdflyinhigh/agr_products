import pymysql


def insert_item(item):

    item = dict(item)


    conn = pymysql.connect(host='localhost', port=3306, user='root', password='mysql', db='products', charset='utf8')


    cur = conn.cursor()

    name = item['name']
    address = item['address']
    url = item['url']
    contact = item['contact']
    description = item['desc']
    big_category = item['big_category']
    small_category = item['small_category']
    child_category = item['child_category']

    words = 'insert into products (name,address,url,contact,description,big_category,small_category,child_category) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s");' % (name,address,url,contact,description,big_category,small_category,child_category)
    print(words)
    cur.execute(words)

    conn.commit()