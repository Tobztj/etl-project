CREATE TABLE Transform.DimPolicy (
    PolicyKey                   INT IDENTITY(1,1) PRIMARY KEY,
    PolicyId                    NVARCHAR(15) NOT NULL,
    PolicyType                  VARCHAR(50) NOT NULL,
    PolicyBrand                 VARCHAR(50) NOT NULL,
    EffectiveDate               DATETIME NOT NULL,
    EndDate                     DATETIME NULL,
    IsCurrent                   BIT NOT NULL,
    LoadDate                    DATETIME2       DEFAULT SYSDATETIME()
);
