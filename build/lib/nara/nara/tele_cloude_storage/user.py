import time
from tele_db import user_db,table_list,ConfigureDatabase

# print("table_list = ",table_list())
# ConfigureDatabase()
table = user_db("150")
def main():
    while True:
        x = input("'q' to exit >>> ")
        st = time.time()
        if x.lower()=="q":break
        eval(x)
        print(f"Time  = {time.time() - st}")


if __name__ == "__main__":
    st = time.time()
    
    # print(table.append({"fdhfghfghfg":"subhash"}))
    # print(table.append({"hi":"dfdfsgdfgg","hello":"dfdfsgdfgg"}))
    # print(table.append({"hi":"dfdfsgdfgg","hello":"dfdfsgdfgg","_file":{"a.py":"py"}}))
    # print(table.append({"hi":"dfdfsgdfgg","hello":"dfdfsgdfgg","_file":{"https://y20india.in/wp-content/uploads/2024/04/artificial-intelligence-new-technology-science-futuristic-abstract-human-brain-ai-technology-cpu-central-processor-unit-chipset-big-data-machine-learning-cyber-mind-domination-generative-ai-scaled-1-1536x1024.jpg":"jpg"}}))
    # print(table.append({"hi":"dfdfsgdfgg","hello":"dfdfsgdfgg","_file":{"https://images.unsplash.com/photo-1575936123452-b67c3203c357?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8aW1hZ2V8ZW58MHx8MHx8fDA%3D":'jpg',r"https://y20india.in/wp-content/uploads/2024/04/artificial-intelligence-new-technology-science-futuristic-abstract-human-brain-ai-technology-cpu-central-processor-unit-chipset-big-data-machine-learning-cyber-mind-domination-generative-ai-scaled-1-1536x1024.jpg":'png'}}))
    # print(table.append({"_file":{"a.py":"py"}}))
    print(table.show_table(save_file=True))
    # print(table.count())
    # print(table.pop(_id_=855))
    # print(table.delete(_id_=875,key='file_attachments'))
    # print(table.delete(_id_=854,key='subhash'))
    # print(table.edit(_id_=852,key='subhash',new_value="gbgb"))
    # print(table.show_table(save_file=False))
    # print(table.show_table(save_file=True))
    # print(table.show_docs([861]))
    print(f"Time  = {time.time() - st}")
    
    main()