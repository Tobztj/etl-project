CREATE PROCEDURE Transform.uspFactPolicyEvent
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO Transform.FactPolicyEvent (
        PolicyKey,
        CustomerKey,
        EventTypeKey,
        EventTimestamp,
        DateKey,
        PremiumAmount,
        CoverageAmount,
        SourceFile
    )
    SELECT
        dp.PolicyKey,
        dc.CustomerKey,
        det.EventTypeKey,
        spd.EventTimestamp,
        ddt.DateKey,
        spd.PremiumAmount,
        spd.CoverageAmount,
        spd.SourceFile
    FROM Store.PoliciesData spd
    JOIN Transform.DimPolicy dp
        ON spd.PolicyId = dp.PolicyId AND dp.IsCurrent = 1
    JOIN Transform.DimCustomer dc
        ON spd.CustomerId = dc.CustomerId AND dc.IsCurrent = 1
    JOIN Transform.DimEventType det
        ON spd.EventType = det.EventType
    JOIN Transform.DimDate ddt
        ON CAST(FORMAT(spd.EventTimestamp, 'yyMMdd') AS INT) = CAST(FORMAT(ddt.CalendarDate, 'yyMMdd') AS INT)
    LEFT JOIN Transform.FactPolicyEvent fpe
        ON dp.PolicyKey = fpe.PolicyKey
        AND dc.CustomerKey = fpe.CustomerKey
        AND det.EventTypeKey = fpe.EventTypeKey
        AND ddt.DateKey = fpe.DateKey
    WHERE fpe.PolicyEventId IS NULL;  -- Avoid duplicates
END;
