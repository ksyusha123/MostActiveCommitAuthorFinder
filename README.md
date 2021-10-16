# The most active commit author finder  
Автор: Астахова Ксения  

## Описание  
Консольная утилита, которая по организации ищет автора, сделавшего наибольшее количество коммитов. Так же есть возможность вывода круговой диаграммы по ключу -d (--diagram). Она сохраняется в файл authors_activity_pie.png.  

## Требования  
- Python версии не ниже 3.8 
- requests   
- click  

## Состав  
- запускаемый скрипт: main.py  
- модуль для отрисовки круговой диаграммы: diagram.py  

## Пример запуска  
python main.py --help  
python main.py -d ksyusha123 my_unique_token  
