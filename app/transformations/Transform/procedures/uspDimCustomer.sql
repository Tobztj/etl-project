CREATE PROCEDURE Transform.uspDimCustomer
AS
BEGIN
    SET NOCOUNT ON;

    -- 1. Close current records for customers whose region has changed
    UPDATE dc
    SET dc.EndDate = SYSDATETIME(),
        dc.IsCurrent = 0
    FROM Transform.DimCustomer dc
    JOIN Store.PoliciesData spd
        ON spd.CustomerId = dc.CustomerId
    WHERE dc.IsCurrent = 1
      AND spd.Region <> dc.Region;

    -- 2. Insert new customers or new region records (SCD Type 2)
    INSERT INTO Transform.DimCustomer (
    CustomerId,
    DOB,
    Age,
    Region,
    EffectiveDate,
    EndDate,
    IsCurrent
)
SELECT
    spd.CustomerId,
    CAST(DATEADD(YEAR, -spd.AgeOfInsured, SYSDATETIME()) AS DATE),
    spd.AgeOfInsured,
    spd.Region,
    SYSDATETIME(),
    NULL,
    1
FROM Store.PoliciesData spd
LEFT JOIN Transform.DimCustomer dc
    ON spd.CustomerId = dc.CustomerId
    AND dc.IsCurrent = 1
    AND spd.Region = dc.Region
WHERE dc.CustomerKey IS NULL;

END;