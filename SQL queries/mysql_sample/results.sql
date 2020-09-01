use test
set names utf8;

-- 1. Выбрать все товары (все поля)
select * from product

-- 2. Выбрать названия всех автоматизированных складов
SELECT * FROM store
WHERE is_automated = 1

-- 3. Посчитать общую сумму в деньгах всех продаж
SELECT sum(total)
FROM sale


-- 4. Получить уникальные store_id всех складов, с которых была хоть одна продажа
SELECT DISTINCT store_id
FROM sale


-- 5. Получить уникальные store_id всех складов, с которых не было ни одной продажи
SELECT store_id
FROM store LEFT JOIN sale USING(store_id)
WHERE sale_id IS NULL

-- 6. Получить для каждого товара название и среднюю стоимость единицы товара avg(total/quantity), если товар не продавался, он не попадает в отчет.
SELECT name, avg(total/quantity) 
from product JOIN sale using(product_id)
group by name
order by avg(total/quantity) asc

-- 7. Получить названия всех продуктов, которые продавались только с единственного склада
select name 
from product natural join sale 
group by product_id 
having count(distinct store_id) = 1


-- 8. Получить названия всех складов, с которых продавался только один продукт
select name
from sale join store using(store_id)
group by store_id
having count(distinct product_id) = 1

-- 9. Выберите все ряды (все поля) из продаж, в которых сумма продажи (total) максимальна (равна максимальной из всех встречающихся)
select * 
from sale
where total = (select MAX(total)
				from sale)
-- 10. Выведите дату самых максимальных продаж, если таких дат несколько, то самую раннюю из них
select date 
from sale
where total = (select MAX(total)
				from sale)
order by date asc
limit 1
