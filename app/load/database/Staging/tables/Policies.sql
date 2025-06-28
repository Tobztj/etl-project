CREATE TABLE Staging.Policies (
    PolicyId        NVARCHAR(15)    NOT NULL,
    CustomerId      NVARCHAR(15)    NOT NULL,
    EventType       NVARCHAR(30)    NOT NULL,
    EventTimestamp  NVARCHAR(MAX)   NOT NULL,
    PolicyType      VARCHAR(50)     NOT NULL,
    PolicyBrand     VARCHAR(50)     NOT NULL,
    PremiumAmount   DECIMAL(15,5)   NULL,
    CoverageAmount  DECIMAL(15,5)   NULL,
    AgeOfInsured    INT             NULL,
    Region          VARCHAR(10)     NULL,
    SourceFile      NVARCHAR(255)   NOT NULL,
    LoadDate        DATETIME2       DEFAULT SYSDATETIME()
);