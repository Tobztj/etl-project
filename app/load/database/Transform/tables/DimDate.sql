CREATE TABLE Transform.DimDate (
    [DateKey]                 INT IDENTITY(1,1) PRIMARY KEY,
    [CalendarDate]            DATE NOT NULL,
    [Year]                    INT NOT NULL,
    [Month]                   INT NOT NULL,
    [Day]                     INT NOT NULL,
    [Weekday]                 INT NOT NULL,
    LoadDate                  DATETIME2       DEFAULT SYSDATETIME()
);