# Python application to retrive data through face recognition

Hi,
This python application uses aws dynamoDb and aws rekognition 

## prerequisites

1. create an AWS account
2. Install AWS cli and configure your credentials.
3. Install Dynamo db in your local computer

That's it your ready

### Run DynamoDB in your local system

<pre>
    <code>
        java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb
    </code>
</pre>

### Go to your python console and run the commands

<pre>
  <code>
    from face_collections import *
    create_collection('faces')
    # you can use any name you want, i used faces as my collection name.
    # this will create a collection with name faces
  </code>
</pre>

### Now create a table in DynamoDB

<pre>
  <code>
    from DynamoDB import *
    create_table('Employee')
    # you can use any name you want , i used Emmployee as my table name
  </code>
</pre>

After creating collection and table now Run Enter_Details.py

Enter the Employee details 

### To check data in table

<pre>
  <code>
    from DynamoDB imoort *
    table_data()
  </code>
</pre>

Ouput will be :
<pre>
<code>
>>>tabel_data()
{'emp_name': 'salman khan', 'emp_image_name': 'salmankhan.jpg', 'emp_address': 'apartments in mumabi road no 112', 'emp_email': 'salmankhan@gmail.com', 'emp_phone': '0000000003', 'emp_id': '3'}
{'emp_name': 'Hrithik roshan', 'emp_image_name': 'HrithikRoshan.jpg', 'emp_address': 'apartments near beach road no 102', 'emp_email': 'hrithik@bollywood.com', 'emp_phone': '0000000004', 'emp_id': '4'}
{'emp_name': 'shahrukh khan', 'emp_image_name': 'shahrukhkhan.jpg', 'emp_address': 'some where in mumbai manat', 'emp_email': 'shahrukh@bollywood.com', 'emp_phone': '0000000002', 'emp_id': '2'}
{'emp_name': 'sujjad', 'emp_image_name': 'IMG.jpg', 'emp_address': 'ngo colony kadapa', 'emp_email': 'sujjadmohammedshaik@gmail.com', 'emp_phone': '0000000001', 'emp_id': '1'}
</code>
</pre>

#### It's time to retrive data from database using face recognition
#### To do this run Get_emp_data_by_face.py

<pre>
<code>

Enter Employee image url : https://raw.githubusercontent.com/sujjadshaik/Challenge2/master/face-to-match/sujjad.jpg
Found 1 match
[{'emp_name': 'sujjad', 'emp_image_name': 'IMG.jpg', 'emp_address': 'ngo colony kadapa', 'emp_email': 'sujjadmohammedshaik@gmail.com', 'emp_phone': '0000000001', 'emp_id': '1'}]

Process 


</code>
</pre>

You will get similar output if it find any face matches in the collection
