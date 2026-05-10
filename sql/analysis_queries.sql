-- 1. Get Overall Churn Rate
SELECT 
    COUNT(*) as TotalCustomers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) as ChurnedCustomers,
    (SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) as ChurnPercentage
FROM customers;

-- 2. Analyze Churn by Contract Type
SELECT 
    Contract, 
    COUNT(*) as CustomerCount,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) as Churned
FROM customers
GROUP BY Contract
ORDER BY Churned DESC;

-- 3. Identify High-Risk Customers (Month-to-month, high charges, tenure < 6)
SELECT customerID, MonthlyCharges, tenure
FROM customers
WHERE Churn = 'Yes' AND Contract = 'Month-to-month' AND tenure < 6
ORDER BY MonthlyCharges DESC;
