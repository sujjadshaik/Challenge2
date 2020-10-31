from face_collections import *
from DynamoDB import *

print("Enter employee details")



emp_img_url = input("Enter Employee Image URL : ")

filename = emp_img_url.split("/")[-1]
add_face('faces',emp_img_url)

emp_id = input("Enter Employee ID : ")
emp_name = input("Enter Employee Name : ")
emp_address = input("Enter Employee Addresss : ")
emp_phone = input("Enter Employee Mobile Number : ")
emp_email = input("Enter Employee Email : ")

insert_emp_details(emp_id,emp_name,emp_phone,emp_email,emp_address,filename)
print(tabel_data())
