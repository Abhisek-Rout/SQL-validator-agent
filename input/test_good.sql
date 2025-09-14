-- Correct SQL using GROUP BY
SELECT country, COUNT(customer_id) AS total_customers, AVG(age) AS avg_age
FROM customers
WHERE active = 1
GROUP BY country
HAVING COUNT(customer_id) > 10
ORDER BY total_customers DESC;
