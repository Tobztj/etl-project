CREATE PROCEDURE Transform.uspDimPolicy
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO DimPolicy (
        PolicyId,
        PolicyType,
        PolicyBrand,
        EffectiveDate,
        EndDate,
        IsCurrent
    )
    SELECT
        spd.PolicyId,
        spd.PolicyType,
        spd.PolicyBrand,
        SYSDATETIME(),
        NULL,
        1
    FROM Store.PoliciesData spd
    LEFT JOIN DimPolicy dp
        ON spd.PolicyId = dp.PolicyId
        AND dp.IsCurrent = 1
        AND (spd.PolicyType = dp.PolicyType AND spd.PolicyBrand = dp.PolicyBrand)
    WHERE dp.PolicyKey IS NULL
    -- Or, if different policy type or brand, end current row and insert new one
    OR EXISTS (
        SELECT 1
        FROM DimPolicy dp2
        WHERE dp2.PolicyId = spd.PolicyId
          AND dp2.IsCurrent = 1
          AND (spd.PolicyType <> dp2.PolicyType OR spd.PolicyBrand <> dp2.PolicyBrand)
    );

    -- Handle SCD Type 2 (close current)
    UPDATE dp
    SET dp.EndDate = SYSDATETIME(),
        dp.IsCurrent = 0
    FROM DimPolicy dp
    JOIN Store.PoliciesData spd
        ON spd.PolicyId = dp.PolicyId
    WHERE dp.IsCurrent = 1
      AND (spd.PolicyType <> dp.PolicyType OR spd.PolicyBrand <> dp.PolicyBrand);
END;
