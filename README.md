**commands to run** <br>
```python3 task.py < input.txt```

for headless version
```python3 headless.py < input.txt```

**Result** <br>
./final_result.png <br>
./headless_final_result.png <br>

<h4> input.txt format </h4> (line number mentioned in brackets)

- date --> 
(1) YYYY-mm-dd HH:MM:SS <br>
- product --> <br>
(2) product_type (eg : Tickets, Guided Tours) <br>
(3) product_name (eg : Brunelleschi's Dome, Cathedral, Museum, Baptistery) <br>
- no of tickets --> <br>
(4) no_of_adult no_of_paid_child <br>
- create_new_account --> <br>
(5) bool (0 or 1) <br>
- credentials --> <br>
 (6) email <br>
 (7) password <br>
    (only if create_new_account) <br>
  (8) uname_first <br>
  (9) uname_last <br>
  
<h4> input.txt example </h4>
2021-10-29 17:15:00 <br>
Tickets <br>
Brunelleschi's Dome <br>
2 2 <br>
1 <br>
myemail@gmail.com <br>
mypassword <br>
my_first_name <br>
my_last_name <br>

