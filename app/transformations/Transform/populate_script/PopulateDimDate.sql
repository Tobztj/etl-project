-- Define start and end dates
DECLARE @StartDate DATE = '2020-01-01',
        @EndDate DATE = '2025-12-31'

DECLARE @CurrentDate DATE = @StartDate

-- Loop through the date range
WHILE @CurrentDate <= @EndDate
    BEGIN
        INSERT INTO Transform.DimDate (
            [CalendarDate],
            [Year],
            [Month],
            [Day],
            [Weekday],
            [LoadDate]
        )
        VALUES (
            CAST(@CurrentDate AS DATE),
            CAST(YEAR(@CurrentDate) AS INT),
            CAST(MONTH(@CurrentDate) AS INT),
            CAST(DAY(@CurrentDate) AS INT),
            CAST(DATEPART(WEEKDAY, @CurrentDate) AS INT),
            SYSDATETIME()
        )

        -- Move to the next day
        SET @CurrentDate = DATEADD(DAY, 1, @CurrentDate)
    END;