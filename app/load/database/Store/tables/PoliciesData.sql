CREATE TABLE Store.PoliciesData(
	PolicyId        NVARCHAR(15)    NOT NULL,
    CustomerId      NVARCHAR(15)    NOT NULL,
    EventType       NVARCHAR(30)    NOT NULL,
    EventTimestamp  DATETIME2       NOT NULL,
    EventDate		DATE			NOT NULL,
	EventTime		TIME			NOT NULL,
    PolicyType      VARCHAR(20)     NOT NULL,
    PolicyBrand     VARCHAR(20)     NOT NULL,
    PremiumAmount   DECIMAL(15,5)   NULL,
    CoverageAmount  DECIMAL(15,5)   NULL,
    AgeOfInsured    INT             NULL,
    Region          VARCHAR(10)     NULL,
    SourceFile      NVARCHAR(MAX)   NOT NULL,
    LoadDate        DATETIME2       DEFAULT SYSDATETIME()
)